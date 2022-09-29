/* REMETTER Emilie 21601724 */

#include "image.h"
#include "kdtree.h"
#include "ray.h"
#include "raytracer.h"
#include "scene_types.h"
#include <math.h>
#include <stdio.h>

#include <glm/gtc/epsilon.hpp>
#include <cmath>

#ifndef M_PI
#define M_PI 3.14159265358979323846
#endif

/// acne_eps is a small constant used to prevent acne when computing
/// intersection
//  or boucing (add this amount to the position before casting a new ray !
const float acne_eps = 1e-4;

bool intersectPlane(Ray *ray, Intersection *intersection, Object *obj) {
  float t;
  vec3 normal = obj->geom.plane.normal;
  point3 origin = ray->orig;
  vec3 direction = ray->dir;
  float distance = obj->geom.plane.dist;

  if (abs(dot(direction, normal)) >= acne_eps){
    t = -((dot(origin, normal) + distance) / dot(direction, normal));
    if(t >= ray->tmin && t <= ray->tmax){
      intersection->position = rayAt(*ray, t);
      intersection->mat = &(obj->mat);
      intersection->normal = normalize(obj->geom.plane.normal);
      ray->tmax = t;
      return true;
    }
  }
  return false;
}

bool intersectSphere(Ray *ray, Intersection *intersection, Object *obj) {
  float t = 0, t1 = 0, t2 = 0;
  point3 O = ray->orig;
  float R = obj->geom.sphere.radius;
  vec3 C = obj->geom.sphere.center;

  float a = 1.f;
  float b = dot(ray->dir,(O - C)) * 2.f;
  float c = dot((O - C),(O - C)) - R*R;
  float delta = b*b - 4.f*a*c;

  if(delta < 0.0){
    return false;
  }
  else if(delta >= 0.0){
    t1 = (-b-sqrt(delta))/(2*a);
    t2 = (-b+sqrt(delta))/(2*a);
    if(t1 < ray->tmin){
      t = t2;
    }
    else{
      t = t1;
    }
  }
  if((t >= ray->tmin) && (t <= ray->tmax)){
    intersection->position = rayAt(*ray, t);
    ray->tmax = t;
    intersection->normal = normalize((intersection->position) - C);
    intersection->mat = &(obj->mat);

    return true;
  }
  return false;
}

bool intersectScene(const Scene *scene, Ray *ray, Intersection *intersection) {
  bool hasIntersection = false;
  size_t objectCount = scene->objects.size();

  for (size_t i = 0; i < objectCount; i++) {
    if (scene->objects[i]->geom.type == PLANE) {
      if (hasIntersection)
      intersectPlane(ray, intersection, scene->objects[i]);
      else
      hasIntersection = intersectPlane(ray, intersection, scene->objects[i]);
    }
    else { // object is a sphere
      if (hasIntersection)
      intersectSphere(ray, intersection, scene->objects[i]);
      else
      hasIntersection = intersectSphere(ray, intersection, scene->objects[i]);
    }
  }
  return hasIntersection;
}

/* ---------------------------------------------------------------------------
*/
/*
*	The following functions are coded from Cook-Torrance bsdf model
*description and are suitable only
*  for rough dielectrics material (RDM. Code has been validated with Mitsuba
*renderer)
*/

// Shadowing and masking function. Linked with the NDF. Here, Smith function,
// suitable for Beckmann NDF
float RDM_chiplus(float c) { return (c > 0.f) ? 1.f : 0.f; }

/** Normal Distribution Function : Beckmann
* NdotH : Norm . Half
*/
float RDM_Beckmann(float NdotH, float alpha) {
  float cosCarre = NdotH*NdotH;
  float alphaCarre = alpha * alpha;
  float tan2_x = (1.f - cosCarre) / (cosCarre);

  if (NdotH > 0.f) {
    return 1.f * exp(-tan2_x / (alphaCarre)) / ((float) M_PI * alphaCarre * cosCarre*cosCarre);
  }
  return 0.f;
  //return 0.5f;
}

// Fresnel term computation. Implantation of the exact computation. we can use
// the Schlick approximation
// LdotH : Light . Half
float RDM_Fresnel(float LdotH, float extIOR, float intIOR) {
  float sinCarreTheta = (extIOR/intIOR)*(extIOR/intIOR)*(1-LdotH*LdotH);
  if(sinCarreTheta > 1){
    return 1.f;
  }
  float cosTheta = sqrt(1 - sinCarreTheta);
  float Rs = ((extIOR*LdotH - intIOR*cosTheta)*(extIOR*LdotH - intIOR*cosTheta))/((extIOR*LdotH + intIOR*cosTheta)*(extIOR*LdotH + intIOR*cosTheta));
  float Rp = ((extIOR*cosTheta - intIOR*LdotH)*(extIOR*cosTheta - intIOR*LdotH))/((extIOR*cosTheta + intIOR*LdotH)*(extIOR*cosTheta + intIOR*LdotH));
  return (0.5*(Rs + Rp));
  //return 0.5f;

}

// DdotH : Dir . Half
// HdotN : Half . Norm
float RDM_G1(float DdotH, float DdotN, float alpha) {
  float x = 0.f;
  if (DdotH / DdotN > 0.f) {
    x = 1.f;
  }
  float tan_x = sqrt(1 - DdotN * DdotN) / DdotN;
  float b = 1 / (alpha * tan_x);
  if (b < 1.6) {
    return x * (3.535f * b + 2.181f * b * b) / (1.f + 2.276f * b + 2.577f * b * b);
  }
  return x;
  //return 0.5f;

}

// LdotH : Light . Half
// LdotN : Light . Norm
// VdotH : View . Half
// VdotN : View . Norm
float RDM_Smith(float LdotH, float LdotN, float VdotH, float VdotN, float alpha) {
  return dot(RDM_G1(LdotH, LdotN, alpha), RDM_G1(VdotH, VdotN, alpha));
  //return 0.5f;

}

// Specular term of the Cook-torrance bsdf
// LdotH : Light . Half
// NdotH : Norm . Half
// VdotH : View . Half
// LdotN : Light . Norm
// VdotN : View . Norm
color3 RDM_bsdf_s(float LdotH, float NdotH, float VdotH, float LdotN, float VdotN, Material *m) {

  //! \todo specular term of the bsdf, using D = RDB_Beckmann, F = RDM_Fresnel, G
  //! = RDM_Smith
  float D = RDM_Beckmann(NdotH, m->roughness);
  float F = RDM_Fresnel(LdotH, 1.f, m->IOR);
  float G = RDM_Smith(LdotH, LdotN, VdotH, VdotN, m->roughness);

  return (m->specularColor * D * F * G / (4.f * LdotN * VdotN));
  //return color3(.5f);

}
// diffuse term of the cook torrance bsdf
color3 RDM_bsdf_d(Material *m) {
  return (m->diffuseColor/(float)M_PI);
  //return color3(.5f);

}

// The full evaluation of bsdf(wi, wo) * cos (thetai)
// LdotH : Light . Half
// NdotH : Norm . Half
// VdotH : View . Half
// LdotN : Light . Norm
// VdtoN : View . Norm
// compute bsdf * cos(Oi)
color3 RDM_bsdf(float LdotH, float NdotH, float VdotH, float LdotN, float VdotN, Material *m) {
  return (RDM_bsdf_d(m)+RDM_bsdf_s(LdotH, NdotH, VdotH, LdotN, VdotN, m));
  //return color3(0.f);

}



color3 shade(vec3 n, vec3 v, vec3 l, color3 lc, Material *mat) {
  color3 ret = color3(0.f);
  //float cosTheta = dot(l, n);

  vec3 VplusL = v + l;
  vec3 h = VplusL / sqrt(VplusL.x * VplusL.x + VplusL.y * VplusL.y + VplusL.z * VplusL.z);

  float LdotH = dot(l,h);
  float NdotH = dot(n,h);
  float VdotH = dot(v,h);
  float LdotN = dot(l,n);
  float VdotN = dot(v,n);

  ret = lc * RDM_bsdf(LdotH, NdotH, VdotH, LdotN, VdotN, mat) * LdotN;

  //shade simple
  /*if (cosTheta >= 0.0){
  ret = (mat->diffuseColor / (float)M_PI)*cosTheta*lc;
}*/
return ret;
}

//! if tree is not null, use intersectKdTree to compute the intersection instead
//! of intersect scene

color3 trace_ray(Scene *scene, Ray *ray, KdTree *tree) {
  color3 ret = color3(0, 0, 0);
  Intersection intersection;

  bool intersectionSphere = intersectScene(scene, ray, &intersection);
  if (intersectionSphere == false){
    ret = scene->skyColor;
  }
  else {
    size_t lightsCount = scene->lights.size();
    for (size_t i = 0; i < lightsCount; i++){
      //direction de la lumiere
      vec3 dirLight = normalize(scene->lights[i]->position - intersection.position);
      //Creation de l'ombre
      Ray ombre;
      int tmax = length(scene->lights[i]->position - intersection.position);
      rayInit(&ombre, intersection.position + acne_eps*dirLight, dirLight, acne_eps, tmax);

      Intersection intersectionO;
      bool intersectionOmbre = intersectScene(scene, &ombre, &intersectionO);
      if(intersectionOmbre == false){
        ret += shade(intersection.normal, -(ray->dir), dirLight, scene->lights[i]->color, intersection.mat);
      }
    }
    if (ray->depth < 10) {
      vec3 dirReflechi = reflect(ray->dir, intersection.normal);
      Ray reflechi;
      rayInit(&reflechi, intersection.position + dirReflechi * acne_eps, dirReflechi, acne_eps, 10000, ray->depth+1);
      color3 Cr = trace_ray(scene, &reflechi, tree);
      color3 Cs = intersection.mat->specularColor;
      float LdotH = dot(normalize(ray->dir - (normalize(dirReflechi))), ray->dir);
      float fresnelTerm = RDM_Fresnel(LdotH, 1.f, intersection.mat->IOR);
      if(fresnelTerm > 1.f){
        fresnelTerm = 1.f;
      }
      ret += fresnelTerm * Cr * Cs;
    }
    else {
      ret += color3(0.f);
    }
    //trace_ray simple
    //ret = (vec3)0.5*(intersection.normal) + (vec3)0.5;
  }
  return ret;
}

void renderImage(Image *img, Scene *scene) {

  //! This function is already operational, you might modify it for antialiasing
  //! and kdtree initializaion
  float aspect = 1.f / scene->cam.aspect;

  KdTree *tree = NULL;


  //! \todo initialize KdTree

  float delta_y = 1.f / (img->height * 0.5f);   //! one pixel size
  vec3 dy = delta_y * aspect * scene->cam.ydir; //! one pixel step
  vec3 ray_delta_y = (0.5f - img->height * 0.5f) / (img->height * 0.5f) *
  aspect * scene->cam.ydir;

  float delta_x = 1.f / (img->width * 0.5f);
  vec3 dx = delta_x * scene->cam.xdir;
  vec3 ray_delta_x =
  (0.5f - img->width * 0.5f) / (img->width * 0.5f) * scene->cam.xdir;


  for (size_t j = 0; j < img->height; j++) {
    if (j != 0)
    printf("\033[A\r");
    float progress = (float)j / img->height * 100.f;
    printf("progress\t[");
    int cpt = 0;
    for (cpt = 0; cpt < progress; cpt += 5)
    printf(".");
    for (; cpt < 100; cpt += 5)
    printf(" ");
    printf("]\n");
    #pragma omp parallel for
    for (size_t i = 0; i < img->width; i++) {
      color3 *ptr = getPixelPtr(img, i, j);
      vec3 ray_dir = scene->cam.center + ray_delta_x + ray_delta_y +
      float(i) * dx + float(j) * dy;

      Ray rx;
      rayInit(&rx, scene->cam.position, normalize(ray_dir));
      *ptr = trace_ray(scene, &rx, tree);

    }
  }
}
