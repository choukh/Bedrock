{-# OPTIONS --cubical --safe --guardedness #-}
module HelloWorld where

open import Cubical.Foundations.Prelude

-- A minimal Cubical Agda "hello world": reflexivity gives a path from any
-- point to itself, checked by the same toolchain the CI uses.
hello : {ℓ : Level} {A : Type ℓ} (x : A) → x ≡ x
hello x = refl
