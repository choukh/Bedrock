<h1 style="display: flex; align-items: center; gap: 0.35rem"><img src="../../site/static/favicon.svg" alt="" height="32" align="middle"> Bedrock</h1>

[English](../../README.md) · **中文** · [日本語](../ja/README.md)

[![Typecheck](https://github.com/choukh/Bedrock/actions/workflows/typecheck.yml/badge.svg)](https://github.com/choukh/Bedrock/actions/workflows/typecheck.yml)
![Status: early](https://img.shields.io/badge/status-early-orange)
[![Agda](https://img.shields.io/badge/Agda-2.8.0-blue)](https://github.com/agda/agda)
[![cubical](https://img.shields.io/badge/cubical-0.9-blue)](https://github.com/agda/cubical)
[![Content: CC BY-NC-SA 4.0](https://img.shields.io/badge/content-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Code: AGPL-3.0-only](https://img.shields.io/badge/code-AGPL--3.0--only-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![REUSE status](https://api.reuse.software/badge/github.com/choukh/Bedrock)](https://api.reuse.software/info/github.com/choukh/Bedrock)

*为 V 的形而上学奠基。*

一项在 [Cubical Agda](https://github.com/agda/cubical) 中的机器验证工作，针对当代集合宇宙问题背后的那部分集合论：力迫、内模型，以及 V 的结构。

## 首个目标

眼下的首要目标，是完整机械化：

> **`L` ⊨ GCH**，其中 `L` 是在以高阶归纳类型实现的累积层级 `V` 之上构造的可构造层级。这是一个宿主内部的语义定理。

内容是哥德尔 1938 年的结果，但路线不是教科书那条，也没有人针对 GCH 走过这条路线。它适合作为第一块基石，是因为它会演练本项目其余部分所需的整个基础层：深嵌入的一阶语言、累积层级、`L`、以及双语义机制。而它从第一行起就锚定了下文那套宿主语言最大化的进路。把它做对，就校准了其余一切赖以站立的基础设施。

## 方向

越过这第一块基石，长期目标是把机械化集合论推过它当前的止步处。现有的力迫形式化止步于 Cohen (1963)，而目标是抵达本世纪的成果：力迫作为研究多宇宙的工具、基模型的可定义性、地幔，以及「V 究竟是否具有确定结构」这一更宏大的问题。

这些是目标，不是承诺。每一项都唯有经检验后才会在此宣告。

## 奠基

本项目的目标不是裁定 V 的形而上学，而是为它奠定一份经过验证的根基：将那些为争论提供仲裁的定理 (基模型的可定义性、地幔、脱殊绝对性) 机械化，就是字面意义上的奠基。

一切的出发点是**宿主语言最大化**：不逐字誊抄教科书的 ZF 公理、再围着它们扭曲证明助理，而是把每个概念都以类型论原生的语汇重构，于是宿主语言负责 *说话*，深嵌入的 `Formula` 只负责 *被研究*。这看上去恰像奠基的反面，但证明助理给出的是严格性而非还原式的基底，而严格性与元理论的强度无关；最大化恰恰使机器检验成为可能，其代价也被公开声明。

这份根基也是中立的：集合论地质学为单宇宙观与多宇宙观补上各自缺失的严格立足点，并把争论参数化为所假定的无穷公理的强度，因此本项目不站在任何一边。

完整论述见 [纲领](CHARTER.md)。

## 命名

*Bedrock (基岩)* 是最深的基模型；它是否存在，本身就是一个微妙的、对大基数敏感的问题 (Usuba 定理)。这个词亦取其寻常义：一项探究之下的根基。两重含义皆为本意。

## 作者声明

本项目的所有内容均由 AI 辅助完成，但每一行都经作者逐字审阅，本文档亦不例外。

## 依赖

本开发针对以下锁定的工具链进行类型检查：

| 组件 | 版本 |
| --- | --- |
| [Agda](https://github.com/agda/agda) | 2.8.0 |
| [cubical](https://github.com/agda/cubical) | 0.9 |
| [Python](https://www.python.org) | 3.11+ |

`make check` 与站点构建需 Python 3.11+；开发工具 (`reuse` 检查器) 固定在 [requirements-dev.txt](../../requirements-dev.txt) 中，并由 `make venv` 安装进本地虚拟环境 (每个克隆运行一次即可)。每次推送都会经 [GitHub Actions](../../.github/workflows/typecheck.yml) 针对上述版本进行类型检查。

## 贡献

AI agent 以 [AGENTS.md](../../AGENTS.md) 为准，人类贡献者请从 [CONTRIBUTING.md](../../CONTRIBUTING.md) 开始。

## 许可

Bedrock 采用多重许可；逐文件的条款在 [`REUSE.toml`](../../REUSE.toml) 中声明，并由 `reuse lint` 验证。简而言之：

- **数学开发与文稿** (`src/`、`docs/`、本 `README`) 以及品牌标识 (`site/static/favicon.svg`) 以 [CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/) 许可；其中的 Agda 开发被视作一份数学写作，而非传统软件。
- **所有第一方代码与配置** (工具链、站点前端、构建与开发文件) 以 [AGPL-3.0-only](https://www.gnu.org/licenses/agpl-3.0.html) 许可。这包括改编自 [1lab](https://1lab.dev) 的前端资源，以及 `site/vendor/1lab/` 下内嵌的 1lab 副本，在此仅以聚合方式组合。
- **自托管的网页字体** (`site/static/fonts/`) 为第三方资源，以 [OFL-1.1](https://openfontlicense.org) 许可。

完整许可文本见 [`LICENSES/`](../../LICENSES/)；第三方署名与 AGPL 第 13 条对应源代码声明见 [NOTICE](../../NOTICE)。

© 2026 choukh (choukyuhei@gmail.com)。