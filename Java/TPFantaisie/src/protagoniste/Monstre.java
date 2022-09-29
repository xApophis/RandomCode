package protagoniste;
import java.util.Arrays;
import java.util.Iterator;
import java.util.Random;

import attaque.Pouvoir;
import bataille.Bataille;

public class Monstre <P extends Pouvoir> extends EtreVivant implements Iterable<P>{
	private P[] attaques;
	private ZoneDeCombat zoneDeCombat;
	private Domaine domaine;
	private Iterator<P> gestionAttaque;

	@SafeVarargs
	public Monstre(String nom, int forceDeVie, ZoneDeCombat zoneDeCombat, 
			Domaine domaine, P...attaques) {
		super(nom, forceDeVie);
		this.attaques = attaques;
		this.zoneDeCombat = zoneDeCombat;
		this.domaine = domaine;
	}
	public ZoneDeCombat getZoneDeCombat() {
		return zoneDeCombat;
	}
	public Domaine getDomaine() {
		return domaine;
	}
	public void entreEnCombat() {
		for(int i = 0; i < attaques.length; i++) {
				attaques[i].regenererPouvoir();
		}
		gestionAttaque = iterator();
	}
	public P attaque() {
		if(gestionAttaque.hasNext()) {
			return gestionAttaque.next();
		}
		return null;
	}
	public Iterator<P> iterator() {
		return new GestionAttaque();
	}
	@Override
	public String toString() {
		return "Monstre [getNom()="+ this.getNom()+", attaques=" + Arrays.toString(attaques) + ", zoneDeCombat=" + zoneDeCombat + ", getForceDeVie()="
				+ this.getForceDeVie() + "]";
	}
	
	public void rejointBataille(Bataille bataille) {
		super.rejointBataille(bataille);
		bataille.ajouter(this);
	}
	
	public void mourir(Bataille bataille) {
		bataille.eliminer(this);
	}


	private class GestionAttaque implements Iterator<P>{
		private P[] attaquesPossibles;
		private int nbAttaquesPossibles;

		public GestionAttaque() {
			attaquesPossibles = attaques;
			nbAttaquesPossibles = attaques.length;
		}
		public boolean hasNext() {
			for(int i = 0; i < nbAttaquesPossibles; i++) {
				if(attaquesPossibles[i].isOperationnel() == false) {
				attaquesPossibles[i] = attaquesPossibles[nbAttaquesPossibles - 1];
				nbAttaquesPossibles--;
				}
			}
			return nbAttaquesPossibles != 0;
		}
		public P next() {
			return attaquesPossibles[new Random().nextInt(nbAttaquesPossibles)];
		}
	}
}
