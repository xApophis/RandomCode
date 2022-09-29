/* Modifications du sujet : Le message circule 3 fois
                            Le père injecte le message initial
                            Pour le fils0 on fera for(int i = 0; i < 3; i++){
                                                    lire le message
                                                    afficher le message
                                                    modifier le message
                                                    transmettre le message au frère suivant
                                                }
                            Pour les autres fils on fera while(je lis le message){
                                                            afficher le message
                                                            modifier le message
                                                            transmettre le message au frère suivant
                                                        }
*/
/* Écrire un programme dans lequel le processus principal crée N processus fils qui communiquent selon
le  protocole  décrit  au-dessus.  Lorsque  l’information  sera  revenue  au  premier  processus,
l’application devra se terminer (le père attendra la fin de ses fils). */
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>
#include <time.h>


typedef struct {
  pid_t identificateur;
  int valeur_immuable;
  int compteur;
} infoProcessus;

int fils(int tab1Pipe[2], int tab2Pipe[2], int rangActuel, int rangSuivant){
    infoProcessus infoTransmise;
    while (read (tab1Pipe[0], &infoTransmise, sizeof(infoProcessus)) {
        /* mettre les à jour les info processus + transmettre le message  + print + write*/
}

int main(int argc, char *argv[]){
    /* Recuperation du parametre de l'application */
    if (argc != 2) {
    printf("Usage : %s nombreDeProcessus\n", argv[0]);
    exit(1);    
    }
    
    int N = argv[2]
    /* Creation des variables */
    int pids;
    /* Declaration du message initial qui sera transmis par le père en premier et d'un tableau de pids */
    infoProcessus messageTransmis;
    messageTransmis.identificateur = getpid();
    messageTransmis->valeur_immuable = rand() % 1000;
    messageTransmis->compteur =  0;
    infoProcessus buffer;
    /* Creation et initialisation des tubes */
    int pipetab[N][2];
    for (i = 0; i < N; i++){
        if (pipe(pipetab[i]) == -1){
            perror("Echec pipe");
            exit(1);
        }
    }
    //Creation des fils
    //pid_t pids[N];
    for(int i = 0; i < N; i++){
        switch (pid[i] = fork()) {
            case -1 :
                erreur("Echec fork", 1);
                exit(2);
            case 0 :
                //Fils crees
                for(int j = 0; j < N; j++){
                    if ( j != 1 && j != i+1){
                        close(pipeTab[j][0]);
                        close(pipeTab[j][1]);
                    }
                }
                close(pipeTab[i][1]);
                close(pipeTab[i+1][1]);
                messageTransmis->compteur = i+1;
                i = N;
            default :
            break;
        }
    }
    // Initialisation de l'identificateur et du prochain identificateur
    messageTransmis->identificateur = getppid();
    nextId = (messageTransmis->compteur % N) + 1;
    // cas du fils
    if (pid == 0){
      if(numeroFils == 0 /*Commment savoir si c'est le premier fils ? */){
        for(int i = 0; i < N; i++){
          //Lire le message : vérifier que l'identificateur est bien le PID du père
          read(pipetab[messageTransmis->compteur - 1][0], &buffer, sizeof(struct infoProcessus);
          printf("Le compteur est de %d\n", message->compteur);
          write(pipetab[nextId - 1][1], &val, sizeof(struct infoProcessus));
          //Transmettre le message au fils suivant
        }
      }
      else if(numeroFils > 0){
        while(read(pipetab[messageTransmis->compteur - 1][0], &buffer, sizeof(struct infoProcessus)){
          printf("Le compteur est de %d\n", message->compteur);
          message->compteur++;
          //Transmettre le message au fils suivant
        }
      }
    }
    // cas du père
    else
    {
        printf("Processus de pid %d, n°1 dans l’anneau : j’envoie au n°2 l’info [%d – %d – 1]\n", messageTransmis->identificateur, messageTransmis->identificateur, messageTransmis->valeur_immuable);
        write(pipetab[nextId - 1][1], &val, sizeof(struct infoProcessus));
        read(pipetab[messageTransmis->compteur - 1][0], &buffer, sizeof(struct Value));
        printf("Processus de pid %d : l’information m’est revenue de %d, je peux me terminer\n", messageTransmis->identificateur, buffer->identificateur);
        // attendre la fin de tous les fils
        while (wait(NULL) > 0)
            ;
    }

    return 0;
}
