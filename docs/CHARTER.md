# Bedrock — Charter

**English** · [中文](./CHARTER.zh.md)

The full methodological and philosophical commitments behind Bedrock. The
[README](../README.md) condenses these into a single *Groundwork* section and
links here for the complete treatment, preserved below in three parts.

## Approach

The host is Cubical Agda; classical principles (LEM, AC) are explicit module
parameters, not global assumptions, so the constructive/classical boundary stays
visible.

The one choice everything else follows from is **host-language maximalism**. We
do **not** transcribe the textbook ZF axioms verbatim and then bend the proof
assistant around them, the route by which a textbook formalisation, under
foundational constraints, is forced into detours and workarounds. Instead **every
notion is reconstructed in type-theory-native idiom**, stated directly in Cubical
Agda's own computational language, taking the host's benefits in full rather than
hobbling the development for "formal purity":

- unique existence is `isContr`, so the definite-description operator `℩` is a
  *projection* rather than an axiom, and the description axiom dissolves;
- extensional characterisations are path equalities, so propositional
  extensionality is a *theorem*; structure transport is underwritten by the SIP;
  adequacy is a literal `≡`;
- Regularity is the meta-level `WellFounded`, and Infinity makes a ZF-set
  *reflect* the meta-level inductive `Nat`, so that the ZF axiomatised in the host
  admits only **standard models** (no non-standard ω, no infinite descent);
- satisfaction is structural recursion on the host inductive `Formula`, so the
  Tarski equations hold **by computation (`refl`)**, with no arithmetised syntax
  (Gödel numbering, β-function coding) and nothing to prove;
- the constructible hierarchy is not arithmetised into Δ₀ formulas (Jech §13, the
  sharpest wall); instead `L` is an **inductive predicate**.

This is why the deeply embedded `Formula` is *not* an expressive device: the host
language is strictly more expressive, and `Formula` appears only where first-order
definability is itself the object of study (bridged to host predicates by
reflection-driven *reification*). The host language does the *speaking*; `Formula`
is what gets *studied*.

## Groundwork

The aim is not to settle the metaphysics of V, but to lay verified groundwork on
which its questions can be studied in a proof assistant. The theorems that inform
the debate, such as the definability of grounds, the mantle, and generic
absoluteness, are the field's arbitration infrastructure, and mechanizing them is
groundwork in the literal sense.

The word can mislead. To "ground" mathematics often means reducing it to the most
austere base one can bear, in the manner of finitism or PRA, so by that standard
host-language maximalism looks like the opposite. But a proof assistant offers
rigor, not reductive security, and rigor is independent of the strength of the
metatheory. A proof is no less gap-free in Cubical Agda than in PRA. The host's
strength changes only what is assumed, not whether the derivation is verified.
Retreating to a minimal base would buy proof-theoretic reduction, which this
project has no reason to pay for and which would not make the mathematics any
better checked. Maximalism is in fact what makes the checking attainable. The
metaphysics of V needs a metatheory rich enough to express V's own structure, and
an austere base only forces the encoding detours that are themselves a source of
error. Working in the host's native idiom keeps the formalization close to the
mathematics, and the metatheoretic cost is declared openly. Mechanizing these
theorems is itself the groundwork, putting the metaphysics of V on machine-checked
ground.

## Neutral ground

The metaphysics of V is contested. Universism holds that V is a single determinate
universe, in which CH has a truth value that the independence results merely fail
to settle. Multiversism holds that forcing extensions, ground models, and
ultrapowers are all equally real, and that CH simply varies across them. Each
position has long carried a methodological weakness: the first lacks a testable
mathematical form for its conviction that V has a determinate deep structure, and
the second lacks mathematical legitimacy for its central object, the multiverse of
all forcing extensions, which can look like informal metatheory.

Set-theoretic geology repairs both, with one body of ZFC theorems. Ground-model
definability shows that all grounds are uniformly definable inside V, so the
multiverse is no longer mere metatheoretic talk about it but a definable,
quantifiable structure in the language of ZFC, which is the legitimacy
multiversism needs. The same
theorems hand universism a falsifiable instrument: a candidate axiom for the
"true" V can be tested against its geological consequences, and a universe that
claims to be canonical but is geologically pathological is ruled out. What the
theorems really do is parameterise the dispute. How rigid the universe's structure
is depends on how strong an axiom of infinity one assumes, and the argument moves
from rhetoric to the choice of axioms.

So this project takes no side. It mechanizes theorems that presuppose neither
position and serve both. That is the sense in which it is bedrock: not a stance in
the debate, but neutral ground beneath it, on which either camp can build.

---

← Back to [README](../README.md)
