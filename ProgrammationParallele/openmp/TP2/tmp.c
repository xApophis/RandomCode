#include <stdio.h>
#include <stdlib.h>
#include <omp.h>
#include <sys/time.h>
#define SIZE 2000

int* solution,nb=16;
long* m,*u;
long masse_max;
double t0,t1,t2,t3,t4,start,stop, debut,fin;

void sac_a_dos(int nb_objet){
    long** s;
    int i,j;
    int e[nb_objet];

    for(i=0;i<nb_objet;i++){
        e[i]=0;
    }

    s=malloc(nb_objet * sizeof(*s));

    start = omp_get_wtime();
    #pragma omp parallel for num_threads(nb)
    for(j=0;j<=masse_max;j++){
        if(m[0]>j){s[0][j]=0;}
        else{s[0][j]=u[0];}
    }
    stop=omp_get_wtime();
    t2=stop-start;

    for(i=1;i<nb_objet;i++){
        start = omp_get_wtime();
        #pragma omp parallel for num_threads(nb)
        for(j=0;j<=masse_max;j++){
            if(m[i]>j){s[i][j]=s[i-1][j];}
            else{
                if((s[i-1][j-m[i]] + u[i]) > s[i-1][j]){
                    s[i][j]=s[i-1][j-m[i]] + u[i];
                }
                else {s[i][j]=s[i-1][j];}
            }
        }
        stop=omp_get_wtime();
        t3=stop-start;
    }

    j=masse_max;


    for(i=nb_objet-1;i>0;i--){
        if(s[i][j]==(s[i-1][j-m[i]] + u[i])){
            e[i]=1;
            j=j-m[i];
        }
    }


    if(s[i][j]!=0){
        e[i]=1;
    }

    for(i=0;i<nb_objet;i++){
        if(e[i]==1){
            printf("%d ",i);
        }
    }

    printf("\n\nJe suis la meilleure utilite (youhou) : %d \n", s[nb_objet-1][masse_max]);
    printf("\nNombre de tread : %d\nCréation de la première ligne\t\t\t\t%f\nCréation d'une ligne quelconque \t\t\t%f \nRemplissage du tableau e\t\t\t\t%f\n",nb,t2,t3,t4);


    for(i=0;i<nb_objet;i++){free(s[i]);}
    free(s);
}

int main(int argc, char* argv[]){
    debut = omp_get_wtime();
    int nb_obj=0,i,capacite;
    FILE* objets = NULL;
    char car, x;

    if(argc!=2){
        perror("usage : ./exo4 tableau_des_objet.txt\n");
        exit(1) ;
    }

    objets=fopen(argv[1],"r");

    if (objets==NULL){
        perror("Impossible d'ouvrir le fichier des objets\n");
        exit(2);
    }

    rewind(objets);
    do{
        car=fgetc(objets);
        if(car=='o'){
            ++nb_obj;
        }
    }while(car!=EOF);

    rewind(objets);
    m=malloc((nb_obj+1)*sizeof(long));
    u=malloc((nb_obj+1)*sizeof(long));

    fscanf(objets,"%c %ld\n",&car,&masse_max);
    if(car==EOF){
        perror("fichier vide");
        exit(2);
    }

    start = omp_get_wtime();
    int max = 0;
    #pragma omp parallel for num_threads(nb)
    for(i=0;i<nb_obj;i++){
    fscanf(objets,"%c %ld %ld\n",&car,&m[i],&u[i]);
    }
    stop=omp_get_wtime();
    t1=stop-start;
    printf("Lecture du problème\t\t\t\t\t%f\n\n",t1);

    printf("%d objets avec une capacite de %d\n\n", nb_obj, masse_max);

    sac_a_dos(nb_obj);
    fin = omp_get_wtime();
    t0=fin-debut;
    printf("Temps total du programme \t\t\t\t%f\n", t0);
    t0=t1+t2+t3+t4;
    printf("Temps total passé dans les parties parallélisées \t%f\n", t0);

    free(u);
    free(m);
    fclose(objets);
    exit(0);
}
