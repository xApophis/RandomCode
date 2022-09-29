from PIL import Image, ImageDraw
from constantes import *
from numpy import binary_repr

def conv_8bits(message,version_qrcode):
	#on etablit des variables utiles plus tard (ici la longueur du message et
        #le nombre de bits sur lequel sera code la longueur du message)
	longueur=len(message)
	nb_bit_version=16
	if version_qrcode < 10:
		nb_bit_version=8
	#ord(x) retourne un caractere (ici x) en unicode.
	#format(ord(x),'b') permet de formatter le premier argument selon le format precise dans le 2nd argument.
	#Ici, 'b' indique un formattage en binaire.
	#zfill(8) permet de preciser le nombre de bit que l'on souhaite utiliser pour chaque caractere.
	#for x in message permet d'effectuer la commande pour chaque caractere contenu dans le message.
	#Pour finir, ''.join permet de regrouper chaque caractere converti en binaire.
	#'' permet de coller les caracteres entre eux.
	message=(''.join(format(ord(x), 'b').zfill(8) for x in message))
	#On convertit la variable "longeur" en binaire 8-bit ou 16-bit,
	#selon la version du QR-code, comme etablit plus haut
	longueur=(''.join(format(longueur, 'b').zfill(nb_bit_version)))
	#On forme les codewords selon le modele format+longueur du message+message
	message='0100'+longueur+message
	return(message)
	
	

def concatenation(message,ecc):
	resultat=str(message+ecc)
	return(resultat)



def chaine_color(message):
  message_color=[]
  for i in range(0,len(message),1):
    message_color.append(choix_couleur(message[i]))
  return(message_color)
 
def choix_couleur(caractere):
	if caractere == '1':
		couleur=(0,0,0)
	if caractere == '0':
		couleur=(255,255,255)
	return(couleur)

def completion(nb_caractere,message):
        i=0
        f=0
        while i != 4 and len(message) < nb_caractere*8:
                message+='0'
                i = i + 1
                
        while len(message)%8!=0 and len(message)< nb_caractere*8:
                message+='0'

        while len(message) < nb_caractere*8:
            if len(message) != nb_caractere*8:
                if f == 0:
                        message += '11101100'
                        f = 1
            if len(message) != nb_caractere*8:
                if f == 1:
                        message += '00010001' 
                        f = 0
                
                
        return(message)
                
        
        
def choix_version (message,nivECC):
                if nivECC == 'L':
                        liste_versions=[17,1,32,2,53,3,78,4]
                if nivECC == 'M':
                        liste_versions=[14,1,26,2,42,3]
                if nivECC == 'Q':
                        liste_versions=[11,1,20,2]
                if nivECC == 'H':
                        liste_versions=[7,1,14,2]
                for i in range(0,len(message),2):
                        if len(message) <= liste_versions[i]:
                                nb_caracteres=liste_versions[i]
                                version=liste_versions[i+1]
                                break
                return(nb_caracteres,version)

def choix_infos_versions(ecc,mask) :
	liste1 = ["L","M","Q","H"]
	liste2 = ["0","8","16","24"]
	liste3 = ["111011111000100","111001011110011","111110110101010","111100010011101","110011000101111","110001100011000","110110001000001","110100101110110","101010000010010","101000100100101","101111001111100","101101101001011","100010111111001","100000011001110","100111110010111","100101010100000","011010101011111","011000001101000","011111100110001","011101000000110","010010010110100","010000110000011","010111011011010","010101111101101","001011010001001","001001110111110","001110011100111","001100111010000","000011101100010","000001001010101","000110100001100","000100000111011"]
	for i in range(0,len(liste1),1) :
		if liste1[i] == ecc :
			info=liste3[int(liste2[i])+int(mask)]
	return(info)
        



def placement_module(image,chaine):
        im=Image.open(image)
        taille_version = im.size[0]-1
        debut=0
        fin=taille_version
        compteur=1
        indice=0
        for x in range(fin,0,-2):

                debut,fin,compteur=fin,debut,-compteur
                if x <= 6:
                        x = x - 1
                        
                       
                

                
                for y in range(debut,fin+compteur,compteur):
                        
                                        

                                        
                                        current=im.getpixel((x,y))
                                        if current==(0,255,0):
                                                if (x)%3 == 0:

                                                        if chaine[indice] == (0,0,0):
                                                            chaine[indice] = (255,255,255)
                                                        elif chaine[indice] == (255,255,255):
                                                            chaine[indice] = (0,0,0)
                                                im.putpixel((x,y),chaine[indice])
                                                indice=indice+1

                                                
                                        x = x - 1

                                
                                        current=im.getpixel((x,y))
                                        if current==(0,255,0):
                                                if (x)%3 == 0 :

                                                        if chaine[indice] == (0,0,0):
                                                            chaine[indice] = (255,255,255)
                                                        elif chaine[indice] == (255,255,255): 
                                                            chaine[indice] = (0,0,0)
                                                im.putpixel((x,y),chaine[indice])
                                                indice=indice+1

                                                
                                        x = x + 1
                                        
                                        
        
                                
        im.save("image.png")
                        



def placement_formats(image,couleur):
        
        f=0
        g=0
        im=Image.open(image)
        taille_version=im.size[0]-1
	
        for i in range(0,7):
                im.putpixel((8,taille_version-i),couleur[i])
        for i in range(14,8,-1):
                im.putpixel((8,g),couleur[i])
                g=g+1
        for i in range(14,6,-1):
                im.putpixel((taille_version-f,8),couleur[i])
                f=f+1
        for i in range(0,6):
                im.putpixel((i,8),couleur[i])
        im.putpixel((7,8),couleur[6])
        im.putpixel((8,8),couleur[7])
        im.putpixel((8,7),couleur[8])
        im.save("image.png")

def matrix(image):
    im=Image.open(image)
    im2=im.resize((im.size[0]*20, im.size[0]*20))
    im2.save('image.png',quality=100)



                        
                                      

def qrv1():
	new_im = Image.new('RGB', (21,21), (0,255,0))
	new_im.putpixel((0,0),0)
	new_im.putpixel((0,1),0)
	new_im.putpixel((0,2),0)
	new_im.putpixel((0,3),0)
	new_im.putpixel((0,4),0)
	new_im.putpixel((0,5),0)
	new_im.putpixel((0,6),0)
	new_im.putpixel((0,7),(255,255,255))
	new_im.putpixel((0,8),(255,255,255))
	new_im.putpixel((0,13),(255,255,255))
	new_im.putpixel((0,14),0)
	new_im.putpixel((0,15),0)
	new_im.putpixel((0,16),0)
	new_im.putpixel((0,17),0)
	new_im.putpixel((0,18),0)
	new_im.putpixel((0,19),0)
	new_im.putpixel((0,20),0)



	new_im.putpixel((1,0),0)
	new_im.putpixel((1,1),(255,255,255))
	new_im.putpixel((1,2),(255,255,255))
	new_im.putpixel((1,3),(255,255,255))
	new_im.putpixel((1,4),(255,255,255))
	new_im.putpixel((1,5),(255,255,255))
	new_im.putpixel((1,6),0)
	new_im.putpixel((1,7),(255,255,255))
	new_im.putpixel((1,8),(255,255,255))
	new_im.putpixel((1,13),(255,255,255))
	new_im.putpixel((1,14),0)
	new_im.putpixel((1,15),(255,255,255))
	new_im.putpixel((1,16),(255,255,255))
	new_im.putpixel((1,17),(255,255,255))
	new_im.putpixel((1,18),(255,255,255))
	new_im.putpixel((1,19),(255,255,255))
	new_im.putpixel((1,20),0)

	new_im.putpixel((2,0),0)
	new_im.putpixel((2,1),(255,255,255))
	new_im.putpixel((2,2),0)
	new_im.putpixel((2,3),0)
	new_im.putpixel((2,4),0)
	new_im.putpixel((2,5),(255,255,255))
	new_im.putpixel((2,6),0)
	new_im.putpixel((2,7),(255,255,255))
	new_im.putpixel((2,8),(255,255,255))
	new_im.putpixel((2,13),(255,255,255))
	new_im.putpixel((2,14),0)
	new_im.putpixel((2,15),(255,255,255))
	new_im.putpixel((2,16),0)
	new_im.putpixel((2,17),0)
	new_im.putpixel((2,18),0)
	new_im.putpixel((2,19),(255,255,255))
	new_im.putpixel((2,20),0)



	new_im.putpixel((3,0),0)
	new_im.putpixel((3,1),(255,255,255))
	new_im.putpixel((3,2),0)
	new_im.putpixel((3,3),0)
	new_im.putpixel((3,4),0)
	new_im.putpixel((3,5),(255,255,255))
	new_im.putpixel((3,6),0)
	new_im.putpixel((3,7),(255,255,255))
	new_im.putpixel((3,8),(255,255,255))
	new_im.putpixel((3,13),(255,255,255))
	new_im.putpixel((3,14),0)
	new_im.putpixel((3,15),(255,255,255))
	new_im.putpixel((3,16),0)
	new_im.putpixel((3,17),0)
	new_im.putpixel((3,18),0)
	new_im.putpixel((3,19),(255,255,255))
	new_im.putpixel((3,20),0)


	new_im.putpixel((4,0),0)
	new_im.putpixel((4,1),(255,255,255))
	new_im.putpixel((4,2),0)
	new_im.putpixel((4,3),0)
	new_im.putpixel((4,4),0)
	new_im.putpixel((4,5),(255,255,255))
	new_im.putpixel((4,6),0)
	new_im.putpixel((4,7),(255,255,255))
	new_im.putpixel((4,8),(255,255,255))
	new_im.putpixel((4,13),(255,255,255))
	new_im.putpixel((4,14),0)
	new_im.putpixel((4,15),(255,255,255))
	new_im.putpixel((4,16),0)
	new_im.putpixel((4,17),0)
	new_im.putpixel((4,18),0)
	new_im.putpixel((4,19),(255,255,255))
	new_im.putpixel((4,20),0)


	new_im.putpixel((5,0),0)
	new_im.putpixel((5,1),(255,255,255))
	new_im.putpixel((5,2),(255,255,255))
	new_im.putpixel((5,3),(255,255,255))
	new_im.putpixel((5,4),(255,255,255))
	new_im.putpixel((5,5),(255,255,255))
	new_im.putpixel((5,6),0)
	new_im.putpixel((5,7),(255,255,255))
	new_im.putpixel((5,8),(255,255,255))
	new_im.putpixel((5,13),(255,255,255))
	new_im.putpixel((5,14),0)
	new_im.putpixel((5,15),(255,255,255))
	new_im.putpixel((5,16),(255,255,255))
	new_im.putpixel((5,17),(255,255,255))
	new_im.putpixel((5,18),(255,255,255))
	new_im.putpixel((5,19),(255,255,255))
	new_im.putpixel((5,20),0)


	new_im.putpixel((6,0),0)
	new_im.putpixel((6,1),0)
	new_im.putpixel((6,2),0)
	new_im.putpixel((6,3),0)
	new_im.putpixel((6,4),0)
	new_im.putpixel((6,5),0)
	new_im.putpixel((6,6),0)
	new_im.putpixel((6,7),(255,255,255))
	new_im.putpixel((6,8),0)
	new_im.putpixel((6,9),(255,255,255))
	new_im.putpixel((6,10),0)
	new_im.putpixel((6,11),(255,255,255))
	new_im.putpixel((6,12),0)
	new_im.putpixel((6,13),(255,255,255))
	new_im.putpixel((6,14),0)
	new_im.putpixel((6,15),0)
	new_im.putpixel((6,16),0)
	new_im.putpixel((6,17),0)
	new_im.putpixel((6,18),0)
	new_im.putpixel((6,19),0)
	new_im.putpixel((6,20),0)

	new_im.putpixel((7,0),(255,255,255))
	new_im.putpixel((7,1),(255,255,255))
	new_im.putpixel((7,2),(255,255,255))
	new_im.putpixel((7,3),(255,255,255))
	new_im.putpixel((7,4),(255,255,255))
	new_im.putpixel((7,5),(255,255,255))
	new_im.putpixel((7,6),(255,255,255))
	new_im.putpixel((7,7),(255,255,255))
	new_im.putpixel((7,8),(255,255,255))
	new_im.putpixel((7,13),(255,255,255))
	new_im.putpixel((7,14),(255,255,255))
	new_im.putpixel((7,15),(255,255,255))
	new_im.putpixel((7,16),(255,255,255))
	new_im.putpixel((7,17),(255,255,255))
	new_im.putpixel((7,18),(255,255,255))
	new_im.putpixel((7,19),(255,255,255))
	new_im.putpixel((7,20),(255,255,255))

	new_im.putpixel((8,0),(255,255,255))
	new_im.putpixel((8,1),(255,255,255))
	new_im.putpixel((8,2),(255,255,255))
	new_im.putpixel((8,3),(255,255,255))
	new_im.putpixel((8,4),(255,255,255))
	new_im.putpixel((8,5),(255,255,255))
	new_im.putpixel((8,6),0)
	new_im.putpixel((8,7),(255,255,255))
	new_im.putpixel((8,8),(255,255,255))
	new_im.putpixel((8,13),0)
	new_im.putpixel((8,14),(255,255,255))
	new_im.putpixel((8,15),(255,255,255))
	new_im.putpixel((8,16),(255,255,255))
	new_im.putpixel((8,17),(255,255,255))
	new_im.putpixel((8,18),(255,255,255))
	new_im.putpixel((8,19),(255,255,255))
	new_im.putpixel((8,20),(255,255,255))

	new_im.putpixel((9,6),(255,255,255))

	new_im.putpixel((10,6),0)

	new_im.putpixel((11,6),(255,255,255))

	new_im.putpixel((12,6),0)

	new_im.putpixel((13,0),(255,255,255))
	new_im.putpixel((13,1),(255,255,255))
	new_im.putpixel((13,2),(255,255,255))
	new_im.putpixel((13,3),(255,255,255))
	new_im.putpixel((13,4),(255,255,255))
	new_im.putpixel((13,5),(255,255,255))
	new_im.putpixel((13,6),(255,255,255))
	new_im.putpixel((13,7),(255,255,255))
	new_im.putpixel((13,8),(255,255,255))

	new_im.putpixel((14,0),0)
	new_im.putpixel((14,1),0)
	new_im.putpixel((14,2),0)
	new_im.putpixel((14,3),0)
	new_im.putpixel((14,4),0)
	new_im.putpixel((14,5),0)
	new_im.putpixel((14,6),0)
	new_im.putpixel((14,7),(255,255,255))
	new_im.putpixel((14,8),(255,255,255))

	new_im.putpixel((15,0),0)
	new_im.putpixel((15,1),(255,255,255))
	new_im.putpixel((15,2),(255,255,255))
	new_im.putpixel((15,3),(255,255,255))
	new_im.putpixel((15,4),(255,255,255))
	new_im.putpixel((15,5),(255,255,255))
	new_im.putpixel((15,6),0)
	new_im.putpixel((15,7),(255,255,255))
	new_im.putpixel((15,8),(255,255,255))

	new_im.putpixel((16,0),0)
	new_im.putpixel((16,1),(255,255,255))
	new_im.putpixel((16,2),0)
	new_im.putpixel((16,3),0)
	new_im.putpixel((16,4),0)
	new_im.putpixel((16,5),(255,255,255))
	new_im.putpixel((16,6),0)
	new_im.putpixel((16,7),(255,255,255))
	new_im.putpixel((16,8),(255,255,255))

	new_im.putpixel((17,0),0)
	new_im.putpixel((17,1),(255,255,255))
	new_im.putpixel((17,2),0)
	new_im.putpixel((17,3),0)
	new_im.putpixel((17,4),0)
	new_im.putpixel((17,5),(255,255,255))
	new_im.putpixel((17,6),0)
	new_im.putpixel((17,7),(255,255,255))
	new_im.putpixel((17,8),(255,255,255))

	new_im.putpixel((18,0),0)
	new_im.putpixel((18,1),(255,255,255))
	new_im.putpixel((18,2),0)
	new_im.putpixel((18,3),0)
	new_im.putpixel((18,4),0)
	new_im.putpixel((18,5),(255,255,255))
	new_im.putpixel((18,6),0)
	new_im.putpixel((18,7),(255,255,255))
	new_im.putpixel((18,8),(255,255,255))

	new_im.putpixel((19,0),0)
	new_im.putpixel((19,1),(255,255,255))
	new_im.putpixel((19,2),(255,255,255))
	new_im.putpixel((19,3),(255,255,255))
	new_im.putpixel((19,4),(255,255,255))
	new_im.putpixel((19,5),(255,255,255))
	new_im.putpixel((19,6),0)
	new_im.putpixel((19,7),(255,255,255))
	new_im.putpixel((19,8),(255,255,255))

	new_im.putpixel((20,0),0)
	new_im.putpixel((20,1),0)
	new_im.putpixel((20,2),0)
	new_im.putpixel((20,3),0)
	new_im.putpixel((20,4),0)
	new_im.putpixel((20,5),0)
	new_im.putpixel((20,6),0)
	new_im.putpixel((20,7),(255,255,255))
	new_im.putpixel((20,8),(255,255,255))
	new_im.save("image.png", "PNG")

def qrv2():
	new_im = Image.new('RGB', (25,25), (0,255,0))
	new_im.putpixel((0,0),0)
	new_im.putpixel((0,1),0)
	new_im.putpixel((0,2),0)
	new_im.putpixel((0,3),0)
	new_im.putpixel((0,4),0)
	new_im.putpixel((0,5),0)
	new_im.putpixel((0,6),0)
	new_im.putpixel((0,7),(255,255,255))
	new_im.putpixel((0,8),(255,255,255))
	new_im.putpixel((0,17),(255,255,255))
	new_im.putpixel((0,18),0)
	new_im.putpixel((0,19),0)
	new_im.putpixel((0,20),0)
	new_im.putpixel((0,21),0)
	new_im.putpixel((0,22),0)
	new_im.putpixel((0,23),0)
	new_im.putpixel((0,24),0)

	new_im.putpixel((1,0),0)
	new_im.putpixel((1,1),(255,255,255))
	new_im.putpixel((1,2),(255,255,255))
	new_im.putpixel((1,3),(255,255,255))
	new_im.putpixel((1,4),(255,255,255))
	new_im.putpixel((1,5),(255,255,255))
	new_im.putpixel((1,6),0)
	new_im.putpixel((1,7),(255,255,255))
	new_im.putpixel((1,8),(255,255,255))
	new_im.putpixel((1,17),(255,255,255))
	new_im.putpixel((1,18),0)
	new_im.putpixel((1,19),(255,255,255))
	new_im.putpixel((1,20),(255,255,255))
	new_im.putpixel((1,21),(255,255,255))
	new_im.putpixel((1,22),(255,255,255))
	new_im.putpixel((1,23),(255,255,255))
	new_im.putpixel((1,24),0)

	new_im.putpixel((2,0),0)
	new_im.putpixel((2,1),(255,255,255))
	new_im.putpixel((2,2),0)
	new_im.putpixel((2,3),0)
	new_im.putpixel((2,4),0)
	new_im.putpixel((2,5),(255,255,255))
	new_im.putpixel((2,6),0)
	new_im.putpixel((2,7),(255,255,255))
	new_im.putpixel((2,8),(255,255,255))
	new_im.putpixel((2,17),(255,255,255))
	new_im.putpixel((2,18),0)
	new_im.putpixel((2,19),(255,255,255))
	new_im.putpixel((2,20),0)
	new_im.putpixel((2,21),0)
	new_im.putpixel((2,22),0)
	new_im.putpixel((2,23),(255,255,255))
	new_im.putpixel((2,24),0)

	new_im.putpixel((3,0),0)
	new_im.putpixel((3,1),(255,255,255))
	new_im.putpixel((3,2),0)
	new_im.putpixel((3,3),0)
	new_im.putpixel((3,4),0)
	new_im.putpixel((3,5),(255,255,255))
	new_im.putpixel((3,6),0)
	new_im.putpixel((3,7),(255,255,255))
	new_im.putpixel((3,8),(255,255,255))
	new_im.putpixel((3,17),(255,255,255))
	new_im.putpixel((3,18),0)
	new_im.putpixel((3,19),(255,255,255))
	new_im.putpixel((3,20),0)
	new_im.putpixel((3,21),0)
	new_im.putpixel((3,22),0)
	new_im.putpixel((3,23),(255,255,255))
	new_im.putpixel((3,24),0)

	new_im.putpixel((4,0),0)
	new_im.putpixel((4,1),(255,255,255))
	new_im.putpixel((4,2),0)
	new_im.putpixel((4,3),0)
	new_im.putpixel((4,4),0)
	new_im.putpixel((4,5),(255,255,255))
	new_im.putpixel((4,6),0)
	new_im.putpixel((4,7),(255,255,255))
	new_im.putpixel((4,8),(255,255,255))
	new_im.putpixel((4,17),(255,255,255))
	new_im.putpixel((4,18),0)
	new_im.putpixel((4,19),(255,255,255))
	new_im.putpixel((4,20),0)
	new_im.putpixel((4,21),0)
	new_im.putpixel((4,22),0)
	new_im.putpixel((4,23),(255,255,255))
	new_im.putpixel((4,24),0)

	new_im.putpixel((5,0),0)
	new_im.putpixel((5,1),(255,255,255))
	new_im.putpixel((5,2),(255,255,255))
	new_im.putpixel((5,3),(255,255,255))
	new_im.putpixel((5,4),(255,255,255))
	new_im.putpixel((5,5),(255,255,255))
	new_im.putpixel((5,6),0)
	new_im.putpixel((5,7),(255,255,255))
	new_im.putpixel((5,8),(255,255,255))
	new_im.putpixel((5,17),(255,255,255))
	new_im.putpixel((5,18),0)
	new_im.putpixel((5,19),(255,255,255))
	new_im.putpixel((5,20),(255,255,255))
	new_im.putpixel((5,21),(255,255,255))
	new_im.putpixel((5,22),(255,255,255))
	new_im.putpixel((5,23),(255,255,255))
	new_im.putpixel((5,24),0)

	new_im.putpixel((6,0),0)
	new_im.putpixel((6,1),0)
	new_im.putpixel((6,2),0)
	new_im.putpixel((6,3),0)
	new_im.putpixel((6,4),0)
	new_im.putpixel((6,5),0)
	new_im.putpixel((6,6),0)
	new_im.putpixel((6,7),(255,255,255))
	new_im.putpixel((6,8),0)
	new_im.putpixel((6,9),(255,255,255))
	new_im.putpixel((6,10),0)
	new_im.putpixel((6,11),(255,255,255))
	new_im.putpixel((6,12),0)
	new_im.putpixel((6,13),(255,255,255))
	new_im.putpixel((6,14),0)
	new_im.putpixel((6,15),(255,255,255))
	new_im.putpixel((6,16),0)
	new_im.putpixel((6,17),(255,255,255))
	new_im.putpixel((6,18),0)
	new_im.putpixel((6,19),0)
	new_im.putpixel((6,20),0)
	new_im.putpixel((6,21),0)
	new_im.putpixel((6,22),0)
	new_im.putpixel((6,23),0)
	new_im.putpixel((6,24),0)
	
	new_im.putpixel((7,0),(255,255,255))
	new_im.putpixel((7,1),(255,255,255))
	new_im.putpixel((7,2),(255,255,255))
	new_im.putpixel((7,3),(255,255,255))
	new_im.putpixel((7,4),(255,255,255))
	new_im.putpixel((7,5),(255,255,255))
	new_im.putpixel((7,6),(255,255,255))
	new_im.putpixel((7,7),(255,255,255))
	new_im.putpixel((7,8),(255,255,255))
	new_im.putpixel((7,17),(255,255,255))
	new_im.putpixel((7,18),(255,255,255))
	new_im.putpixel((7,19),(255,255,255))
	new_im.putpixel((7,20),(255,255,255))
	new_im.putpixel((7,21),(255,255,255))
	new_im.putpixel((7,22),(255,255,255))
	new_im.putpixel((7,23),(255,255,255))
	new_im.putpixel((7,24),(255,255,255))

	new_im.putpixel((8,0),(255,255,255))
	new_im.putpixel((8,1),(255,255,255))
	new_im.putpixel((8,2),(255,255,255))
	new_im.putpixel((8,3),(255,255,255))
	new_im.putpixel((8,4),(255,255,255))
	new_im.putpixel((8,5),(255,255,255))
	new_im.putpixel((8,6),0)
	new_im.putpixel((8,7),(255,255,255))
	new_im.putpixel((8,8),(255,255,255))
	new_im.putpixel((8,17),0)
	new_im.putpixel((8,18),(255,255,255))
	new_im.putpixel((8,19),(255,255,255))
	new_im.putpixel((8,20),(255,255,255))
	new_im.putpixel((8,21),(255,255,255))
	new_im.putpixel((8,22),(255,255,255))
	new_im.putpixel((8,23),(255,255,255))
	new_im.putpixel((8,24),(255,255,255))
	
	new_im.putpixel((9,6),(255,255,255))

	new_im.putpixel((10,6),0)
	
	new_im.putpixel((11,6),(255,255,255))

	new_im.putpixel((12,6),0)
	
	new_im.putpixel((13,6),(255,255,255))

	new_im.putpixel((14,6),0)
	
	new_im.putpixel((15,6),(255,255,255))

	new_im.putpixel((16,6),0)
	new_im.putpixel((16,16),0)
	new_im.putpixel((16,17),0)
	new_im.putpixel((16,18),0)
	new_im.putpixel((16,19),0)
	new_im.putpixel((16,20),0)

	new_im.putpixel((17,0),(255,255,255))
	new_im.putpixel((17,1),(255,255,255))
	new_im.putpixel((17,2),(255,255,255))
	new_im.putpixel((17,3),(255,255,255))
	new_im.putpixel((17,4),(255,255,255))
	new_im.putpixel((17,5),(255,255,255))
	new_im.putpixel((17,6),(255,255,255))
	new_im.putpixel((17,7),(255,255,255))
	new_im.putpixel((17,8),(255,255,255))
	new_im.putpixel((17,16),0)
	new_im.putpixel((17,17),(255,255,255))
	new_im.putpixel((17,18),(255,255,255))
	new_im.putpixel((17,19),(255,255,255))
	new_im.putpixel((17,20),0)

	new_im.putpixel((18,0),0)
	new_im.putpixel((18,1),0)
	new_im.putpixel((18,2),0)
	new_im.putpixel((18,3),0)
	new_im.putpixel((18,4),0)
	new_im.putpixel((18,5),0)
	new_im.putpixel((18,6),0)
	new_im.putpixel((18,7),(255,255,255))
	new_im.putpixel((18,8),(255,255,255))
	new_im.putpixel((18,16),0)
	new_im.putpixel((18,17),(255,255,255))
	new_im.putpixel((18,18),0)
	new_im.putpixel((18,19),(255,255,255))
	new_im.putpixel((18,20),0)

	new_im.putpixel((19,0),0)
	new_im.putpixel((19,1),(255,255,255))
	new_im.putpixel((19,2),(255,255,255))
	new_im.putpixel((19,3),(255,255,255))
	new_im.putpixel((19,4),(255,255,255))
	new_im.putpixel((19,5),(255,255,255))
	new_im.putpixel((19,6),0)
	new_im.putpixel((19,7),(255,255,255))
	new_im.putpixel((19,8),(255,255,255))
	new_im.putpixel((19,16),0)
	new_im.putpixel((19,17),(255,255,255))
	new_im.putpixel((19,18),(255,255,255))
	new_im.putpixel((19,19),(255,255,255))
	new_im.putpixel((19,20),0)

	new_im.putpixel((20,0),0)
	new_im.putpixel((20,1),(255,255,255))
	new_im.putpixel((20,2),0)
	new_im.putpixel((20,3),0)
	new_im.putpixel((20,4),0)
	new_im.putpixel((20,5),(255,255,255))
	new_im.putpixel((20,6),0)
	new_im.putpixel((20,7),(255,255,255))
	new_im.putpixel((20,8),(255,255,255))
	new_im.putpixel((20,16),0)
	new_im.putpixel((20,17),0)
	new_im.putpixel((20,18),0)
	new_im.putpixel((20,19),0)
	new_im.putpixel((20,20),0)

	new_im.putpixel((21,0),0)
	new_im.putpixel((21,1),(255,255,255))
	new_im.putpixel((21,2),0)
	new_im.putpixel((21,3),0)
	new_im.putpixel((21,4),0)
	new_im.putpixel((21,5),(255,255,255))
	new_im.putpixel((21,6),0)
	new_im.putpixel((21,7),(255,255,255))
	new_im.putpixel((21,8),(255,255,255))

	new_im.putpixel((22,0),0)
	new_im.putpixel((22,1),(255,255,255))
	new_im.putpixel((22,2),0)
	new_im.putpixel((22,3),0)
	new_im.putpixel((22,4),0)
	new_im.putpixel((22,5),(255,255,255))
	new_im.putpixel((22,6),0)
	new_im.putpixel((22,7),(255,255,255))
	new_im.putpixel((22,8),(255,255,255))

	new_im.putpixel((23,0),0)
	new_im.putpixel((23,1),(255,255,255))
	new_im.putpixel((23,2),(255,255,255))
	new_im.putpixel((23,3),(255,255,255))
	new_im.putpixel((23,4),(255,255,255))
	new_im.putpixel((23,5),(255,255,255))
	new_im.putpixel((23,6),0)
	new_im.putpixel((23,7),(255,255,255))
	new_im.putpixel((23,8),(255,255,255))

	new_im.putpixel((24,0),0)
	new_im.putpixel((24,1),0)
	new_im.putpixel((24,2),0)
	new_im.putpixel((24,3),0)
	new_im.putpixel((24,4),0)
	new_im.putpixel((24,5),0)
	new_im.putpixel((24,6),0)
	new_im.putpixel((24,7),(255,255,255))
	new_im.putpixel((24,8),(255,255,255))
	new_im.save("image.png", "PNG")

def qrv3():
	new_im = Image.new('RGB', (29,29), (0,255,0))
	new_im.putpixel((0,0),0)
	new_im.putpixel((0,1),0)
	new_im.putpixel((0,2),0)
	new_im.putpixel((0,3),0)
	new_im.putpixel((0,4),0)
	new_im.putpixel((0,5),0)
	new_im.putpixel((0,6),0)
	new_im.putpixel((0,7),(255,255,255))
	new_im.putpixel((0,8),(255,255,255))
	new_im.putpixel((0,21),(255,255,255))
	new_im.putpixel((0,22),0)
	new_im.putpixel((0,23),0)
	new_im.putpixel((0,24),0)
	new_im.putpixel((0,25),0)
	new_im.putpixel((0,26),0)
	new_im.putpixel((0,27),0)
	new_im.putpixel((0,28),0)



	new_im.putpixel((1,0),0)
	new_im.putpixel((1,1),(255,255,255))
	new_im.putpixel((1,2),(255,255,255))
	new_im.putpixel((1,3),(255,255,255))
	new_im.putpixel((1,4),(255,255,255))
	new_im.putpixel((1,5),(255,255,255))
	new_im.putpixel((1,6),0)
	new_im.putpixel((1,7),(255,255,255))
	new_im.putpixel((1,8),(255,255,255))
	new_im.putpixel((1,21),(255,255,255))
	new_im.putpixel((1,22),0)
	new_im.putpixel((1,23),(255,255,255))
	new_im.putpixel((1,24),(255,255,255))
	new_im.putpixel((1,25),(255,255,255))
	new_im.putpixel((1,26),(255,255,255))
	new_im.putpixel((1,27),(255,255,255))
	new_im.putpixel((1,28),0)

	new_im.putpixel((2,0),0)
	new_im.putpixel((2,1),(255,255,255))
	new_im.putpixel((2,2),0)
	new_im.putpixel((2,3),0)
	new_im.putpixel((2,4),0)
	new_im.putpixel((2,5),(255,255,255))
	new_im.putpixel((2,6),0)
	new_im.putpixel((2,7),(255,255,255))
	new_im.putpixel((2,8),(255,255,255))
	new_im.putpixel((2,21),(255,255,255))
	new_im.putpixel((2,22),0)
	new_im.putpixel((2,23),(255,255,255))
	new_im.putpixel((2,24),0)
	new_im.putpixel((2,25),0)
	new_im.putpixel((2,26),0)
	new_im.putpixel((2,27),(255,255,255))
	new_im.putpixel((2,28),0)

	new_im.putpixel((3,0),0)
	new_im.putpixel((3,1),(255,255,255))
	new_im.putpixel((3,2),0)
	new_im.putpixel((3,3),0)
	new_im.putpixel((3,4),0)
	new_im.putpixel((3,5),(255,255,255))
	new_im.putpixel((3,6),0)
	new_im.putpixel((3,7),(255,255,255))
	new_im.putpixel((3,8),(255,255,255))
	new_im.putpixel((3,21),(255,255,255))
	new_im.putpixel((3,22),0)
	new_im.putpixel((3,23),(255,255,255))
	new_im.putpixel((3,24),0)
	new_im.putpixel((3,25),0)
	new_im.putpixel((3,26),0)
	new_im.putpixel((3,27),(255,255,255))
	new_im.putpixel((3,28),0)

	new_im.putpixel((4,0),0)
	new_im.putpixel((4,1),(255,255,255))
	new_im.putpixel((4,2),0)
	new_im.putpixel((4,3),0)
	new_im.putpixel((4,4),0)
	new_im.putpixel((4,5),(255,255,255))
	new_im.putpixel((4,6),0)
	new_im.putpixel((4,7),(255,255,255))
	new_im.putpixel((4,8),(255,255,255))
	new_im.putpixel((4,21),(255,255,255))
	new_im.putpixel((4,22),0)
	new_im.putpixel((4,23),(255,255,255))
	new_im.putpixel((4,24),0)
	new_im.putpixel((4,25),0)
	new_im.putpixel((4,26),0)
	new_im.putpixel((4,27),(255,255,255))
	new_im.putpixel((4,28),0)

	new_im.putpixel((5,0),0)
	new_im.putpixel((5,1),(255,255,255))
	new_im.putpixel((5,2),(255,255,255))
	new_im.putpixel((5,3),(255,255,255))
	new_im.putpixel((5,4),(255,255,255))
	new_im.putpixel((5,5),(255,255,255))
	new_im.putpixel((5,6),0)
	new_im.putpixel((5,7),(255,255,255))
	new_im.putpixel((5,8),(255,255,255))
	new_im.putpixel((5,21),(255,255,255))
	new_im.putpixel((5,22),0)
	new_im.putpixel((5,23),(255,255,255))
	new_im.putpixel((5,24),(255,255,255))
	new_im.putpixel((5,25),(255,255,255))
	new_im.putpixel((5,26),(255,255,255))
	new_im.putpixel((5,27),(255,255,255))
	new_im.putpixel((5,28),0)


	new_im.putpixel((6,0),0)
	new_im.putpixel((6,1),0)
	new_im.putpixel((6,2),0)
	new_im.putpixel((6,3),0)
	new_im.putpixel((6,4),0)
	new_im.putpixel((6,5),0)
	new_im.putpixel((6,6),0)
	new_im.putpixel((6,7),(255,255,255))
	new_im.putpixel((6,8),0)
	new_im.putpixel((6,9),(255,255,255))
	new_im.putpixel((6,10),0)
	new_im.putpixel((6,11),(255,255,255))
	new_im.putpixel((6,12),0)
	new_im.putpixel((6,13),(255,255,255))
	new_im.putpixel((6,14),0)
	new_im.putpixel((6,15),(255,255,255))
	new_im.putpixel((6,16),0)
	new_im.putpixel((6,17),(255,255,255))
	new_im.putpixel((6,18),0)
	new_im.putpixel((6,19),(255,255,255))
	new_im.putpixel((6,20),0)
	new_im.putpixel((6,21),(255,255,255))
	new_im.putpixel((6,22),0)
	new_im.putpixel((6,23),0)
	new_im.putpixel((6,24),0)
	new_im.putpixel((6,25),0)
	new_im.putpixel((6,26),0)
	new_im.putpixel((6,27),0)
	new_im.putpixel((6,28),0)

	new_im.putpixel((7,0),(255,255,255))
	new_im.putpixel((7,1),(255,255,255))
	new_im.putpixel((7,2),(255,255,255))
	new_im.putpixel((7,3),(255,255,255))
	new_im.putpixel((7,4),(255,255,255))
	new_im.putpixel((7,5),(255,255,255))
	new_im.putpixel((7,6),(255,255,255))
	new_im.putpixel((7,7),(255,255,255))
	new_im.putpixel((7,8),(255,255,255))
	new_im.putpixel((7,21),(255,255,255))
	new_im.putpixel((7,22),(255,255,255))
	new_im.putpixel((7,23),(255,255,255))
	new_im.putpixel((7,24),(255,255,255))
	new_im.putpixel((7,25),(255,255,255))
	new_im.putpixel((7,26),(255,255,255))
	new_im.putpixel((7,27),(255,255,255))
	new_im.putpixel((7,28),(255,255,255))
	
	new_im.putpixel((8,0),(255,255,255))
	new_im.putpixel((8,1),(255,255,255))
	new_im.putpixel((8,2),(255,255,255))
	new_im.putpixel((8,3),(255,255,255))
	new_im.putpixel((8,4),(255,255,255))
	new_im.putpixel((8,5),(255,255,255))
	new_im.putpixel((8,6),0)
	new_im.putpixel((8,7),(255,255,255))
	new_im.putpixel((8,8),(255,255,255))
	new_im.putpixel((8,21),0)
	new_im.putpixel((8,22),(255,255,255))
	new_im.putpixel((8,23),(255,255,255))
	new_im.putpixel((8,24),(255,255,255))
	new_im.putpixel((8,25),(255,255,255))
	new_im.putpixel((8,26),(255,255,255))
	new_im.putpixel((8,27),(255,255,255))
	new_im.putpixel((8,28),(255,255,255))
	
	new_im.putpixel((9,6),(255,255,255))
	
	new_im.putpixel((10,6),0)
	
	new_im.putpixel((11,6),(255,255,255))

	new_im.putpixel((12,6),0)
	
	new_im.putpixel((13,6),(255,255,255))

	new_im.putpixel((14,6),0)
	
	new_im.putpixel((15,6),(255,255,255))

	new_im.putpixel((16,6),0)
	
	new_im.putpixel((17,6),(255,255,255))

	new_im.putpixel((18,6),0)
	
	new_im.putpixel((19,6),(255,255,255))

	new_im.putpixel((20,6),0)
	new_im.putpixel((20,20),0)
	new_im.putpixel((20,21),0)
	new_im.putpixel((20,22),0)
	new_im.putpixel((20,23),0)
	new_im.putpixel((20,24),0)
	
	new_im.putpixel((21,0),(255,255,255))
	new_im.putpixel((21,1),(255,255,255))
	new_im.putpixel((21,2),(255,255,255))
	new_im.putpixel((21,3),(255,255,255))
	new_im.putpixel((21,4),(255,255,255))
	new_im.putpixel((21,5),(255,255,255))
	new_im.putpixel((21,6),(255,255,255))
	new_im.putpixel((21,7),(255,255,255))
	new_im.putpixel((21,8),(255,255,255))
	new_im.putpixel((21,20),0)
	new_im.putpixel((21,21),(255,255,255))
	new_im.putpixel((21,22),(255,255,255))
	new_im.putpixel((21,23),(255,255,255))
	new_im.putpixel((21,24),0)

	new_im.putpixel((22,0),0)
	new_im.putpixel((22,1),0)
	new_im.putpixel((22,2),0)
	new_im.putpixel((22,3),0)
	new_im.putpixel((22,4),0)
	new_im.putpixel((22,5),0)
	new_im.putpixel((22,6),0)
	new_im.putpixel((22,7),(255,255,255))
	new_im.putpixel((22,8),(255,255,255))
	new_im.putpixel((22,20),0)
	new_im.putpixel((22,21),(255,255,255))
	new_im.putpixel((22,22),0)
	new_im.putpixel((22,23),(255,255,255))
	new_im.putpixel((22,24),0)

	new_im.putpixel((23,0),0)
	new_im.putpixel((23,1),(255,255,255))
	new_im.putpixel((23,2),(255,255,255))
	new_im.putpixel((23,3),(255,255,255))
	new_im.putpixel((23,4),(255,255,255))
	new_im.putpixel((23,5),(255,255,255))
	new_im.putpixel((23,6),0)
	new_im.putpixel((23,7),(255,255,255))
	new_im.putpixel((23,8),(255,255,255))
	new_im.putpixel((23,20),0)
	new_im.putpixel((23,21),(255,255,255))
	new_im.putpixel((23,22),(255,255,255))
	new_im.putpixel((23,23),(255,255,255))
	new_im.putpixel((23,24),0)

	new_im.putpixel((24,0),0)
	new_im.putpixel((24,1),(255,255,255))
	new_im.putpixel((24,2),0)
	new_im.putpixel((24,3),0)
	new_im.putpixel((24,4),0)
	new_im.putpixel((24,5),(255,255,255))
	new_im.putpixel((24,6),0)
	new_im.putpixel((24,7),(255,255,255))
	new_im.putpixel((24,8),(255,255,255))
	new_im.putpixel((24,20),0)
	new_im.putpixel((24,21),0)
	new_im.putpixel((24,22),0)
	new_im.putpixel((24,23),0)
	new_im.putpixel((24,24),0)

	new_im.putpixel((25,0),0)
	new_im.putpixel((25,1),(255,255,255))
	new_im.putpixel((25,2),0)
	new_im.putpixel((25,3),0)
	new_im.putpixel((25,4),0)
	new_im.putpixel((25,5),(255,255,255))
	new_im.putpixel((25,6),0)
	new_im.putpixel((25,7),(255,255,255))
	new_im.putpixel((25,8),(255,255,255))


	new_im.putpixel((26,0),0)
	new_im.putpixel((26,1),(255,255,255))
	new_im.putpixel((26,2),0)
	new_im.putpixel((26,3),0)
	new_im.putpixel((26,4),0)
	new_im.putpixel((26,5),(255,255,255))
	new_im.putpixel((26,6),0)
	new_im.putpixel((26,7),(255,255,255))
	new_im.putpixel((26,8),(255,255,255))

	new_im.putpixel((27,0),0)
	new_im.putpixel((27,1),(255,255,255))
	new_im.putpixel((27,2),(255,255,255))
	new_im.putpixel((27,3),(255,255,255))
	new_im.putpixel((27,4),(255,255,255))
	new_im.putpixel((27,5),(255,255,255))
	new_im.putpixel((27,6),0)
	new_im.putpixel((27,7),(255,255,255))
	new_im.putpixel((27,8),(255,255,255))

	new_im.putpixel((28,0),0)
	new_im.putpixel((28,1),0)
	new_im.putpixel((28,2),0)
	new_im.putpixel((28,3),0)
	new_im.putpixel((28,4),0)
	new_im.putpixel((28,5),0)
	new_im.putpixel((28,6),0)
	new_im.putpixel((28,7),(255,255,255))
	new_im.putpixel((28,8),(255,255,255))
	new_im.save("image.png", "PNG")

def qrv4():
	new_im = Image.new('RGB', (33,33), (0,255,0))
	new_im.putpixel((0,0),0)
	new_im.putpixel((0,1),0)
	new_im.putpixel((0,2),0)
	new_im.putpixel((0,3),0)
	new_im.putpixel((0,4),0)
	new_im.putpixel((0,5),0)
	new_im.putpixel((0,6),0)
	new_im.putpixel((0,7),(255,255,255))
	new_im.putpixel((0,8),(255,255,255))
	new_im.putpixel((0,25),(255,255,255))
	new_im.putpixel((0,26),0)
	new_im.putpixel((0,27),0)
	new_im.putpixel((0,28),0)
	new_im.putpixel((0,29),0)
	new_im.putpixel((0,30),0)
	new_im.putpixel((0,31),0)
	new_im.putpixel((0,32),0)



	new_im.putpixel((1,0),0)
	new_im.putpixel((1,1),(255,255,255))
	new_im.putpixel((1,2),(255,255,255))
	new_im.putpixel((1,3),(255,255,255))
	new_im.putpixel((1,4),(255,255,255))
	new_im.putpixel((1,5),(255,255,255))
	new_im.putpixel((1,6),0)
	new_im.putpixel((1,7),(255,255,255))
	new_im.putpixel((1,8),(255,255,255))
	new_im.putpixel((1,25),(255,255,255))
	new_im.putpixel((1,26),0)
	new_im.putpixel((1,27),(255,255,255))
	new_im.putpixel((1,28),(255,255,255))
	new_im.putpixel((1,29),(255,255,255))
	new_im.putpixel((1,30),(255,255,255))
	new_im.putpixel((1,31),(255,255,255))
	new_im.putpixel((1,32),0)

	new_im.putpixel((2,0),0)
	new_im.putpixel((2,1),(255,255,255))
	new_im.putpixel((2,2),0)
	new_im.putpixel((2,3),0)
	new_im.putpixel((2,4),0)
	new_im.putpixel((2,5),(255,255,255))
	new_im.putpixel((2,6),0)
	new_im.putpixel((2,7),(255,255,255))
	new_im.putpixel((2,8),(255,255,255))
	new_im.putpixel((2,25),(255,255,255))
	new_im.putpixel((2,26),0)
	new_im.putpixel((2,27),(255,255,255))
	new_im.putpixel((2,28),0)
	new_im.putpixel((2,29),0)
	new_im.putpixel((2,30),0)
	new_im.putpixel((2,31),(255,255,255))
	new_im.putpixel((2,32),0)

	new_im.putpixel((3,0),0)
	new_im.putpixel((3,1),(255,255,255))
	new_im.putpixel((3,2),0)
	new_im.putpixel((3,3),0)
	new_im.putpixel((3,4),0)
	new_im.putpixel((3,5),(255,255,255))
	new_im.putpixel((3,6),0)
	new_im.putpixel((3,7),(255,255,255))
	new_im.putpixel((3,8),(255,255,255))
	new_im.putpixel((3,25),(255,255,255))
	new_im.putpixel((3,26),0)
	new_im.putpixel((3,27),(255,255,255))
	new_im.putpixel((3,28),0)
	new_im.putpixel((3,29),0)
	new_im.putpixel((3,30),0)
	new_im.putpixel((3,31),(255,255,255))
	new_im.putpixel((3,32),0)

	new_im.putpixel((4,0),0)
	new_im.putpixel((4,1),(255,255,255))
	new_im.putpixel((4,2),0)
	new_im.putpixel((4,3),0)
	new_im.putpixel((4,4),0)
	new_im.putpixel((4,5),(255,255,255))
	new_im.putpixel((4,6),0)
	new_im.putpixel((4,7),(255,255,255))
	new_im.putpixel((4,8),(255,255,255))
	new_im.putpixel((4,25),(255,255,255))
	new_im.putpixel((4,26),0)
	new_im.putpixel((4,27),(255,255,255))
	new_im.putpixel((4,28),0)
	new_im.putpixel((4,29),0)
	new_im.putpixel((4,30),0)
	new_im.putpixel((4,31),(255,255,255))
	new_im.putpixel((4,32),0)

	new_im.putpixel((5,0),0)
	new_im.putpixel((5,1),(255,255,255))
	new_im.putpixel((5,2),(255,255,255))
	new_im.putpixel((5,3),(255,255,255))
	new_im.putpixel((5,4),(255,255,255))
	new_im.putpixel((5,5),(255,255,255))
	new_im.putpixel((5,6),0)
	new_im.putpixel((5,7),(255,255,255))
	new_im.putpixel((5,8),(255,255,255))
	new_im.putpixel((5,25),(255,255,255))
	new_im.putpixel((5,26),0)
	new_im.putpixel((5,27),(255,255,255))
	new_im.putpixel((5,28),(255,255,255))
	new_im.putpixel((5,29),(255,255,255))
	new_im.putpixel((5,30),(255,255,255))
	new_im.putpixel((5,31),(255,255,255))
	new_im.putpixel((5,32),0)


	new_im.putpixel((6,0),0)
	new_im.putpixel((6,1),0)
	new_im.putpixel((6,2),0)
	new_im.putpixel((6,3),0)
	new_im.putpixel((6,4),0)
	new_im.putpixel((6,5),0)
	new_im.putpixel((6,6),0)
	new_im.putpixel((6,7),(255,255,255))
	new_im.putpixel((6,8),0)
	new_im.putpixel((6,9),(255,255,255))
	new_im.putpixel((6,10),0)
	new_im.putpixel((6,11),(255,255,255))
	new_im.putpixel((6,12),0)
	new_im.putpixel((6,13),(255,255,255))
	new_im.putpixel((6,14),0)
	new_im.putpixel((6,15),(255,255,255))
	new_im.putpixel((6,16),0)
	new_im.putpixel((6,17),(255,255,255))
	new_im.putpixel((6,18),0)
	new_im.putpixel((6,19),(255,255,255))
	new_im.putpixel((6,20),0)
	new_im.putpixel((6,21),(255,255,255))
	new_im.putpixel((6,22),0)
	new_im.putpixel((6,23),(255,255,255))
	new_im.putpixel((6,24),0)
	new_im.putpixel((6,25),(255,255,255))
	new_im.putpixel((6,26),0)
	new_im.putpixel((6,27),0)
	new_im.putpixel((6,28),0)
	new_im.putpixel((6,29),0)
	new_im.putpixel((6,30),0)
	new_im.putpixel((6,31),0)
	new_im.putpixel((6,32),0)
	
	new_im.putpixel((7,0),(255,255,255))
	new_im.putpixel((7,1),(255,255,255))
	new_im.putpixel((7,2),(255,255,255))
	new_im.putpixel((7,3),(255,255,255))
	new_im.putpixel((7,4),(255,255,255))
	new_im.putpixel((7,5),(255,255,255))
	new_im.putpixel((7,6),(255,255,255))
	new_im.putpixel((7,7),(255,255,255))
	new_im.putpixel((7,8),(255,255,255))
	new_im.putpixel((7,25),(255,255,255))
	new_im.putpixel((7,26),(255,255,255))
	new_im.putpixel((7,27),(255,255,255))
	new_im.putpixel((7,28),(255,255,255))
	new_im.putpixel((7,29),(255,255,255))
	new_im.putpixel((7,30),(255,255,255))
	new_im.putpixel((7,31),(255,255,255))
	new_im.putpixel((7,32),(255,255,255))

	new_im.putpixel((8,0),(255,255,255))
	new_im.putpixel((8,1),(255,255,255))
	new_im.putpixel((8,2),(255,255,255))
	new_im.putpixel((8,3),(255,255,255))
	new_im.putpixel((8,4),(255,255,255))
	new_im.putpixel((8,5),(255,255,255))
	new_im.putpixel((8,6),0)
	new_im.putpixel((8,7),(255,255,255))
	new_im.putpixel((8,8),(255,255,255))
	new_im.putpixel((8,25),0)
	new_im.putpixel((8,26),(255,255,255))
	new_im.putpixel((8,27),(255,255,255))
	new_im.putpixel((8,28),(255,255,255))
	new_im.putpixel((8,29),(255,255,255))
	new_im.putpixel((8,30),(255,255,255))
	new_im.putpixel((8,31),(255,255,255))
	new_im.putpixel((8,32),(255,255,255))
	
	new_im.putpixel((9,6),(255,255,255))
	
	new_im.putpixel((10,6),0)
	
	new_im.putpixel((11,6),(255,255,255))

	new_im.putpixel((12,6),0)
	
	new_im.putpixel((13,6),(255,255,255))

	new_im.putpixel((14,6),0)
	
	new_im.putpixel((15,6),(255,255,255))

	new_im.putpixel((16,6),0)
	
	new_im.putpixel((17,6),(255,255,255))

	new_im.putpixel((18,6),0)
	
	new_im.putpixel((19,6),(255,255,255))

	new_im.putpixel((20,6),0)
	
	new_im.putpixel((21,6),(255,255,255))

	new_im.putpixel((22,6),0)
	
	new_im.putpixel((23,6),(255,255,255))

	new_im.putpixel((24,6),0)
	new_im.putpixel((24,24),0)
	new_im.putpixel((24,25),0)
	new_im.putpixel((24,26),0)
	new_im.putpixel((24,27),0)
	new_im.putpixel((24,28),0)

	new_im.putpixel((25,0),(255,255,255))
	new_im.putpixel((25,1),(255,255,255))
	new_im.putpixel((25,2),(255,255,255))
	new_im.putpixel((25,3),(255,255,255))
	new_im.putpixel((25,4),(255,255,255))
	new_im.putpixel((25,5),(255,255,255))
	new_im.putpixel((25,6),(255,255,255))
	new_im.putpixel((25,7),(255,255,255))
	new_im.putpixel((25,8),(255,255,255))
	new_im.putpixel((25,24),0)
	new_im.putpixel((25,25),(255,255,255))
	new_im.putpixel((25,26),(255,255,255))
	new_im.putpixel((25,27),(255,255,255))
	new_im.putpixel((25,28),0)

	new_im.putpixel((26,0),0)
	new_im.putpixel((26,1),0)
	new_im.putpixel((26,2),0)
	new_im.putpixel((26,3),0)
	new_im.putpixel((26,4),0)
	new_im.putpixel((26,5),0)
	new_im.putpixel((26,6),0)
	new_im.putpixel((26,7),(255,255,255))
	new_im.putpixel((26,8),(255,255,255))
	new_im.putpixel((26,24),0)
	new_im.putpixel((26,25),(255,255,255))
	new_im.putpixel((26,26),0)
	new_im.putpixel((26,27),(255,255,255))
	new_im.putpixel((26,28),0)

	new_im.putpixel((27,0),0)
	new_im.putpixel((27,1),(255,255,255))
	new_im.putpixel((27,2),(255,255,255))
	new_im.putpixel((27,3),(255,255,255))
	new_im.putpixel((27,4),(255,255,255))
	new_im.putpixel((27,5),(255,255,255))
	new_im.putpixel((27,6),0)
	new_im.putpixel((27,7),(255,255,255))
	new_im.putpixel((27,8),(255,255,255))
	new_im.putpixel((27,24),0)
	new_im.putpixel((27,25),(255,255,255))
	new_im.putpixel((27,26),(255,255,255))
	new_im.putpixel((27,27),(255,255,255))
	new_im.putpixel((27,28),0)

	new_im.putpixel((28,0),0)
	new_im.putpixel((28,1),(255,255,255))
	new_im.putpixel((28,2),0)
	new_im.putpixel((28,3),0)
	new_im.putpixel((28,4),0)
	new_im.putpixel((28,5),(255,255,255))
	new_im.putpixel((28,6),0)
	new_im.putpixel((28,7),(255,255,255))
	new_im.putpixel((28,8),(255,255,255))
	new_im.putpixel((28,24),0)
	new_im.putpixel((28,25),0)
	new_im.putpixel((28,26),0)
	new_im.putpixel((28,27),0)
	new_im.putpixel((28,28),0)

	new_im.putpixel((29,0),0)
	new_im.putpixel((29,1),(255,255,255))
	new_im.putpixel((29,2),0)
	new_im.putpixel((29,3),0)
	new_im.putpixel((29,4),0)
	new_im.putpixel((29,5),(255,255,255))
	new_im.putpixel((29,6),0)
	new_im.putpixel((29,7),(255,255,255))
	new_im.putpixel((29,8),(255,255,255))

	new_im.putpixel((30,0),0)
	new_im.putpixel((30,1),(255,255,255))
	new_im.putpixel((30,2),0)
	new_im.putpixel((30,3),0)
	new_im.putpixel((30,4),0)
	new_im.putpixel((30,5),(255,255,255))
	new_im.putpixel((30,6),0)
	new_im.putpixel((30,7),(255,255,255))
	new_im.putpixel((30,8),(255,255,255))

	new_im.putpixel((31,0),0)
	new_im.putpixel((31,1),(255,255,255))
	new_im.putpixel((31,2),(255,255,255))
	new_im.putpixel((31,3),(255,255,255))
	new_im.putpixel((31,4),(255,255,255))
	new_im.putpixel((31,5),(255,255,255))
	new_im.putpixel((31,6),0)
	new_im.putpixel((31,7),(255,255,255))
	new_im.putpixel((31,8),(255,255,255))

	new_im.putpixel((32,0),0)
	new_im.putpixel((32,1),0)
	new_im.putpixel((32,2),0)
	new_im.putpixel((32,3),0)
	new_im.putpixel((32,4),0)
	new_im.putpixel((32,5),0)
	new_im.putpixel((32,6),0)
	new_im.putpixel((32,7),(255,255,255))
	new_im.putpixel((32,8),(255,255,255))

	new_im.save("image.png", "PNG")



def tmp(mcb):
        ma_liste = [0] * (int(len(mcb)/8))
        indice = 0
        for octet in range(0, len(mcb),8):
    
                mon_octet = mcb[octet:octet+8]
                ma_liste[indice]= int(mon_octet,2)
                indice = indice + 1
        return (ma_liste)

def make_error_block(liste, block_number, version, error):        
  error_info=ecccodewords[version][error]
  if block_number<error_info[1]:
    code_words_per_block=error_info[2]
  else:
    code_words_per_block=error_info[4]
  error_block_size=error_info[0]
  
  
  code_words_per_block = error_info[2]
  mp_coeff=liste[:]
  mp_coeff.extend([0]*(error_block_size))
  generator=generator_polynomials[error_block_size]
  
  gen_result=[0]*len(generator)

  for i in range(code_words_per_block):    
    coefficient=mp_coeff.pop(0)
    if coefficient==0:
        continue
    else:
            alpha_exp=galois_antilog[coefficient]
	 
    for n in range(len(generator)):
        gen_result[n]=alpha_exp+generator[n]
        if gen_result[n]>255:
            gen_result[n]=gen_result[n]%255
        gen_result[n]=galois_log[gen_result[n]]
        mp_coeff[n]=gen_result[n]^mp_coeff[n]
  if len(mp_coeff) < code_words_per_block:
        mp_coeff.extend([0] * (code_words_per_block - len(mp_coeff)))
  return mp_coeff

def dec_to_bin(ECC):
        chaine=''
        for i in range(0, len(ECC)):
    
                valeur=binary_repr(ECC[i], 8)
                chaine += valeur
  
        return (chaine)




def main(message,nivECC):
    
    nb_caractere=choix_version(message,nivECC)[0]
    version=choix_version(message,nivECC)[1]

    
    infos = choix_infos_versions(nivECC,'2')
    
    
    message_convertit=conv_8bits(message,version)
    message_convertit=completion((nb_caractere+2),message_convertit)

    
    
    message_polynomial_coefficient=tmp(message_convertit)
    ecc=make_error_block(message_polynomial_coefficient,1,version,nivECC)
    ecc=dec_to_bin(ecc)
    

    
    message_final=concatenation(message_convertit,str(ecc))    

    
    chaine_message=chaine_color(message_final)
    chaine_info=chaine_color(infos)
    
    if version == 1:
        qrv1()
    elif version == 2:
        qrv2()
    elif version == 3:
        qrv3()
    elif version == 4:
        qrv4()
        
        
    placement_formats("image.png",chaine_info)
    placement_module("image.png",chaine_message)
    

    
    matrix("image.png")

