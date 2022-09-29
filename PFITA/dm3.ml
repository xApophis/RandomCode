let nom = "REMETTER" and prenom = "Emilie";;

let fst couple = match couple with (x,_) -> x;;
let snd couple = match couple with (_,x) -> x;;

let rec add_once x list = match list with
  | [] -> [x]
  | head :: tail -> if head = x then failwith "already" else head :: add_once x tail;;

let rec remove_if p list = match list with
  | [] -> []
  | head :: tail -> if p head then remove_if p tail else head :: remove_if p tail;;

let init_comments = (0, []);;

let add_comment author_id text base = 
  match text with
  | "" -> failwith "no comment"
  | t -> (fst base + 1,
          add_once (fst base + 1, author_id, text, []) (snd base));;

let vote_comment user_id comment_id base = 
  let rec vote_comment' comment_list = match comment_list with
    | [] -> []
    | (c_id, u_id, text, user_id_list) :: tail ->
        if c_id = comment_id then
          if u_id = user_id then failwith "autovote"
          else (c_id, u_id, text, add_once user_id user_id_list) :: tail
        else (c_id, u_id, text, user_id_list) :: vote_comment' tail
  in (fst base, vote_comment' (snd base));;
(* Q 4.3 *)
let get_comment comment_id base = 
  let rec get_comment' comment_list = match comment_list with
    | [] -> failwith "not found"
    | (c_id,u_id,text,user_id_list)::tail -> if c_id = comment_id then text
        else get_comment' tail
  in get_comment' (snd base);;

let get_comments author_id base =
  let rec get_comments' comment_list = match comment_list with
    | [] -> []
    | (c_id,u_id,text,user_id_list) :: tail -> if u_id = author_id then text :: get_comments' tail
        else get_comments' tail
  in get_comments' (snd base);;

(*let get_voted_comments author_id base = 
   let rec get_voted_comments' comment_list = match comment_list with 
     | [] -> []
     | (c_id,u_id,text,user_id_list) :: tail -> ;;*)

let remove_comment comment_id base = 
  let rec remove_comment' comment_list = match comment_list with
    | [] -> failwith "not found"
    | (c_id,u_id,text,user_id_list) :: tail -> if c_id = comment_id then remove_comment' tail 
        else (c_id,u_id,text,user_id_list) :: remove_comment' tail
  in (fst base, remove_comment' (snd base));;

let remove_comments user_id base = 
  let rec remove_comments' comment_list = match comment_list with
    | [] -> []
    | (c_id,u_id,text,user_id_list) :: tail -> if u_id = user_id then remove_comments' tail
        else (c_id,u_id,text,user_id_list) :: remove_comments' tail
  in (fst base, remove_comments' (snd base));;  
