(* TP3 *)
(* REMETTER Emilie *)


open List ;; 

(* FONCTIONS SUR LA STRUCTURE DU GRAPHE *)
(* Teste si deux sommets sont adjacents *)
let rec adjacent graphe sommet1 sommet2 = 
  (List.exists(function e -> e = (sommet1, sommet2) || e = (sommet2, sommet1)) graphe);;

(* Liste les sommets d'un graphe *)
let listeSommets graphe = 
  sort_uniq (compare) (match split graphe with x, y -> x@y);;

(* Liste des voisins d'un sommet d'un graphe *)
let voisins graphe sommet =
  (sort_uniq (compare) (filter (adjacent graphe sommet) (listeSommets graphe)));;

(* Calcule le nombre de voisins *)
let nbVoisins graphe sommet = length (voisins graphe sommet);;

(* Renvoie la couleur *)
let rec getCouleur element liste = match liste with
  | [] -> failwith "vide"
  | (sommet, couleur)::reste -> if sommet = element then couleur else getCouleur element reste;; 

let listeCouleur graphe sommet liste = match liste with
  | [] -> [];
  | _ -> match split (filter (fun a -> mem (fst a) (voisins graphe sommet)) liste) with
      (_,couleur) -> couleur;;


(* Renvoie le nombre minimal de couleur *)
let minCouleur listeC = 
  let rec minBis maximum liste = match liste with
    | [] -> maximum
    | tete::reste -> match (tete = maximum) with
      |true -> (minBis (maximum + 1) reste)
      |false -> maximum
  in (minBis 1 ((sort_uniq (fun a b -> a-b) listeC)));;

(* ALGORITHMES GLOUTONS *)
let gloutonSansH graphe = 
  let rec gloutonBis g cmax colored liste = match g with
    |  [] -> (colored, cmax, List.rev liste) 
    | tete::reste -> if ((minCouleur (listeCouleur graphe tete colored) ) > cmax) then
          gloutonBis reste (minCouleur (listeCouleur graphe tete colored)) ((tete, minCouleur (listeCouleur graphe tete colored))::colored) (tete::liste)
        else gloutonBis reste cmax ((tete, minCouleur (listeCouleur graphe tete colored))::colored) (tete::liste);
  in gloutonBis (listeSommets graphe) 1 [] [];;


(* Ordonne sommet par degres *)
let ordonneDeg graphe = match List.split graphe with
  |(x, y) -> sort (fun elementY elementX -> (nbVoisins graphe elementX) - (nbVoisins graphe elementY)) (sort_uniq compare (List.merge (fun elementX elementY -> (nbVoisins graphe elementX) -(nbVoisins graphe elementY)) x y));;

  
let gloutonDeg graphe = 
  let rec gloutonBis g cmax colored liste = match g with
    | [] -> (colored, cmax, rev liste)
    | tete::reste -> if ((minCouleur (listeCouleur graphe tete colored) ) > cmax) then
          gloutonBis reste (minCouleur (listeCouleur graphe tete colored)) ((tete, minCouleur (listeCouleur graphe tete colored))::colored) (tete::liste)
        else gloutonBis reste cmax ((tete, minCouleur (listeCouleur graphe tete colored))::colored) (tete::liste);
  in gloutonBis (ordonneDeg graphe) 1 [] [];;

(* TP4 CSP *)
let rec print_list = function 
    [] -> ()
  | e::l -> print_int e ; print_string " " ; print_list l;; 

let rec consListCoul min p =
  if min > p then [] else min :: consListCoul (min+1) p;;

let rec exist elem l = match l with
  | [] -> false
  |e::sl -> (e=elem) || exist elem sl;;

let enum_couleurs sommet graphe sommetsColo couleurs = 
  let rec aux = function
    | [] -> []
    | c :: tail -> if exist c (listeCouleur graphe sommet sommetsColo)
        then (aux tail)
        else (sommet,c) :: (aux tail)
  in aux couleurs;;

let rec enumValeurs sommet mini maxi =
  if (mini > maxi) then []
  else
    (sommet,mini) :: (enumValeurs sommet (mini+1) maxi);;

let backtrack graphe p =
  let sommets = listeSommets graphe in 
  let nbAffect = 0 in
  let nbBacktrack = 0 
  in if sommets = [] then ([],nbAffect,nbBacktrack) else
    let rec backtrack_rec sommetsTmp cmax sommetsColo affectation = 
      match sommetsTmp with
      | [] -> ([],affectation,nbBacktrack)
      | s :: tail -> 
          let listeCouleurs = enumValeurs s 1 cmax in 
          let listeCouleursPoss = enum_couleurs s graphe sommetsColo (consListCoul 1 cmax) in 
          let rec aux affectation = function
            | [] -> (sommetsColo,affectation,nbBacktrack)
            | (s,c) :: tail2 -> print_int s; print_int c; 
                if exist (s,c) listeCouleursPoss 
                then let (somc,nba,nbt) = backtrack_rec tail cmax ((s,c)::sommetsColo) (affectation+1)
                  in if somc <> [] then (print_string "x"; aux (affectation+1) tail2)
                  else (somc,nba,nbt)
                else aux (affectation+1) tail2
          in (print_newline(); aux affectation listeCouleurs)
    in backtrack_rec sommets p [] nbAffect;;
