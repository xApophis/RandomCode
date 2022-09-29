open List;;

let sommetAdj graphe s1 s2 =
  (List.exists(function e -> e = (s1, s2) || e = (s2, s1)) graphe);;

let grapheListe graphe =
  List.sort_uniq (String.compare) (match List.split graphe with v1, v2 -> v1@v2);;

let voisins graphe sommet =
  (List.sort_uniq (String.compare) (List.filter (sommetAdj graphe sommet) (grapheListe graphe)));;

let sommetsL graphe =
  (List.sort_uniq compare (fst (List.split graphe) @ (snd (List.split graphe))));;

let min color =
  let rec minBis maximum liste = match liste with
    | [] -> maximum
    | tete::reste -> match (tete = maximum) with
                     |true -> (minBis (maximum + 1) reste)
                     |false -> maximum
  in (minBis 1 ((List.sort_uniq (fun a b -> a-b) color)));;

let rec getCouleur elem liste = match liste with
  | [] -> failwith "vide"
  | (sommet, couleur)::reste -> match (sommet = elem) with
                                |true -> couleur
                                |false -> (getCouleur elem reste);;


let rec contents elem liste = match liste with
  | [] -> false
  | (sommet, couleur)::reste -> match (sommet = elem) with
                                |true -> true
                                |false -> (contents elem reste);;


let colorL graphe colorPartielle sommet =
  let rec colorLBis liste = match liste with
    | [] -> []
    | tete::reste -> match (contents tete colorPartielle) with
                        |true -> (getCouleur tete colorPartielle)::(colorLBis reste)
                        |false -> (colorLBis reste)
     in (List.sort_uniq compare (colorLBis (voisins graphe sommet)));;


let ordre color =
  let rec ordreBis liste = match liste with
    | [] -> []
    | (sommet,couleur)::reste -> sommet::(ordreBis reste) in (List.rev (ordreBis color));;

let nbColor color =
  let rec nbColorBis liste = match liste with
    | [] -> []
    | (sommet, couleur)::reste -> couleur::(nbColorBis reste) in (List.length ((List.sort_uniq (fun a b -> a - b) (nbColorBis color))));;

let gloutonSansH graphe = let final = [] in
  let rec gloutonSansHBis color liste = match liste with
    | [] -> (color, (nbColor color), (ordre color))
    | tete::reste -> (gloutonSansHBis ((tete, min (colorL graphe color tete))::color) reste) in (gloutonSansHBis final (sommetsL graphe));;

(* tests *)

(*****************************************************************************)
(* Des graphes : *************************************************************)
(*****************************************************************************)

(* Un petit graphe en extension : *)

let g1 = ["WA","NA" ; "WA","SA" ; "NA","SA" ; "NA","Q" ; "SA","Q" ; "SA","V" ; "SA","NSW" ; "Q","NSW" ; "NSW","V" ]


(* Un autre petit graphe pour vérifier le retour arrière *)

let g2 = ["A","B" ; "A","E" ; "B","C" ; "B","D" ; "B","E" ; "C","D" ; "D","E"]

(* Construction à partir d'un fichier au format "DIMACS standard" - décommenter les 4 dernières lignes *)

let rec split s = try let i = String.index_from s 0 ' '
	in (String.sub s 0 i)::(split (String.sub s (i+1) ((String.length s )-(i+1))))
	with Not_found -> [s]

let lire_graphe (nom_fichier : string) : ('a * 'a) list =
(* retourne la liste des arêtes *)
	let ref_l_aretes = ref [] and flux = open_in nom_fichier
	in try
		while true; do match (split (input_line flux)) with
			  "e"::x::y::[] -> ref_l_aretes := (int_of_string x, int_of_string y)::!ref_l_aretes
			| _ -> ()
  		done ; !ref_l_aretes
		with End_of_file -> close_in flux ; !ref_l_aretes



let myciel3 = lire_graphe "myciel3.col";; (* 11 sommets *)
let myciel4 = lire_graphe "myciel4.col";; (* 23 sommets , 5 couleurs *)
let myciel5 = lire_graphe "myciel5.col";; (* 47 sommets *)
let miles750 = lire_graphe "miles750.col";; (* 128 sommets *)

                gloutonSansH myciel3;;

