#-*-coding:UTF-8-*-
import cherrypy
from fonctions_qrcode import *
class QRCodeGenerator(object):


    @cherrypy.expose
    def index(self):
        
        return '''<!DOCTYPE html><html><head><meta charset="ISO-8859-15:45 12/05/2016"><title>Générateur QR-Code</title><link rel="stylesheet" type="text/css" href="QRCode.css"></head><body><h1>Générateur de QR-Code</h1><label for="message">Message que vous voulez intégrer dans un QR-Code :</label><br /><form action="demarrer" method="GET"><textarea id="Saisissez votre texte" maxlength="300" class="input_saisie_text" type="text" name="message" style="width:300px; height:110px" align="top" value="Saisissez votre texte" placeholder="Saisissez votre texte"></textarea><select name="nivECC" type="submit"><option>--Choissez votre niveau de correction d'erreur--</option><option id="ECC1" value="L">Niveau de correction faible</option><option id="ECC2" value="M">Niveau de correction moyen</option><option id="ECC3" value="Q">Niveau de correction fort</option><option id="ECC4" value="H">Niveau de correction très fort</option></select><button name="generer">QR-Code</button></form><p>Les limites de caractères sont de: 78 caractères pour le niveau faible, 42 pour le niveau moyen, 11 pour le niveau fort et 7 pour le niveau très fort</p>'''

    index.exposed=True
    
    
    def demarrer(self,generer,message,nivECC):
        main(message,nivECC)
        return '''<html><title>QR-Code pour votre message</title> <p><img src="image.png"/></p></html>'''
    demarrer.exposed=True

cherrypy.quickstart(QRCodeGenerator(),config="config.conf")



