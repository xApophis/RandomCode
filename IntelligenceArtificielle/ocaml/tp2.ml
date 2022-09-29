(* GODINO PIERRE TDA5.1 *)
(* Programme TP2*)
open List;;


 (* MINIMAX *)

 let minL liste = match liste with
      |[] -> failwith "Liste vide"
      |e::resteListe -> fold_left min e resteListe;;

let maxL liste = match liste with
     |[] -> failwith "Liste vide"
     |e::resteListe -> fold_left max e resteListe;;

let longueur liste = length liste;;

let pair elem = match (elem mod 2) with
  |0 -> true
  |_ -> false;;



let rec minimax etatCourant p etatsFils evaluation =
  let possibilites = map snd (etatsFils etatCourant) in
  let minimaxBis = match longueur possibilites with
    |0 -> evaluation etatCourant
    |_ -> match pair p with
            |true -> maxL (map (function e -> minimax e (p + 1) etatsFils evaluation) possibilites)
            |false -> minL (map (function e -> minimax e (p + 1) etatsFils evaluation) possibilites)
  in minimaxBis;;


(* RECHERCHE *)

    let recherche pMax etatCourant p etatsFils evaluation =
    let rec minimax etatCourant p etatsFils evaluation =
    let possibilites = map snd (etatsFils etatCourant) in
    match ((longueur possibilites = 0) || (p = pMax)) with
      |true -> evaluation etatCourant
      |false -> match pair p with
              |true -> maxL (map (function e -> minimax e (p + 1) etatsFils evaluation) possibilites)
              |false -> minL (map (function e -> minimax e (p + 1) etatsFils evaluation) possibilites)
    in minimax etatCourant 0 etatsFils evaluation;;

    (* Pour pouvoir demarrer directement a la profondeur 1, pour meilleur coup par exemple *)
    let recherchep1 pMax etatCourant p etatsFils evaluation =
    let rec minimax etatCourant p etatsFils evaluation =
    let possibilites = map snd (etatsFils etatCourant) in
    match ((longueur possibilites = 0) || (p = pMax)) with
      |true -> evaluation etatCourant
      |false -> match pair p with
              |true -> maxL (map (function e -> minimax e (p + 1) etatsFils evaluation) possibilites)
              |false -> minL (map (function e -> minimax e (p + 1) etatsFils evaluation) possibilites)
    in minimax etatCourant 1 etatsFils evaluation;;


(* MEILLEUR COUP *)

let maxC c1 c2 = match (fst c1) > (fst c2) with
  |true -> c1
  |false -> c2;;

let rec maxLC liste = match liste with
  |[] -> failwith "La liste de couples est vide"
  |[c] -> c
  |tete::reste -> maxC (maxLC reste) tete;;

let rec resFils liste listeCouplesFils = match liste with
  |[] -> []
  |tete::reste -> (tete, fst (hd listeCouplesFils))::(resFils reste (tl listeCouplesFils));;



let meilleurCoup pMax etatInitial p etatsFils evaluation =
  let filsEtatInitial = map snd (etatsFils etatInitial) in
  let listeValeurs = (map (function e -> recherchep1 pMax e p etatsFils evaluation) filsEtatInitial) in
  let listeResultatsFils = resFils listeValeurs (etatsFils etatInitial)
  in maxLC listeResultatsFils;;

let meilleurCoup profondeurMax etatInitial profondeur etatFils evaluation = 
    let filsEtatInitial = map snd (etatFils evaluation) in
    let listeValeurs = map(function e -> recherche profondeurMax e profondeur etatFils evaluation) filsEtatInitial in
    let listeResultatsFils = resFils listeValeurs (etatFils etatInitial)
    in maxList listeResultatsFils;;
