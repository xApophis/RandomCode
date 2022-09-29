#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <sys/time.h>
#include <math.h>

#define MAX_NUM_OBJ 1000

int num_obj = 0;
int capacity;
int weight[MAX_NUM_OBJ];
int utility[MAX_NUM_OBJ];

void read_problem(char *filename){
    char line[256];
    FILE *problem = fopen(filename,"r");
    if (problem == NULL){
        fprintf(stderr,"File %s not found.\n",filename);
        exit(-1);
    }

    while (fgets(line, 256, problem) != NULL){
        switch(line[0]){
            case 'c': // capacity
                if (sscanf(&(line[2]),"%d\n", &capacity) != 1){
                    fprintf(stderr,"Error in file format in line:\n");
                    fprintf(stderr, "%s", line);
                    exit(-1);
                }
                break;
            case 'o': // graph size
                if (num_obj >= MAX_NUM_OBJ){
                    fprintf(stderr,"Too many objects (%d): limit is %d\n", num_obj, MAX_NUM_OBJ);
                    exit(-1);
                }
                if (sscanf(&(line[2]),"%d %d\n", &(weight[num_obj]), &(utility[num_obj])) != 2){
                    fprintf(stderr,"Error in file format in line:\n");
                    fprintf(stderr, "%s", line);
                    exit(-1);
                }
                else{
                    num_obj++;
                    break;
                }
            default:
                break;
        }
    }
    if (num_obj == 0){
        fprintf(stderr,"Could not find any object in the problem file. Exiting.");
        exit(-1);
    }
}


int main (int argc, char* argv[]){
    int** S = malloc(num_obj*sizeof(S)); //tableau de l'utilite maximale
    int Umax, i, j;
    int E[MAX_NUM_OBJ]; //tableau des objets choisis
    double start, stop, startP, stopP, timeP, t1, t2, t3, t4;
    
    startP = omp_get_wtime();
    
    start = omp_get_wtime();
    read_problem(argv[1]);
    stop = omp_get_wtime();
    t1 = stop - start;
    printf("Problem reading time : %f\n\n", t1);
    printf("%d objets avec une capacité de %d\n\n", num_obj, capacity);

    
    start = omp_get_wtime();
    #pragma omp parallel for num_threads(4)
    for(i=0;i<num_obj;i++){
        S[i]=malloc((capacity+1)*sizeof(int));
    }
    for(j=0; i<= capacity; i++){
        if(weight[0]>j)
            S[0][j] = 0;
        else
            S[0][j] = utility[0];
    }
    stop = omp_get_wtime();
    t2 = stop - start;
    printf("First row computation time : %f\n", t2);
    
    for(i=1;i<num_obj;i++){
        start = omp_get_wtime();
       #pragma omp parallel for num_threads(4)
        for(j=0;j<=capacity;j++){
            if(weight[i]>j){S[i][j]=S[i-1][j];}
            else{
                if((S[i-1][j-weight[i]] + utility[i]) > S[i-1][j]){
                    S[i][j]=S[i-1][j-weight[i]] + utility[i];
                }
                else {S[i][j]=S[i-1][j];}
            }
        }
        stop=omp_get_wtime();
        t3=stop-start;
    }
    printf("Other rows computation time : %f\n", t3);
    
    Umax=S[num_obj-1][capacity];
    printf("Umax : %d\n\n", Umax);
    j = capacity;
    
    for(i=num_obj-1;i>0;i--){
        if(S[i][j]==(S[i-1][j-weight[i]] + utility[i])){
            E[i]=1;
            j=j-weight[i];
        }
    }
    if(S[i][j] != 0)
        E[i] = 1;
    for(i=0; i<num_obj; i++){
        if(E[i] == 1){
            printf("%d ", i);
        }
    }
    printf("\n");
    
    for(i=0; i<num_obj; i++){
        free(S[i]);
    }
    free(S);
    //free(utility);
    //free(weight);
    
    stopP = omp_get_wtime();
    timeP = stopP - startP;
    printf("Total computation time : %f\n", timeP);

    return 0;
}

