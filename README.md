# Bedrock

**English** · [中文](./README.zh.md)

[![Typecheck](https://github.com/choukh/Bedrock/actions/workflows/typecheck.yml/badge.svg)](https://github.com/choukh/Bedrock/actions/workflows/typecheck.yml)
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

The host is Cubical Agda; classical principles (LEM, AC) are explicit module
parameters, not global assumptions, so the constructive/classical boundary stays
visible. Beyond that, the aim is not to settle the metaphysics of V, but to lay
verified groundwork on which its questions can be studied in a proof assistant.
The theorems that arbitrate the debate, such as ground-model definability, the
mantle, and generic absoluteness, are the field's arbitration infrastructure, and
mechanizing them is groundwork in the literal sense.

The one methodological choice everything follows from is **host-language
maximalism**: rather than transcribing the textbook ZF axioms and bending the
proof assistant around them, every notion is reconstructed in type-theory-native
idiom. Unique existence is `isContr` (so `℩` is a projection, not an axiom);
extensional characterisations are path equalities; Regularity is the meta-level
`WellFounded` and Infinity makes a ZF-set reflect `Nat`, admitting only standard
models; satisfaction is structural recursion on `Formula`, so the Tarski equations
hold by computation; `L` is an inductive predicate, not an arithmetised Δ₀ formula.
The host does the *speaking*; the deep-embedded `Formula` is what gets *studied*.
This can look like the opposite of grounding, which usually means retreating to an
austere base. But a proof assistant offers rigor, not reductive security, and
rigor is independent of the metatheory's strength. Maximalism is in fact what makes
the checking attainable: the metaphysics of V needs a metatheory rich enough to
express V's own structure, and the metatheoretic cost is declared openly.

The groundwork is also neutral. The metaphysics of V is contested: universism
holds V is a single determinate universe, while multiversism holds forcing
extensions, grounds, and ultrapowers are equally real. Each side has carried a
methodological weakness. Set-theoretic geology repairs both with one body of ZFC
theorems, making the multiverse a definable, quantifiable structure (the legitimacy
multiversism needs) while handing universism a falsifiable instrument, and
parameterising the dispute by the strength of the infinity axiom assumed. This
project takes no side: it mechanizes theorems that presuppose neither position and
serve both. That is the sense in which it is bedrock: neutral ground beneath the
debate, on which either camp can build.

The full treatment, covering the bullet-by-bullet rationale, the defense of
maximalism, and the geology positioning, is in the [Charter](docs/CHARTER.md).

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