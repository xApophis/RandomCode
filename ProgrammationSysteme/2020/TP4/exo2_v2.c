/**-------------------------------------------------------------------------
  TP4 - Squelette code exercice 2-V2
  Compilation : gcc tp45_exo2-v2_base.c -o tp45_exo2-v2 -Wall
--------------------------------------------------------------------------**/

#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <stdlib.h>


/*------------------------------------------------------------------------
 Fonction d'affichage d'une erreur selon la cause de l'echec d'une primitive
 Arret du processus avec retour valant codeRetour
  ------------------------------------------------------------------------*/
void erreur (char *msg, int codeRetour) {
  perror(msg);
  exit(codeRetour);
}

/*------------------------------------------------------------------------
 Traitement associe a SIGINT
  ------------------------------------------------------------------------*/
void traiterSIGINT (int signal) {
  if(signal==SIGINT)
    printf(">> Ctrl-C/SIGINT recu par %d\n", getpid());
}

/*------------------------------------------------------------------------*/
int main(int argc, char *argv[]) {

    // Se proteger contre Ctrl-C (SIGINT)
    //Structure pour enregistrer une action lors de la réception
    struct sigaction action, oldAction;
    action.sa_handler = traiterSIGINT;

    //On vide la liste des signaux bloqués
    sigemptyset(&action.sa_mask);

    //Redémarrage
    action.sa_flags = SA_RESTART;

    //Mise en place de l'action pour le signal SIGINT (CTRL-C), ancienne action sauvegardée dans oldAction
    if(sigaction(SIGINT, &action, &oldAction) != 0){
        erreur("Echec sigaction", 1);
    }
  
    printf("Processus de pid %d : protege contre SIGINT\n", getpid());

    printf("Processus de pid %d : Je vais executer boucle\n", getpid());

    /* Remplacer son code par celui de l'executable boucler */
    /* Ne pas oublier de changer le répertoire pour son executable afficher */
    // Note : Je n'arrive pas à faire tourner le programme correctement alors que j'ai mis le bon chemin du fichier, les parametres de execl ne doivent pas etre bons mais je ne vois pas quoi mettre d'autre
    if(execl("./home/emilie/Documents/Cours_Emilie/L3/Programmation_Systeme/2020/TP4/afficher","afficher",NULL) != 0){
        erreur("Error execl", 2);
        exit(3);
    }
    return 0;
}
