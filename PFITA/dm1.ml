let nom = "REMETTER" and prenom = "Emilie"

(* Fonction donnée dans l'énoncé *)
let string_of_chars l = String.init (List.length l) (List.nth l)

(* Q1 *) 
let rec map_range f n =
  if n<=0 then [] else map_range f (n-1) @ [f n];;
                                                             
(* Q2 *)
let chars_of_string chaine = 
  let taille = String.length chaine in 
  let rec constructionListe string longueur = 
    match longueur with 
      0     -> []
    | autre -> constructionListe string (longueur - 1) 
               @ [(String.get string (autre-1))];
  in constructionListe chaine taille;;

(* Q3 *)
let rec normalize = function 
    [] -> []
  | tete :: reste -> match tete with
      'a'..'z' -> Char.uppercase_ascii tete :: normalize reste
    | 'A'..'Z' -> tete :: normalize reste
    | _        -> normalize reste;;

(* Q4 *)
let rec insert element liste = match liste with
    [] -> [(element, 1)]
  | (valeur, nb_occs) :: reste -> 
      if valeur = element then (valeur, nb_occs + 1) :: reste
      else (valeur, nb_occs) :: insert element reste;;
  
(* Q5 *)
let rec occurrences = function
    [] -> []
  | tete :: reste -> insert tete(occurrences reste);;

(* Q6 *)
let max2 x y  = if x > y then x else y;; 
let rec kmax liste = match liste with 
    (element, poids) :: reste -> max2 poids (kmax reste) 
  | _ -> failwith "Erreur : liste vide";;

(* Q7 *)
let rec cesar enc key message = match message with
    [] -> []
  | tete :: reste -> enc tete key :: cesar enc key reste;;

(* Q8 *)
let encode key c = 
  Char.chr((((Char.code key - Char.code 'A') + (Char.code c - Char.code 'A')) mod 26) + Char.code 'A');;

(* Q9 *)
let cesar_encode key message = 
  string_of_chars(cesar encode key (normalize (chars_of_string message)));;
 
