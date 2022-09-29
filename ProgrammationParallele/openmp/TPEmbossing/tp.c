#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <assert.h>
#include <omp.h>
#include <sys/time.h>

#define NBTHREADS 8

typedef struct color_pixel_struct {
    unsigned char r,g,b;
} color_pixel_type;

typedef struct color_image_struct{
    int width, height;
    color_pixel_type * pixels;
} color_image_type;

typedef struct grey_image_struct{
    int width, height;
    unsigned char * pixels;
} grey_image_type;


/**********************************************************************/

color_image_type * loadColorImage(char *filename){
    int i, width,height,max_value;
    char format[8];
    color_image_type * image;
    FILE * f = fopen(filename,"r");
    if (!f){
        fprintf(stderr,"Cannot open file %s...\n",filename);
        exit(-1);
    }
    fscanf(f,"%s\n",format);
    assert( (format[0]=='P' && format[1]=='3'));  // check P3 format
    while(fgetc(f)=='#'){ //commentaire
        while(fgetc(f) != '\n'); // aller jusqu'a la fin de la ligne
    }
    fseek( f, -1, SEEK_CUR);
    fscanf(f,"%d %d\n", &width, &height);
    fscanf(f,"%d\n", &max_value);
    image = malloc(sizeof(color_image_type));
    assert(image != NULL);
    image->width = width;
    image->height = height;
    image->pixels = malloc(width*height*sizeof(color_pixel_type));
    assert(image->pixels != NULL);

    for(i=0 ; i<width*height ; i++){
        int r,g,b;
        fscanf(f,"%d %d %d", &r, &g, &b);
        image->pixels[i].r = (unsigned char) r;
        image->pixels[i].g = (unsigned char) g;
        image->pixels[i].b = (unsigned char) b;
        }
    fclose(f);
    return image;
}

/**********************************************************************/

grey_image_type * createGreyImage(int width, int height){
    grey_image_type * image = malloc(sizeof(grey_image_type));
    assert(image != NULL);
    image->width = width;
    image->height = height;
    image->pixels = malloc(width*height*sizeof(unsigned char));
    assert(image->pixels != NULL);
    return(image);
}

/**********************************************************************/

void saveGreyImage(char * filename, grey_image_type *image){
    int i;
    FILE * f = fopen(filename,"w");
    if (!f){
        fprintf(stderr,"Cannot open file %s...\n",filename);
        exit(-1);
    }
    fprintf(f,"P2\n%d %d\n255\n",image->width,image->height);
    for(i=0 ; i<image->width*image->height ; i++){
        fprintf(f,"%d\n",image->pixels[i]);
    }
    fclose(f);
}

/**********************************************************************/

void saveColorImage(char * filename, color_image_type *image){
    int i;
    FILE * f = fopen(filename,"w");
    if (!f){
        fprintf(stderr,"Cannot open file %s...\n",filename);
        exit(-1);
    }
    fprintf(f,"P3\n%d %d\n255\n",image->width,image->height);
    for(i=0 ; i<image->width*image->height ; i++){
        fprintf(f,"%d\n%d\n%d\n",image->pixels[i].r, image->pixels[i].g, image->pixels[i].b);
    }
    fclose(f);
}

/**********************************************************************/

void colorToGrey(color_image_type *col_img, grey_image_type *grey_img){
    double t, start, stop;
    
    start = omp_get_wtime();
    for (int i=0; i < col_img->height ; i++){
      for (int j=0; j < col_img->width ; j++){
        int index = i * col_img->width + j;
        color_pixel_type *pix = &(col_img->pixels[index]);
        grey_img->pixels[index] = (299*pix->r + 587*pix->g + 114*pix->b)/1000;
      }
    }
    stop = omp_get_wtime();
    t = stop - start;
    printf("Temps d'execution de la fonction colorToGrey sequentiel = %f secondes\n", t);
}

void colorToGrey_parallel(color_image_type *col_img, grey_image_type *grey_img){
    int i, j;
    double t, start, stop;
    int index;
    
    start = omp_get_wtime();
    #pragma omp parallel num_threads(8) private(i,j)
    {
    #pragma omp for
    for (i=0; i < col_img->height ; i++)
      for (j=0; j < col_img->width ; j++){
        index = i * col_img->width + j;
        color_pixel_type *pix = &(col_img->pixels[index]);
        grey_img->pixels[index] = (299*pix->r + 587*pix->g + 114*pix->b)/1000;
      }
    }
    
    stop = omp_get_wtime();
    t = stop - start;
    printf("Temps d'execution de la fonction colorToGrey parallelise = %f secondes\n", t);
}

/**********************************************************************/
void updateImageByHistrogram(grey_image_type *image){
    int H[256];
    int C[256];
    int width = image->width;
    int height = image->height;
    int i;
    int S = width*height;
    grey_image_type * imageHisto = createGreyImage(image->width, image->height);

    double t, start, stop;
  
    start = omp_get_wtime();
    // Initialisation des matrices à 0
    for(i = 0; i < 256; i++){
        H[i] = 0;
        C[i] = 0;
    }
    // Calcul du nombre de pixels de valeur de i
    for(i = 0; i < height*width; i++){
        H[image->pixels[i]] = H[image->pixels[i]] + 1;
    }
    // Calcul de l'histogramme cumulé avec H
    for(i = 0; i < 256 ; i++){
        if(i == 0){
            C[i] = H[i];
        }
        else{
            C[i] = C[i-1] + H[i];
        }
    }
    // Calcul du contraste
    for (int i=0; i < image->height; i++)
        for (int j=0; j < image->width ; j++){
            int index = i * image->width + j;
            int pix = image->pixels[index];
            imageHisto->pixels[index] = (256 * C[pix]) / S;
        }
    stop = omp_get_wtime();
    t = stop - start;
    printf("Temps d'execution de la fonction updateImageByHistrogram sequentiel = %f secondes\n", t);
}


void updateImageByHistrogram_parallel(grey_image_type *image){
    int H[256];
    int C[256];
    int width = image->width;
    int height = image->height;
    int S = height*width;
    int i;
    grey_image_type * imageHisto = createGreyImage(image->width, image->height);

    double t, start, stop;

    start = omp_get_wtime();

    #pragma omp parallel num_threads(8) private(i)
    {  // Initialisation des matrices à 0
        #pragma omp for
        for(i = 0; i < 256; i++){
            H[i] = 0;
            C[i] = 0;
        }
        // Calcul du nombre de pixels de valeur de i
        #pragma omp for
        for(i = 0; i < height*width; i++){
            #pragma omp atomic
            H[image->pixels[i]] = H[image->pixels[i]] + 1;
        }
        // Calcul de l'histogramme cumulé avec H
        for(i = 0; i < 256 ; i++){
            if(i == 0){
                C[i] = H[i];
            }
            else{
                C[i] = C[i-1] + H[i];
            }
        }
        // Calcul du contraste
        #pragma omp for
        for(i = 0; i < height*width; i++){
            imageHisto->pixels[i] = (256*C[image->pixels[i]])/S;
        }
    }
    stop = omp_get_wtime();
    t = stop - start;
    printf("Temps d'execution de la fonction updateImageByHistrogram parallelise = %f secondes\n", t);
}


/**********************************************************************/
int main(int argc, char ** argv){
    color_image_type * col_img;
    grey_image_type * grey_img;
    grey_image_type *image_Histogram;

    if (argc != 3){
        printf("Usage: togrey <input image> <output image>\n");
        exit(-1);
    }
    char *input_file = argv[1];
    char *output_file = argv[2];

    col_img = loadColorImage(input_file);
    grey_img = createGreyImage(col_img->width, col_img->height);

    //Version sequentielle
    colorToGrey(col_img, grey_img);
    saveGreyImage(output_file, grey_img);
  
    updateImageByHistrogram(grey_img);
    saveGreyImage(output_file, grey_img);
  
    //Version parallelise
    colorToGrey_parallel(col_img, grey_img);
    saveGreyImage(output_file, grey_img);
  
    updateImageByHistrogram_parallel(grey_img);
    saveGreyImage(output_file, grey_img);
}
