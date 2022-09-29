#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <sys/time.h>
#define SIZE 20000
#define NB_THREADS 8

//somme sequentielle
void V1 (int *matrice){
    int somme = 0;
    double t, start, stop;
    
    start = omp_get_wtime();
    for(int i = 0; i < SIZE; i++){
        for(int j = 0; j < SIZE; j++){
            somme+= matrice[i * SIZE + j];
        }
    }
    stop = omp_get_wtime();
    t = stop - start;
    printf("Resultat V1 : %d  Temps : %f\n", somme, t);
}


//somme partielle puis somme des sommes partielles par un seul thread
void V2(int *matrice){
    int somme = 0, tab_sommes[NB_THREADS];
    double t, start, stop;
    
    
    start = omp_get_wtime();
    
    #pragma omp parallel num_threads(NB_THREADS) shared(somme, tab_sommes)
    {
        #pragma omp for
        for(int i = 0; i < NB_THREADS; i++)
            tab_sommes[i] = 0;
        int num_thread = omp_get_thread_num(); //renvoie le numero du NB_THREADS
        #pragma omp for
        for(int i = 0; i < SIZE; i++){
            for(int j = 0; j < SIZE; j++){
                tab_sommes[num_thread]  += matrice[i * SIZE +j];
            }
        }
        #pragma omp single
        for(int i = 0; i < NB_THREADS; i++){
            somme += tab_sommes[i];
        }
    }
            
    stop = omp_get_wtime();
    t = stop - start;
    printf("Resultat V2 : %d  Temps : %f\n", somme, t);
}

//chaque thread ajoute sa somme partielle à la somme globale
void V3(int *matrice){
    int somme = 0, sommeP;
    double t, start, stop;
    
    start = omp_get_wtime();
    #pragma omp parallel num_threads(NB_THREADS) shared(matrice, somme) private(sommeP) default(none)
    {   
        sommeP = 0;
        #pragma omp for
        for (int i = 0; i < SIZE; ++i) {
            for (int j = 0; j < SIZE; ++j){
                sommeP += matrice[i * SIZE +j];
            }
        }
        #pragma omp atomic
        somme += sommeP;
    } 
    stop = omp_get_wtime();
    t = stop - start;
    printf("Resutlat V3 %d  Temps = %f\n", somme, t);
}

//version parallele qui utilise la reduction
void V4(int *matrice){
    int somme = 0;
    double t, start, stop;
    
    start = omp_get_wtime();
    #pragma omp parallel num_threads(NB_THREADS) reduction(+ : somme)
    {
        #pragma omp for
        for (int i = 0; i < SIZE; i++) {
            for (int j = 0; j < SIZE; j++) 
                somme += matrice[i * SIZE +j];
        }
    }
    
    stop = omp_get_wtime();
    t = stop - start;
    printf("Resultat V4 %d  Temps = %f\n", somme, t);
}



int main(int argc, char **argv){
    //Generation d'une matrice aleatoire
    int *matrice;
    matrice = (int*) malloc(SIZE*SIZE*sizeof(int));
    
    for(int i = 0; i < SIZE; i++) {
        for(int j = 0; j < SIZE; j++)
            matrice[i*SIZE + j] = 1;
    }
    //Execution des differentes versions
    V1(matrice);
    V2(matrice);
    V3(matrice);
    V4(matrice);
} 
