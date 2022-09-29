(* REMETTER Emilie *)
(** Devoir Maison **)

Require Import Nat Arith Omega Psatz.
Import Nat.
Require Import List.
Import ListNotations.

Module Type POW_NAT.

  Definition N := nat.
  Definition E := list bool.
  Definition incrN : N -> N := S.
  Parameter incrE : E -> E.
  Parameter pow_fast : N -> E -> N.
  Definition pow : N -> N -> N := Nat.pow.
  Parameter encode : N -> E.
  Parameter decode : E -> N.
  
  Axiom dec_enc : forall n, decode (encode n) = n.
  Axiom incr_encode : forall n, incrE (encode n) = encode (incrN n).
  Axiom decode_incr : forall e, decode (incrE e) = incrN (decode e).
  Axiom pow_eq : forall e n, pow_fast n e = pow n (decode e).
End POW_NAT.
 
Print Nat.pow.

Module pow_nat <: POW_NAT.
  Definition N := nat.
  Definition E := list bool.
  Definition incrN : N -> N := S.
  Definition pow := Nat.pow.
  Fixpoint decode (l : list bool) : nat := match l with
    | [] => 0
    | head::tail => if head then 1+2*(decode tail) else 0+2*(decode tail)
  end.
  Fixpoint incrE (l : list bool) : list bool := match l with
    | [] => [true]
    | head::tail => if head then [false]++(incrE tail) else [true]++tail
  end.
  Fixpoint encode (n : nat) : list bool := match n with
    | 0 => nil
    | S p => incrE (encode p)
  end.

  Lemma encode_m2 : forall n, n <> 0 -> encode (n + n) = false::encode n.
  Proof.
  Admitted.
  
  
  Lemma decode_incr (l : list bool): decode (incrE l) = incrN (decode l).
  Proof.
  Admitted.
  
  Lemma incr_encode n : incrE (encode n) = encode (S n).
  Proof.
  Admitted.
  
  Theorem dec_enc : forall n, decode (encode n) = n.
  Proof.
  Admitted.

  Fixpoint pow_fast (b : nat) (e : list bool) : nat := match e   with
    | []  => 1
    | head::tail  => if even (decode e) then pow_fast (b*b) tail
                  else b * (pow_fast (b*b) tail)
    end.
  

  Lemma pow_eq : forall e n, pow_fast n e = n ^ (decode e).
  Proof.
  Admitted.
  
End pow_nat.
