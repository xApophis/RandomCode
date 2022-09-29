let rec length = function
  | [] -> 0
  | _ :: l -> 1 + length l

let rec map f = function
  | [] -> []
  | e :: l -> f e :: map f l

type frp =
  | Zero
  | Succ
  | Proj of int * int
  | Comp of frp * frp list
  | Fix of frp * frp
           
module type tENTIER = sig
  type t
  val zero : t
  val suc : t -> t
  val of_frp : frp -> t
  val to_int : t -> int
  val add : t -> t -> t
end

let nom = "REMETTER" and prenom = "Emilie";;

let rec uniq liste = match liste with
  | [] -> failwith "Erreur : Liste vide"
  | [element] -> element
  | tete :: reste -> if tete = uniq(reste) then tete 
      else failwith "Erreur : Les elements de la liste ne sont pas egaux" 
          
let rec nth liste n = match liste with
  | [] -> failwith "Erreur : Liste vide"
  | tete :: reste -> if n = 0 then tete
      else if n > 0 then nth reste (n-1)
      else failwith "Erreur : n doit être >= 0"
          
let rec arite expression = match expression with
  | Zero -> 0
  | Succ -> 1
  | Proj(i, n) -> if i<n then n 
      else failwith "Erreur : i doit être inferieur à n "
  | Comp(f, lg) -> if arite f = length lg then uniq(map arite lg)
      else failwith "Erreur : arite invalide (comp)"
  | Fix(g, h) -> if arite h = (2 + arite g) then 1 + arite g
      else failwith "Erreur : arite invalide (fix)" 
          
let rec opt_arite expression = match expression with
  |Zero -> Some 0
  |Succ -> Some 1
  |Proj(i,n) -> if n > i then Some n else None
  |Comp(f,lg) -> if Some (arite f) = Some (length lg) then Some ( 1 + arite f)
      else None 
  |Fix(g,h) -> if Some (arite h) = Some ( 2 + arite g ) then Some ( 1 + arite g)
      else None

let f_add3 = Comp(Succ,[Comp(Succ,[Succ])])
    
let f_add = Fix(Proj(0, 1),Proj(0, 3));;

(*let rec eval expression liste = 
   if ( arite expression = length liste ) then
     match expression,liste with
     |Zero,_ -> 0
     |Succ,[element]-> element + 1 
     |Proj
   else failwith "Erreur : arite de l'expression inexistante ou differente 
      de la longueur de la liste"
      
 module ENTIER : tENTIER = struct
   type t = frp
   let zero = Zero
   let suc element = Comp(Succ,[element])
   let of_frp expression = if arite expression = 0 then expression 
     else failwith "Erreur : arite != 0"
   let to_int expression = eval expression []
  let rec add x y = match x,y with
    |Zero,y -> y
    |x,Zero -> x
    |x,y    -> add (suc x) (reduce y)
end;;  *) 
