#!/usr/bin/env python3
"""Render the multilingual, hyperlinked Bedrock site from the masters.

Inputs (produced by the Makefile before this runs):
  _build/html/<Module>.md   from `agda --html --html-highlight=code` on src/Everything
  _build/types.json         from scripts/extract-types.py
  site/template.html        the page shell
  site/vendor/1lab/...      vendored front-end assets (M2c builds CSS/JS into the site)

For each enabled language it weaves the prose by markers, splices the language-neutral
highlighted code, resolves inline `name`{.Agda} references, protects math for client-side
KaTeX, rewrites links (+ data-type for hover), and writes _build/site/<lang>/<Module>.html.
It also emits per-module types/<Module>.json (pos -> abbreviated, hyperlinked type) and a
per-language search.json, a per-language index, and a root language-redirect + 404.

Usage:
  render-site.py [--html-dir _build/html] [--types _build/types.json] [--src src]
                 [--template site/template.html] [--out _build/site]
                 [--langs en,zh] [--base-url ""] [--site Bedrock]
"""

import glob
import hashlib
import html as htmllib
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from i18n_markers import weave, group_languages  # noqa: E402

LANG_LABELS = {"en": "English", "zh": "中文", "ja": "日本語"}

UI = {
    "en": {"search": "Search…", "theme": "Toggle theme", "contents": "On this page",
           "menu": "Menu", "close": "Close",
           "untranslated": "This page is not yet translated; showing English.",
           "modules": "Modules", "source": "Source", "overview": "Overview",
           "license": "content licensed CC BY-NC-SA 4.0",
           "credit": 'Rendered with a generator adapted from '
                     '<a href="https://1lab.dev">the 1lab</a> (AGPL-3.0).',
           "external": "You are viewing the Cubical library.",
           "back": "Back to Bedrock"},
    "zh": {"search": "搜索…", "theme": "切换主题", "contents": "本页内容",
           "menu": "菜单", "close": "关闭",
           "untranslated": "本页尚未翻译，此处显示英文。",
           "modules": "模块", "source": "源码", "overview": "概览",
           "license": "内容以 CC BY-NC-SA 4.0 许可",
           "credit": '使用改编自 <a href="https://1lab.dev">1lab</a> 的生成器渲染 '
                     '(AGPL-3.0)。',
           "external": "您正在浏览 Cubical 库。",
           "back": "返回 Bedrock"},
    "ja": {"search": "検索…", "theme": "テーマ切替", "contents": "このページの内容",
           "menu": "メニュー", "close": "閉じる",
           "untranslated": "このページは未翻訳です。英語を表示しています。",
           "modules": "モジュール", "source": "ソース", "overview": "概要",
           "license": "コンテンツは CC BY-NC-SA 4.0 ライセンス",
           "credit": '<a href="https://1lab.dev">1lab</a> を改変した'
                     'ジェネレータでレンダリング (AGPL-3.0)。',
           "external": "Cubical ライブラリを閲覧しています。",
           "back": "Bedrock に戻る"},
}
SOURCE_URL = "https://github.com/choukh/Bedrock"
LANDING = "Everything"  # the aggregator master; rendered as the site landing index.html

PRE_RE = re.compile(r'<pre class="Agda">.*?</pre>', re.DOTALL)
# Definition site: <a id="NAME"></a><a id="POS" ... class="ASPECT" ...>token</a>
DEF_RE = re.compile(r'<a id="([^"]+)"></a><a id="(\d+)"[^>]*class="([^"]*)"')
# Any cross-reference link inside highlighted code (optional self-id, optional #position).
LINK_RE = re.compile(r'<a (id="\d+" )?href="([^"#]+)\.html(#\d+)?"([^>]*)>')
INLINE_AGDA_RE = re.compile(r'`([^`]+)`\{\.Agda\}')
NUL = "\x00"


# ---- small stdlib Markdown renderer (the prose subset Bedrock uses) ----------

def _slug(n):
    return f"sec-{n}"


_PLACEHOLDER = re.compile(NUL + r'[A-Z]+\d+' + NUL)


def _inline(s):
    out = []
    for part in re.split(r'(`[^`]+`)', s):
        if part.startswith("`") and part.endswith("`"):
            out.append(f"<code>{htmllib.escape(part[1:-1])}</code>")
            continue
        for seg in re.split(r'(' + NUL + r'[A-Z]+\d+' + NUL + r')', part):
            if _PLACEHOLDER.fullmatch(seg):    # protected span: leave verbatim
                out.append(seg)
                continue
            p = htmllib.escape(seg, quote=False)
            p = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', p)
            p = re.sub(r'\*\*([^*]+)\*\*', r'<strong>\1</strong>', p)
            p = re.sub(r'(?<!\*)\*([^*\s][^*]*?)\*(?!\*)', r'<em>\1</em>', p)
            out.append(p)
    return "".join(out)


def _is_block_start(line):
    s = line.lstrip()
    return (not s or s.startswith("#") or s.startswith(">")
            or re.match(r'^([-*+]|\d+\.)\s', s) or re.match(r'^(```|~~~)', s)
            or re.match(r'^([-*_])(\s*\1){2,}\s*$', s.strip())
            or s.startswith("<") or re.match(r'^' + NUL, s))


def md_to_html(text):
    """Return (html, toc) where toc is a list of (level, id, text) for h2..h6."""
    lines = text.split("\n")
    out, toc = [], []
    i, n = 0, len(lines)
    hcount = 0
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        m = re.match(r'^(#{1,6})\s+(.*)$', line)
        if m:
            level = len(m.group(1))
            text_in = m.group(2).strip()
            hid = _slug(hcount); hcount += 1
            if level >= 2:
                toc.append((level, hid, re.sub(r'`([^`]+)`', r'\1', text_in)))
            out.append(f'<h{level} id="{hid}">{_inline(text_in)}</h{level}>')
            i += 1
            continue
        if re.match(r'^([-*_])(\s*\1){2,}\s*$', line.strip()):
            out.append("<hr/>"); i += 1; continue
        mf = re.match(r'^\s*(```|~~~)(.*)$', line)
        if mf:
            fence = mf.group(1); body = []
            i += 1
            while i < n and not lines[i].lstrip().startswith(fence):
                body.append(lines[i]); i += 1
            i += 1
            out.append('<pre class="sourceCode"><code>'
                       + htmllib.escape("\n".join(body)) + "</code></pre>")
            continue
        if line.strip().startswith(NUL) and line.strip().endswith(NUL):
            out.append(line.strip()); i += 1; continue
        if line.lstrip().startswith("<"):
            block = []
            while i < n and lines[i].strip():
                block.append(lines[i]); i += 1
            out.append("\n".join(block)); continue
        if re.match(r'^\s*([-*+]|\d+\.)\s+', line):
            ordered = bool(re.match(r'^\s*\d+\.\s+', line))
            items = []
            while i < n and re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i]):
                item = re.sub(r'^\s*([-*+]|\d+\.)\s+', '', lines[i]); i += 1
                cont = []
                while i < n and lines[i].strip() and not re.match(r'^\s*([-*+]|\d+\.)\s+', lines[i]) \
                        and not _is_block_start(lines[i]):
                    cont.append(lines[i].strip()); i += 1
                items.append("<li>" + _inline(" ".join([item] + cont)) + "</li>")
            tag = "ol" if ordered else "ul"
            out.append(f"<{tag}>" + "".join(items) + f"</{tag}>")
            continue
        if line.lstrip().startswith(">"):
            block = []
            while i < n and lines[i].lstrip().startswith(">"):
                block.append(re.sub(r'^\s*>\s?', '', lines[i])); i += 1
            inner, _ = md_to_html("\n".join(block))
            out.append("<blockquote>" + inner + "</blockquote>")
            continue
        para = [line]; i += 1
        while i < n and lines[i].strip() and not _is_block_start(lines[i]):
            para.append(lines[i]); i += 1
        out.append("<p>" + _inline(" ".join(s.strip() for s in para)) + "</p>")
    return "\n".join(out), toc


# ---- code-block index (names, positions, types) ------------------------------

def source_file(html_dir, module):
    """agda --html emits <Module>.md for literate sources (prose + <pre class=Agda> code) and
    <Module>.html for library modules (bare highlighted code, no <pre>). Returns (path,
    is_literate)."""
    md = os.path.join(html_dir, module + ".md")
    if os.path.exists(md):
        return md, True
    return os.path.join(html_dir, module + ".html"), False


def index_definitions(code_html, module, name2pos, pos_aspect):
    """Record (module-local name -> pos) and (pos -> aspect) from highlighted code."""
    for name, pos, aspect in DEF_RE.findall(code_html):
        name2pos.setdefault(module, {})[name] = pos
        pos_aspect.setdefault(module, {})[pos] = aspect.split()[-1] if aspect else ""


def render_type(term, internal_q):
    """Abbreviate module qualifiers and hyperlink internal identifiers in a type string."""
    s = htmllib.escape(term.replace("\n", " "), quote=False)
    links = []
    for q in sorted(internal_q, key=len, reverse=True):
        if q in s:
            mod, pos = internal_q[q]
            tok = f"{NUL}L{len(links)}{NUL}"
            last = q.split(".")[-1]
            links.append(f'<a href="{mod}.html#{pos}">{htmllib.escape(last)}</a>')
            s = s.replace(q, tok)
    s = re.sub(r"(?:[A-Za-z][\w']*\.)+", "", s)        # strip remaining (external) qualifiers
    s = re.sub(r"\bSet\b", "Type", s)                  # cubical display
    for i, link in enumerate(links):
        s = s.replace(f"{NUL}L{i}{NUL}", link)
    return s


# ---- per-page rendering ------------------------------------------------------

def lang_nav(out_name, lang, langs):
    """Language switcher; `out_name` is this page's filename (index.html for the landing)."""
    bits = []
    for L in langs:
        if L == lang:
            bits.append(f'<span class="cur">{LANG_LABELS[L]}</span>')
        else:
            bits.append(f'<a href="../{L}/{out_name}">{LANG_LABELS[L]}</a>')
    return " · ".join(bits)


def hreflang_links(out_name, langs, base):
    return "\n".join(
        f'  <link rel="alternate" hreflang="{L}" href="{base}/{L}/{out_name}" />'
        for L in langs)


def toc_html(toc, lang):
    """The 'On this page' sidebar section (empty when the page has no sub-headings)."""
    if not toc:
        return ""
    items = "".join(f'<li class="toc-l{lvl}"><a href="#{hid}">{htmllib.escape(t)}</a></li>'
                    for lvl, hid, t in toc)
    return (f'<div class="nav-title">{UI[lang]["contents"]}</div>'
            f'<ul class="toc">{items}</ul>')


def modules_nav(current, mods, lang):
    """The 'Modules' sidebar section: every internal module (current one highlighted)."""
    items = "".join(
        f'<li{" class=cur" if m == current else ""}><a href="{m}.html">{m}</a></li>'
        for m in mods)
    return (f'<div class="nav-title">{UI[lang]["modules"]}</div>'
            f'<ul class="modnav">{items}</ul>')


def ext_banner(lang):
    """Prominent header marking a page as external to Bedrock (links home)."""
    s = UI[lang]
    return (f'<div class="ext-banner">⚠ {htmllib.escape(s["external"])} '
            f'<a href="index.html">{htmllib.escape(s["back"])}</a></div>')


def footer_html(lang):
    s = UI[lang]
    source = f'<a href="{SOURCE_URL}">{s["source"]}</a>'
    copyright_ = f'© 2026 choukh (choukyuhei@gmail.com) · {s["license"]} · {source}'
    return (f'<div class="footer-credit">{s["credit"]}</div>'
            f'<div class="footer-copyright">{copyright_}</div>')


def rewrite_links(body, rendered, types_global):
    """Keep links to any rendered module (internal or external), tagging data-type when the
    TARGET has a type (drives hover, including on cubical identifiers). Links to a module we
    did not render lose their dead href (the <a> element stays so the </a> still matches).

    `types_global` is {module: {pos: type-html}} across ALL rendered modules."""
    def repl(m):
        idpart, mod, anchor, rest = m.group(1) or "", m.group(2), m.group(3) or "", m.group(4)
        if mod in rendered:
            pos = anchor[1:] if anchor else ""
            extra = f' data-type="{mod}#{pos}"' if pos and pos in types_global.get(mod, {}) else ""
            target = "index.html" if mod == LANDING else f"{mod}.html"  # landing -> index.html
            return f'<a {idpart}href="{target}{anchor}"{rest}{extra}>'
        return f'<a{rest}>'                          # not rendered: drop the dead href
    return LINK_RE.sub(repl, body)


def build_types(modules, name2pos, types_raw, internal_q):
    """Global {module: {pos: abbreviated/hyperlinked type-html}} for hover + sidecars."""
    g = {}
    for m in modules:
        g[m] = {}
        for name, pos in name2pos.get(m, {}).items():
            t = types_raw.get(m, {}).get(name.split(".")[-1])
            if t:
                g[m][pos] = render_type(t, internal_q)
    return g


def fill_template(tpl, **kw):
    out = tpl
    for k, v in kw.items():
        out = out.replace(f"%%{k}%%", v)
    return out


def render_module(module, html_dir, langs, internal, rendered, modnav_list,
                  name2pos, types_global, tpl, out_dir, base, site):
    path, literate = source_file(html_dir, module)
    raw = open(path, encoding="utf-8").read()

    is_external = module not in internal
    is_landing = module == LANDING
    out_name = "index.html" if is_landing else module + ".html"
    current = "" if (is_external or is_landing) else module  # highlight in the modules nav
    langs_present = group_languages(raw) if literate else set()

    if literate:
        # lift the highlighted code blocks out (language-neutral, shared across languages)
        code_blocks = []
        def lift(m):
            code_blocks.append(m.group(0))
            return f"{NUL}CODE{len(code_blocks)-1}{NUL}"
        text = PRE_RE.sub(lift, raw)

    def page_body(lang):
        if not literate:
            # a library page is bare highlighted code: wrap it and resolve its links
            code = rewrite_links('<pre class="Agda">' + raw + '</pre>', rendered, types_global)
            return code, []
        woven = weave(text, lang)
        store = {}
        def stash(kind, payload):
            key = f"{NUL}{kind}{len(store)}{NUL}"
            store[key] = payload
            return key
        woven = re.sub(r'\$\$(.+?)\$\$',
                       lambda m: stash("DMATH", '<div class="math display">$$'
                                       + htmllib.escape(m.group(1)) + '$$</div>'),
                       woven, flags=re.DOTALL)
        woven = re.sub(r'\$(.+?)\$',
                       lambda m: stash("IMATH", '<span class="math inline">$'
                                       + htmllib.escape(m.group(1)) + '$</span>'),
                       woven)
        woven = INLINE_AGDA_RE.sub(lambda m: stash("REF", inline_ref(m.group(1),
                                   internal, name2pos)), woven)
        body, toc = md_to_html(woven)
        body = re.sub(r'<p>\s*(' + NUL + r'CODE\d+' + NUL + r')\s*</p>', r'\1', body)
        body = re.sub(r'<p>\s*(' + NUL + r'DMATH\d+' + NUL + r')\s*</p>', r'\1', body)
        for key, val in store.items():
            body = body.replace(key, val)
        for j, blk in enumerate(code_blocks):
            body = body.replace(f"{NUL}CODE{j}{NUL}", blk)
        return rewrite_links(body, rendered, types_global), toc

    for lang in langs:
        body, toc = page_body(lang)

        banner = ""
        if langs_present and lang not in langs_present:
            banner = f'<div class="banner">{UI[lang]["untranslated"]}</div>'

        title = UI[lang]["overview"] if is_landing else module
        page = fill_template(
            tpl, LANG=lang, TITLE=htmllib.escape(title), SITE=site, DESC=site,
            BASEURL=base, MODULE=module,
            BODYCLASS="text-page external" if is_external else "text-page",
            EXTBANNER=ext_banner(lang) if is_external else "",
            HREFLANG=hreflang_links(out_name, langs, base),
            LANGNAV=lang_nav(out_name, lang, langs),
            MODNAV=modules_nav(current, modnav_list, lang),
            TOC=toc_html(toc, lang), BANNER=banner, BODY=body, FOOTER=footer_html(lang),
            S_SEARCH=UI[lang]["search"], S_THEME=UI[lang]["theme"],
            S_MENU=UI[lang]["menu"], S_CLOSE=UI[lang]["close"])
        dest = os.path.join(out_dir, lang, out_name)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        open(dest, "w", encoding="utf-8").write(page)

    # per-module type sidecar (keyed by the real module name; hover fetches types/<mod>.json)
    sidecar = json.dumps(types_global.get(module, {}), ensure_ascii=False)
    for lang in langs:
        tdir = os.path.join(out_dir, lang, "types")
        os.makedirs(tdir, exist_ok=True)
        open(os.path.join(tdir, module + ".json"), "w", encoding="utf-8").write(sidecar)


def inline_ref(name, internal, name2pos):
    """Render `name`{.Agda} as a highlighted, hyperlinked span if the identifier is known."""
    target = None
    if "." in name:
        mod, _, local = name.rpartition(".")
        if mod in internal and local in name2pos.get(mod, {}):
            target = (mod, name2pos[mod][local])
    if target is None:
        for mod in internal:
            if name in name2pos.get(mod, {}):
                target = (mod, name2pos[mod][name]); break
    label = htmllib.escape(name)
    if target:
        mod, pos = target
        return (f'<a class="Agda inline-ref" href="{mod}.html#{pos}" '
                f'data-type="{mod}#{pos}">{label}</a>')
    return f'<code class="Agda inline-ref">{label}</code>'


# ---- site-level outputs ------------------------------------------------------

def write_search(out_dir, lang, modules, name2pos, pos_aspect, types_by_module):
    entries = []
    for m in modules:
        for name, pos in name2pos.get(m, {}).items():
            t = types_by_module.get(m, {}).get(pos, "")
            entries.append({"name": name, "module": m, "anchor": pos,
                            "aspect": pos_aspect.get(m, {}).get(pos, ""),
                            "type": re.sub(r"<[^>]+>", "", t),
                            "href": f"{m}.html#{pos}"})
    open(os.path.join(out_dir, lang, "search.json"), "w", encoding="utf-8").write(
        json.dumps(entries, ensure_ascii=False))


def write_root(out_dir, langs, base):
    default = langs[0]
    redirect = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<title>Bedrock</title><script>
var ls = {json.dumps(langs)};
var want = (navigator.language||"en").slice(0,2);
var to = ls.indexOf(want) >= 0 ? want : "{default}";
location.replace("{base}/" + to + "/index.html");
</script><meta http-equiv="refresh" content="0; url={base}/{default}/index.html"></head>
<body><a href="{base}/{default}/index.html">Enter</a></body></html>"""
    open(os.path.join(out_dir, "index.html"), "w", encoding="utf-8").write(redirect)
    open(os.path.join(out_dir, "404.html"), "w", encoding="utf-8").write(redirect)


def main(argv):
    html_dir, types_path, src = "_build/html", "_build/types.json", "src"
    tpl_path, out_dir = "site/template.html", "_build/site"
    static_dir = "site/static"
    langs, base, site = ["en", "zh"], "", "Bedrock"
    i = 0
    while i < len(argv):
        a = argv[i]
        if a == "--html-dir": i += 1; html_dir = argv[i]
        elif a == "--types": i += 1; types_path = argv[i]
        elif a == "--src": i += 1; src = argv[i]
        elif a == "--template": i += 1; tpl_path = argv[i]
        elif a == "--out": i += 1; out_dir = argv[i]
        elif a == "--static": i += 1; static_dir = argv[i]
        elif a == "--langs": i += 1; langs = [x for x in argv[i].split(",") if x]
        elif a == "--base-url": i += 1; base = argv[i].rstrip("/")
        elif a == "--site": i += 1; site = argv[i]
        else: sys.stderr.write(f"unknown option: {a}\n"); return 2
        i += 1

    internal = set(
        os.path.relpath(p, src)[:-len(".lagda.md")].replace(os.sep, ".")
        for p in glob.glob(os.path.join(src, "**", "*.lagda.md"), recursive=True))

    # the full reachable set = every module agda --html emitted (Bedrock .md + library .html)
    rendered = sorted(set(
        os.path.basename(p).rsplit(".", 1)[0]
        for p in glob.glob(os.path.join(html_dir, "*.md"))
        + glob.glob(os.path.join(html_dir, "*.html"))))
    rendered_set = set(rendered)
    if not rendered:
        sys.stderr.write(f"no highlighted output in {html_dir}; run `agda --html` first\n")
        return 1
    modnav_list = sorted(m for m in internal if m != LANDING)  # Modules sidebar (home excluded)

    types_raw = json.load(open(types_path, encoding="utf-8")) if os.path.exists(types_path) else {}
    tpl = open(tpl_path, encoding="utf-8").read()
    # cache-bust: stamp ?v=<hash> on the CSS/JS so browsers always pick up changes
    def _ver(name):
        p = os.path.join(static_dir, name)
        try:
            return hashlib.sha1(open(p, "rb").read()).hexdigest()[:8]
        except OSError:
            return "0"
    tpl = tpl.replace("%%CSSVER%%", _ver("bedrock.css")).replace("%%JSVER%%", _ver("bedrock.js"))

    # first pass: index every definition (names, positions, aspects) across ALL rendered modules
    name2pos, pos_aspect = {}, {}
    for m in rendered:
        path, literate = source_file(html_dir, m)
        content = open(path, encoding="utf-8").read()
        if literate:
            for blk in PRE_RE.findall(content):
                index_definitions(blk, m, name2pos, pos_aspect)
        else:
            index_definitions(content, m, name2pos, pos_aspect)   # whole .html is code
    internal_q = {f"{m}.{n}": (m, p) for m in name2pos for n, p in name2pos[m].items()}
    types_by_module = build_types(rendered, name2pos, types_raw, internal_q)

    # second pass: render every reachable module (externals get the "left Bedrock" banner;
    # the Everything aggregator renders to index.html)
    for m in rendered:
        render_module(m, html_dir, langs, internal, rendered_set, modnav_list,
                      name2pos, types_by_module, tpl, out_dir, base, site)

    search_mods = sorted(internal)                   # search indexes Bedrock identifiers only
    for lang in langs:
        os.makedirs(os.path.join(out_dir, lang), exist_ok=True)
        write_search(out_dir, lang, search_mods, name2pos, pos_aspect, types_by_module)
    write_root(out_dir, langs, base)

    if os.path.isdir(static_dir):                    # committed CSS/JS/favicon
        shutil.copytree(static_dir, os.path.join(out_dir, "static"), dirs_exist_ok=True)

    print(f"rendered {len(rendered)} module(s) ({len(internal)} internal) "
          f"x {len(langs)} language(s) -> {out_dir}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
