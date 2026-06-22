<p align="center"><img src="../../site/static/assets/banner.png" alt="" width="800"></p>

<h1><img src="../../site/static/assets/brand.svg" alt="" height="56" align="middle"> Bedrock</h1>

[English](../../README.md) · [中文](../zh/README.md) · **日本語**

[![Typecheck](https://github.com/BedrockInstitute/Bedrock/actions/workflows/typecheck.yml/badge.svg)](https://github.com/BedrockInstitute/Bedrock/actions/workflows/typecheck.yml)
![Status: early](https://img.shields.io/badge/status-early-orange)
[![Agda](https://img.shields.io/badge/Agda-2.8.0-blue)](https://github.com/agda/agda)
[![cubical](https://img.shields.io/badge/cubical-0.9-blue)](https://github.com/agda/cubical)
[![Content: CC BY-NC-SA 4.0](https://img.shields.io/badge/content-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)
[![Code: AGPL-3.0-only](https://img.shields.io/badge/code-AGPL--3.0--only-blue.svg)](https://www.gnu.org/licenses/agpl-3.0.html)
[![REUSE status](https://api.reuse.software/badge/github.com/BedrockInstitute/Bedrock)](https://api.reuse.software/info/github.com/BedrockInstitute/Bedrock)

*V の形而上学に礎を据える。*

[Cubical Agda](https://github.com/agda/cubical) における機械検証の開発であり、現代の集合宇宙をめぐる問いの背後にある集合論、すなわち強制法、内部モデル、そして V の構造を対象とする。

## 最初の目標

当面の最優先の目標は、次を完全に機械化することである。

> **`L` ⊨ GCH**。ここで `L` は、高次帰納型として実現された累積階層 `V` の上に構成される構成可能階層である。これはホストの内部における意味論的な定理である。

その内容はゲーデルの 1938 年の結果だが、辿る経路は教科書のものではなく、GCH に対して誰かがこれまで辿ったものでもない。これが最初の礎石としてふさわしいのは、本プロジェクトの残り全体が必要とする基盤層、すなわち深い埋め込みによる一階言語、累積階層、`L`、そして二重意味論の機構を、ことごとく動かすからである。しかも一行目から、下に述べるホスト言語最大主義の方針に立脚している。これを正しく仕上げることが、以後のすべてが立脚する基盤を較正する。

## 方向

この最初の礎石を越えて、長期的な目標は、機械化された集合論を、それが現在止まっている地点の先へと推し進めることにある。既存の強制法の形式化はコーエン (1963) で止まっているが、目標は今世紀の成果に到達することである。すなわち、多宇宙を研究するための道具としての強制法、基礎モデルの定義可能性、マントル、そして「V がそもそも確定した構造をもつのか」という、より大きな問いである。

これらは目標であって、約束ではない。いずれも、検証されて初めてここで宣言される。

## 基盤

本プロジェクトの目標は、V の形而上学に決着をつけることではなく、それに検証済みの礎を据えることにある。論争を裁定する定理 (基礎モデルの定義可能性、マントル、ジェネリック絶対性) を機械化することは、文字どおりの意味での基盤づくりにほかならない。

すべての出発点となるのが、**ホスト言語最大主義**である。教科書の ZF 公理を逐語的に書き写し、その周囲で証明支援系をねじ曲げるのではなく、あらゆる概念を型理論に固有の語法で再構成する。かくしてホスト言語が *語る* 側に立ち、深い埋め込みによる `Formula` は *研究される* 側に回るだけである。これは基盤づくりの逆に映るかもしれない。だが証明支援系が与えるのは厳密さであって還元的な基底ではなく、厳密さはメタ理論の強さに依存しない。最大主義こそが機械検証を可能にし、その代価もまた公然と表明される。

この礎は中立でもある。集合論の地質学は、単一宇宙観と多宇宙観のそれぞれが欠いてきた厳密な足場を両者に与え、論争を、仮定される無限公理の強さによってパラメータ化する。ゆえに本プロジェクトは、いずれの側にも与しない。

完全な論述は [綱領](CHARTER.md) にある。

## なぜ Cubical か

Cubical 型理論は現代型理論の最前線であり、いままさに書かれつつある数学の基礎である。一方、V の形而上学は同じ探究のうちで最も古典的な分野であり、「数学的宇宙とは何か」という最も古い問いである。最も古典的な基礎の問いを最も現代的な基礎へと持ち込むことは、しぶしぶ甘受すべき制約ではなく、むしろ本プロジェクトの目的の一つである。両者のあいだの対照は、意図して保たれている。

この選択は技術的にも引き合う。累積階層 V はここで高次帰納型として実現され、cubical はそれを、仮定として措くのではなく計算可能なものにする。だが、より深い理由は、その緊張そのものにある。

## 命名

*Bedrock (岩盤)* は最も深い基礎モデルである。それがそもそも存在するか否かは、それ自体が大基数に敏感な微妙な問題である (薄葉の定理)。この語はまた、ありふれた意味、すなわち探究の下にある土台、としても読める。両義はともに意図されている。

## 著者について

本プロジェクトのすべての内容は AI の補助のもとで作成されているが、その一行一行は、本文書も含めて、著者が一字一句、目を通している。

## 依存

本開発は、以下に固定したツールチェインに対して型検査される。

| コンポーネント | バージョン |
| --- | --- |
| [Agda](https://github.com/agda/agda) | 2.8.0 |
| [cubical](https://github.com/agda/cubical) | 0.9 |
| [Python](https://www.python.org) | 3.11+ |

`make check` とサイトのビルドは Python 3.11+ を必要とする。開発用ツール (`reuse` リンター) は [requirements-dev.txt](../../requirements-dev.txt) に固定され、`make venv` でローカルの仮想環境に導入される (クローンごとに一度実行すればよい)。プッシュのたびに、[GitHub Actions](../../.github/workflows/typecheck.yml) によって上記のバージョンに対して型検査される。

## 貢献

AI エージェントは [AGENTS.md](../../AGENTS.md) を、人間の貢献者は [CONTRIBUTING.md](../../CONTRIBUTING.md) を参照してください。

## ライセンス

Bedrock は複数ライセンスを採用しており、ファイルごとの条項は [`REUSE.toml`](../../REUSE.toml) に宣言され、`reuse lint` が検証する。要するに、

- **[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/)**：数学・文章・ブランドマーク (`src/`、`docs/`、`README`、`site/static/assets/`)。
- **[AGPL-3.0-only](https://www.gnu.org/licenses/agpl-3.0.html)**：その他すべてのプロジェクト自身のコードと構成 (取り込んだ [1lab](https://1lab.dev) フロントエンドを含む)。
- **[OFL-1.1](https://openfontlicense.org)**：自己ホストのウェブフォント (`site/static/fonts/`)。

完全なライセンス本文は [`LICENSES/`](../../LICENSES/) にある。第三者のクレジットと AGPL 第 13 条の対応ソース表明は [NOTICE](../../NOTICE) を参照。

© 2026 Bedrock Institute。
