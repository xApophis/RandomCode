/**-------------------------------------------------------------------------
  TP1 - code exercice 2
  Compilation : gcc RemetterEmilie_tp1_exo2.c -o exo2 -lpthread
--------------------------------------------------------------------------**/
#define _GNU_SOURCE

#include <pthread.h>
#include <stdio.h>
#include <unistd.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define NB_THREADS_MAX  10
#define NB_FOIS         10


typedef struct {
    int rang;
    int nbAffichages;
}Arguments;

/*------------------------------------------------------------------------
 * Affichage de l'identite de l'appelant 
  ------------------------------------------------------------------------*/
void afficher (int rang, pthread_t thdId, int codeRetour) {
  printf("Thread compagnon de rang %d, mon identificateur est %lu, je mourrai en retournant %d\n", rang, thdId, codeRetour);
}

/*------------------------------------------------------------------------
 Fonction d'affichage d'une erreur selon la cause de l'echec d'une primitive
 Arret du thread si arret positionne a 1
  ------------------------------------------------------------------------*/
void thdErreur (char *msg, int cause, int arret) {
  printf("%s : %s \n", msg, strerror(cause));
  if (arret) pthread_exit(NULL);
}

/*------------------------------------------------------------------------
 Code execute par chaque thread 
  ------------------------------------------------------------------------*/

void *thd_afficher (void *arg) { 
    int ptid = pthread_self();
    Arguments *arguments;
    arguments = (Arguments*)arg;
    int *random = malloc(sizeof (int));
    *random = rand()%10;
    afficher(arguments->rang, ptid, *random);
    pthread_exit(random);
}

/*------------------------------------------------------------------------*/
int main(int argc, char *argv[]) {
  int i, nbThreads, etat, nbAffichages;
  pthread_t idThreads[NB_THREADS_MAX];
  Arguments arguments[NB_THREADS_MAX];
  srand(time(NULL));
  int *random;
  int somme = 0;
  pthread_t threadPrincipal = pthread_self();

  if (argc != 2) {
    printf("Usage : %s <Nb Threads>\n", argv[0]);
    exit(1);
  }
  nbThreads = atoi(argv[1]);
  if (nbThreads > NB_THREADS_MAX)
    nbThreads = NB_THREADS_MAX;
  
  /* Creation des threads */
  for (i = 0; i < nbThreads; i++) {
    arguments[i].nbAffichages = nbAffichages;
    arguments[i].rang = i;
    /* A compléter */
    if (etat = pthread_create(&idThreads[i], NULL, thd_afficher,(void*)&arguments[i]) != 0)
      thdErreur("Echec create", etat, 0);
  }
  /* Attendre la fin des threads  */
  for (i= 0; i < nbThreads; i++) {
    if ((etat = pthread_join(idThreads[i], (void*)&random)) != 0)
      thdErreur("Echec join", etat, 0); 
    
    printf("Thread principal %lu : valeur retournee par le thread %lu = %d\n", threadPrincipal, idThreads[i], *random);
    
    somme += *random;
    free(random);
  }
  printf("Thread principal %lu : somme des valeurs recues = %d\n", threadPrincipal, somme);
  return 0;
}
