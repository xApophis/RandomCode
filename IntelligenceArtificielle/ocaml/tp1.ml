(* Ce fichier contient des graphes sur lesquels tester un        *)
(* algorithme de recherche dans un graphe d'etat                 *)

(*imprime une liste *) 
let rec print_list_string l=match l with  
    [] - print_string .  
  xreste - print_string ( ^x); print_list_string reste;; 

(* GRAPHES SANS COUTS ===========================================*)

(* Description du graphe G1 de l'enonce sans couts --------------*)

let initG1 = A ;;
let estButG1 = (function H - true  I - true  _ - false) ;;
let etatsSuivantsG1 = (function
      A - [C;B] 
     B - [D;E] 
     C - [F;D] 
     D - [I]
     E - [I]
     F - [G;H;I] 
      _ - [] );;

(* Description du graphe G2 ------------------------------------*)
(* Ce graphe permet de tester le fonctionnement de la recherche
   en largeur d'abord. En largeur on
   trouve le but H. En profondeur on trouve le but I.
*)

let initG2 = A ;;
let estButG2 = (function HI - true  _ - false) ;;
let etatsSuivantsG2 = (function
      A - [C;B;H] 
     B - [D;E] 
     C - [F;D] 
     D - [I]
     E - [H]
     F - [G;I] 
      _ - [] );;



(* Description du graphe G3 ------------------------------------*)
(* G3 permet de tester la gestion des cycles  c'est le graphe G1
   dans lequel H n'est pas un but. Il y a une boucle entre F et H.
   I est le seul but. Sans liste Vus, la recherche en largeur trouve le but, mais la recherche en profondeur boucle.
*)

let initG3 = A ;;
let estButG3 = (function I - true  _ - false) ;;
let etatsSuivantsG3 = (function
      A - [C;B] 
     B - [D;E] 
     C - [F;D] 
     D - [I]
     E - [I]
     F - [G;H] 
     H - [F] 
     _ - [] );;


(* GRAPHES AVEC COUTS ===========================================*)

(* Description du graphe G1 de l'enonce avec couts --------------*)
(* sans optimisation de la file d'attente, elle contient deux fois I en fin de recherche et le sommet D alors qu'on l'a deja developpe avec un cout inferieur*)
let initG1C = A ;;
let estButG1C = (function H - true  I - true  _ - false) ;;
let opPossG1C = (function
      A - [('n',3,C);('e',4,B)] 
     B - [('s',7,D);('e',4,E)] 
     C - [('n',9,F);('o',2,D)] 
     D - [('e',6,I)]
     E - [('s',4,I)]
     F - [('e',7,G);('n',9,H);('o',7,I)] 
      _ - [] );;
let hEtatG1C = (function
      A - 7
     B - 3	
     C - 5
     D - 2
     E - 2
     F - 2
     G - 100
      _ - 0 );;

(* Description du graphe G4 ------------------------------------*)
(* G4 permet de tester la gestion de la liste attente  l'etat C
   est mis en attente comme fils de a, associe a un cout de 10,
   mais en traitant le premier fils de A, qui est B, on rencontre
   a nouveau C associe cette fois-ci a un cout de 6. 
*)

let initG4 = A;;
let estButG4 =(function F - true  _ - false);;
let opPossG4 =(function
      A - [('h',4,B);('b',10,C)]
     B - [('b',2,C);('h',4,D)]
     C - [('b',6,F)]
     D - [('b',2,C)]
      _ - [] );;
let  hEtatG4 = (function
      A - 8
     B - 3
     C - 2
     D - 5
      _ - 0 );;

(* Description du graphe G5 ------------------------------------*)
(* G5 permet de tester la gestion des cycles  c'est une boucle a
deux noeuds sans etat-but. L'algo doit stopper en signalant
  qu'il n'y a pas de solution. Il faut utiliser une liste Vus.
*)

let initG5 = A ;;
let  estButG5 = (function _ - false) ;;
let  opPossG5 = (function
      A - [('n',2,B)]
     B - [('s',3,A)]
      _ - [] );;
let  hEtatG5 = (function
      A - 4
     B - 3
      _ - 0 );;

(* Description du graphe G6 ------------------------------------*)
(* G6 permet de tester la gestion de la liste vus, D deja vu avec une valeur superieure repasse en file d'attente.
*)

let initG6= A ;;
let  estButG6 = (function F - true  _ - false) ;;
let  opPossG6 = (function
      A - [('n',4,B);('s',7,C)]
     B - [('o',6,D);('e',20,F)]
     C - [('o',4,E);('s',4,D)]
     D - [('o',11,F)]
     E - [('o',12,F)]
      _ - [] );;
let  hEtatG6 = (function
      A - 18
     B - 16
     C - 12
     D - 8
     E - 10
      _ -0 );;

(* RECHERCHE EN LARGEUR, PUIS PROFONDEUR *)
(* largeur *)
let rec largeur attente estBut etatsSuivants = match attente with 
    []- failwith pas de but trouve 
   xreste - if (estBut x) then 
        (print_string file d’attente;print_list_string attente;
         print_newline ();x)
      else (print_string file d’attente;print_list_string attente;
            print_newline ();
            largeur (reste@(etatsSuivants x)) estBut etatsSuivants);;

        
(* profondeur *)
let rec profondeur attente estBut etatsSuivants = match attente with 
    []- failwith pas de but trouve 
   xreste - if (estBut x) then 
        (print_string file d’attente;print_list_string attente;
         print_newline ();x)
      else (print_string file d’attente;print_list_string attente;
            print_newline ();
            profondeur ((etatsSuivants x)@reste) estBut etatsSuivants);;

(* ALGORITHME DE TYPE A *) 

let creerLesFils etat coutGraph opPoss hEtat = 
  let rec creerUnFils coutGraph hEtat (_, g, etat) =
    (etat, coutGraph+g,hEtat etat)
  in List.map ( creerUnFils coutGraph hEtat) (opPoss etat);;

let insererLesFils lFils attente = 
  let rec filsTrier liste (nom, g, h) =
    match liste with
     [] - [(nom, g, h)]
     (a, b, c)  reste - if g+h  b+c then (nom, g, h)  (a, b, c)  reste 
        else (a, b, c)  (filsTrier reste (nom, g, h))
  in (List.fold_left filsTrier lFils attente);;

let rec afficherAttente = function 
  |[] - print_string(" .");  
  |(e, g, h)  reste -> print_string e ; print_string   ; afficherAttente reste;; 

let getCout (_,g,_) = g;;
let getEtat (etat,_,_) = etat;;


let afficherElement etatCourant listeAttente =
  print_string (" Element courant ");
  print_string (getEtat etatCourant);
  print_newline ();
  print_string (" File d'attente ");
  afficherAttente listeAttente;
  print_newline ();;

let print_etatBut etat = 
  print_string ("Etat but : "^getEtat etat);
  print_string ("Cout : "^getCout etat);
  print_newline ();;

let rec print_list l = match l with  
 | [] -> print_string " _" 
 | (x, y, z)::reste -> print_string "("; print_string (x); 
                      print_string ";"; print_int (y); 
                      print_string ";"; print_int (z); 
                      print_string ")"; 
                      print_list reste;;  

(*let aEtoile init opPoss hEtat estBut =
   let rec boucle etatCourant attente = 
     afficherElement etatCourant attente;
     if (estBut (getEtat etatCourant)) 
     then etatCourant
     else 
       match (insererLesFils (creerLesFils (getEtat etatCourant) (getCout etatCourant) opPoss hEtat) attente) with
        [] - failwith pas de but trouve
        premier  reste - boucle premier reste
   in boucle (init,0,(hEtat init)) [];;*)

let rec aEtoile l_attente estBut opPoss hEtat = match l_attente with
    | [] - failwith pas de but trouve
    | (etat, g, h)  tail - if estBut etat 
      then print_etatBut (etat,g,h)
      else (print_string ("En attente : "); print_list l_attente; print_newline ();
            aEtoile (insererLesFils (creerLesFils etat g opPoss hEtat) tail) estBut opPoss hEtat);;
  
(* AUTONOMIE *)
(*
  let getEtatBis (etat,_,_,_) = etat;;
  let getCoutBis (_,g,_,_) = g;;
  let getL (_,_,_,l) = l;;


  let creerLesFilsBis etat coutGraph opPoss hEtat l = 
    let rec creerUnFilsBis coutGraph hEtat l (n, g, etat) = 
      (etat, coutGraph+g,hEtat etat,l @ [n])
    in List.map ( creerUnFilsBis coutGraph hEtat l) (opPoss etat);;


  let insererLesFilsBis lFils attente =
    let rec filsTrierBis l (s,g,h,l1) =
      match l with
       [] - [(s,g,h,l1)]
       (a,b,c,d)  reste - if g+h  b+c then (s,g,h,l1)  (a,b,c,d)  reste 
          else (a,b,c,d)  (filsTrierBis reste (s,g,h,l1)) 
    in List.fold_left filsTrierBis lFils attente;;

  let rec afficherAttenteBis = function 
    [] - print_string .  
    (e,g,h,l)  reste - print_string e ; print_string   ; afficherAttenteBis reste;; 

  let afficherElementBis etatCourant attente =
    print_string Element courant ;
    print_string (getEtatBis etatCourant);
    print_newline();
    print_string  File d'attente;
    afficherAttenteBis attente;
    print_newline();;

  let aEtoileBis init opPoss hEtat estBut =
    let rec boucle etatCourant attente = 
      afficherElementBis etatCourant attente;
      if (estBut (getEtatBis etatCourant)) 
      then etatCourant
      else 
        match (insererLesFilsBis (creerLesFilsBis (getEtatBis etatCourant) (getCoutBis etatCourant) opPoss hEtat (getL etatCourant)) attente) with
         [] - failwith pas de but trouve
         premier  reste - boucle premier reste
    in boucle (init,0,(hEtat init),[]) [];;
  *)


(* TESTS *)
let test1 = aEtoile initG1C opPossG1C hEtatG1C estButG1C;; 
(*let test2 = aEtoileBis initG1C opPossG1C hEtatG1C estButG1C;;*)
