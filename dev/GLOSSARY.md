# Translation glossary

This is the **canonical, machine-checked glossary** for Bedrock's trilingual docs. It exists
to stop terminology drift: when the same English term is translated again and again by
different passes (often by AI agents), the rendering tends to wander. This table fixes the
rendering once, and `scripts/check-glossary.py` enforces it.

This file is both the human-readable reference and the data the checker parses, so there is
no second copy to fall out of sync. It is a developer doc (English prose), but the tables
necessarily carry the Chinese and Japanese renderings they document. The CJK cells are
wrapped in `` ` `` so the prose linter leaves their inner punctuation alone; the backticks
are not part of the value.

## How it works

The checker runs two complementary checks, both part of `make check` (the commit gate) and the
pre-commit hook, so drift is caught in CI, not in review. Both are **report-only**: they never
rewrite text, because the right fix is a translation judgement, not a mechanical substitution.

1. **Avoid check (a denylist).** For every entry in the **Avoid** column it scans the CJK docs
   (`docs/zh/`, `docs/ja/`, and the `<!--zh-->` / `<!--ja-->` prose of `src/**.lagda.md`
   masters) and flags any known off-glossary rendering, pointing at the canonical one.
2. **Presence check (a safety net).** For a row marked in the **Presence** column, when the
   English term appears in a doc's English source but the canonical rendering is absent from
   the parallel translation, it warns. This catches wrong renderings the Avoid list does not
   enumerate. It runs only on standalone parallel docs (`docs/en/X` vs `docs/zh/X` / `docs/ja/X`,
   and the root `README.md` for the localized READMEs), never on masters, whose in-file
   language fallback would make absence ambiguous.

## Maintaining the tables

- **Add a row** to the matching category table when a load-bearing term gets a confirmed
  rendering. Fill the canonical `zh` and `ja` columns (wrapped in backticks); leave **Avoid**
  empty for an advisory-only row (agents read it, the Avoid check does not enforce it).
- **Avoid** lists known wrong renderings, separated by `;`. Tag an entry with a language
  (`zh:宪章`, `ja:憲章`) to scope it to that language; an untagged entry (`散文`) applies to
  both Chinese and Japanese.
- **Presence**: put `yes` to enable the safety-net check for that term. Use it for distinctive
  terms whose canonical rendering should always be present; leave it blank for common English
  words (where the English term appears in prose that does not call for the term), to avoid
  false warnings.
- **False positive?** Put `<!-- glossary-ignore -->` on the line for the Avoid check, or
  `<!-- glossary-ignore: charter -->` to suppress one term. For the Presence check, the scoped
  form anywhere in the translated doc suppresses that term's presence warning for that doc.

Renderings below are taken verbatim from the owner's tuned parallel docs (the en/zh/ja
`CHARTER.md` and `README.md`). Where Chinese and Japanese deliberately diverge (for example
`forcing` is 力迫 in zh but 強制 in ja), the Notes say so; do not "unify" them.

## Set theory

| Term (en) | zh | ja | Avoid | Presence | Notes |
|-----------|------|------|-------|----------|-------|
| forcing | `力迫` | `強制` | | yes | zh 力迫 vs ja 強制 (deliberate) |
| forcing extension | `力迫扩张` | `強制拡大` | | | |
| ground model | `基模型` | `基礎モデル` | | | "grounds" also renders 基模型 |
| ground-model definability | `基模型的可定义性` | `基礎モデルの定義可能性` | | | |
| multiverse | `多宇宙` | `多宇宙` | | yes | |
| universism | `单宇宙观` | `単一宇宙観` | | yes | |
| multiversism | `多宇宙观` | `多宇宙観` | | yes | |
| ultrapower | `超幂` | `超冪` | | | |
| set-theoretic geology | `集合论地质学` | `集合論の地質学` | | yes | |
| mantle | `地幔` | `マントル` | | | |
| generic absoluteness | `脱殊绝对性` | `ジェネリック絶対性` | | yes | zh `脱殊` (translate) vs ja `ジェネリック` (transliterate) |
| independence results | `独立性结果` | `独立性の結果` | | | |
| axiom of infinity | `无穷公理` | `無限公理` | | | also "infinity axiom" |
| regularity | `正则公理` | `正則性公理` | | | zh also 正则性 |
| standard model | `标准模型` | `標準モデル` | | | of ZF |
| infinite descent | `无穷下降` | `無限降下` | | | |
| constructible hierarchy | `可构造层级` | `構成可能階層` | | yes | the L hierarchy |

## Type theory

| Term (en) | zh | ja | Avoid | Presence | Notes |
|-----------|------|------|-------|----------|-------|
| host language | `宿主语言` | `ホスト言語` | | | the proof assistant's own language |
| host-language maximalism | `宿主语言最大化` | `ホスト言語最大主義` | | yes | zh 最大化 vs ja 最大主義 (deliberate) |
| unique existence | `唯一存在` | `一意存在` | | | the `isContr` notion |
| definite-description operator | `摹状词算子` | `確定記述の演算子` | | | the `℩` operator |
| description axiom | `描述公理` | `記述公理` | | | |
| propositional extensionality | `命题外延性` | `命題外延性` | | | |
| path equality | `路径等式` | `道の等式` | | | zh 路径 vs ja 道 |
| transport | `传输` | `輸送` | | | structure transport (SIP) |
| inductive type | `归纳类型` | `帰納型` | | | |
| inductive predicate | `归纳谓词` | `帰納的述語` | | | how `L` is defined |
| structural recursion | `结构递归` | `構造的再帰` | | | |
| deep embedding | `深嵌入` | `深い埋め込み` | | | of `Formula` |
| reflection | `反射` | `反射` | | | drives reification |
| reification | reification | reification | | | keep the English word in all languages; do not translate |
| adequacy | `适足性` | `妥当性` | | yes | zh 适足性 vs ja 妥当性 (deliberate) |

## Logic and philosophy

| Term (en) | zh | ja | Avoid | Presence | Notes |
|-----------|------|------|-------|----------|-------|
| satisfaction | `满足关系` | `充足関係` | | | zh 满足 vs ja 充足 (deliberate) |
| arithmetization | `算术化` | `算術化` | | | of syntax |
| Gödel numbering | `哥德尔数` | `ゲーデル数化` | | | |
| first-order definability | `一阶可定义性` | `一階定義可能性` | | | |
| bi-implication | `双向蕴含` | `双条件` | | | ja 双条件 (biconditional); not the calque 双方向含意 |
| proof-theoretic reduction | `证明论归约` | `証明論的還元` | | | reduction: zh 归约 vs ja 還元 |
| classical principles | `经典原理` | `古典原理` | | | LEM, AC |
| metatheory | `元理论` | `メタ理論` | | | meta-level is 元层 / メタレベル |
| metaphysics | `形而上学` | `形而上学` | | yes | of V |
| determinate | `确定` | `確定` | | | of V's structure |
| canonical | `典范` | `典範` | | | |
| falsifiable | `可证伪` | `反証可能` | | | |
| rigor | `严格性` | `厳密さ` | | | |
| finitism | `有穷主义` | `有限主義` | | | |
| neutral ground | `中立的地基` | `中立的な地盤` | | | zh 地基 vs ja 地盤 |
| groundwork | `奠基` | `基盤` | | | the Groundwork / 奠基 / 基盤 section |
| bedrock | `基岩` | `岩盤` | | | the metaphor; the project name Bedrock stays untranslated |

## Other

| Term (en) | zh | ja | Avoid | Presence | Notes |
|-----------|------|------|-------------------|----------|-------|
| charter | `纲领` | `綱領` | `zh:宪章; ja:憲章` | yes | the project's founding document; file slug stays `CHARTER.md` |
| prose | `文稿` | `文章` | `散文` | | written body text, not the literary essay genre |
| proof assistant | `证明助理` | `証明支援系` | | yes | zh 证明助理 vs ja 証明支援系 (deliberate) |
| machine-checked development | `机器验证工作` | `機械検証の開発` | `zh:机器验证开发; zh:机械验证; ja:機械検査の開発` | yes | the README tagline; "machine-checked" is zh 机器 / ja 機械 and "development" is zh 工作 / ja 開発 (deliberate); the certificate/ground phrasings (机器可检的证书 / 经机器检验的地基 etc.) are separate and not covered here |
