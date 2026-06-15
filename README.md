# Bedrock

**English** · [中文](docs/zh/README.md) · [日本語](docs/ja/README.md)

[![Typecheck](https://github.com/choukh/Bedrock/actions/workflows/typecheck.yml/badge.svg)](https://github.com/choukh/Bedrock/actions/workflows/typecheck.yml)
![Status: early](https://img.shields.io/badge/status-early-orange)
[![Agda](https://img.shields.io/badge/Agda-2.8.0-blue)](https://github.com/agda/agda)
[![cubical](https://img.shields.io/badge/cubical-0.9-blue)](https://github.com/agda/cubical)
[![License: CC BY-NC-SA 4.0](https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by-nc-sa/4.0/)

*Laying the groundwork for the metaphysics of V.*

A machine-checked development, in [Cubical Agda](https://github.com/agda/cubical),
of the set theory underlying contemporary questions about the universe of sets:
forcing, inner models, and the structure of V.

## First goal

The immediate, self-contained target is a full mechanization of

> **`L` ⊨ GCH**, where `L` is the constructible hierarchy built over the
> cumulative hierarchy `V` realised as a higher inductive type. This is a semantic
> theorem internal to the host.

The content is Gödel's 1938 result, but the route is not the textbook one, and not
one anyone has taken for GCH. It is the right first stone because it exercises the
entire base layer the rest of the project needs: a deeply embedded first-order
language, the cumulative hierarchy, `L`, and the dual-semantics machinery. And it
commits from line one to the host-language-maximalist approach described below.
Getting it right calibrates the infrastructure everything else will stand on.

## Direction

Beyond that first stone, the long-term aim is to push mechanized set theory past
where it currently stops. Existing forcing formalizations end at Cohen (1963); the
goal is to reach results from this century: forcing as a tool for studying the
multiverse, the definability of ground models, the mantle, and the broader
question of whether V has a determinate structure at all.

These are goals, not promises. Each will be claimed here only when it is checked.

## Groundwork

The aim is not to settle the metaphysics of V but to lay verified groundwork for
it: mechanizing the theorems that arbitrate the debate, such as ground-model
definability, the mantle, and generic absoluteness, is groundwork in the literal
sense.

The one choice everything follows from is **host-language maximalism**: rather than
transcribing the textbook ZF axioms and bending the proof assistant around them,
every notion is reconstructed in type-theory-native idiom, so the host does the
*speaking* and the deep-embedded `Formula` is what gets *studied*. This can look
like the opposite of grounding, but a proof assistant offers rigor, not a reductive
base, and rigor is independent of the metatheory's strength; maximalism is what
makes the checking attainable, and its cost is declared openly.

The groundwork is also neutral: set-theoretic geology gives both universism and
multiversism the rigorous footing each has lacked, and parameterises the dispute by
the strength of the infinity axiom assumed, so the project takes no side.

The full treatment is in the [Charter](docs/en/CHARTER.md).

## Name

*Bedrock* is the deepest ground model; whether one exists at all is a delicate,
large-cardinal-sensitive question (Usuba's theorem). The name also reads in the
ordinary sense: the groundwork beneath an inquiry. Both meanings are intended.

## Authorship

Everything in this project is produced with AI assistance, and every line of it,
this document included, is reviewed word by word by the author.

## Dependencies

The development typechecks against the following pinned toolchain:

| Component | Version |
| --- | --- |
| [Agda](https://github.com/agda/agda) | 2.8.0 |
| [cubical](https://github.com/agda/cubical) | 0.9 |

Every push is typechecked against these versions by
[GitHub Actions](.github/workflows/typecheck.yml).

## License

The entire repository, source and prose alike, is licensed under
[CC BY-NC-SA 4.0](https://creativecommons.org/licenses/by-nc-sa/4.0/).
The Agda development is treated as a piece of mathematical writing rather than
conventional software, and licensed accordingly.

© 2026 choukh (choukyuhei@gmail.com). You may share and adapt this work for
non-commercial purposes, provided you give appropriate credit and license your
derivatives under the same terms.