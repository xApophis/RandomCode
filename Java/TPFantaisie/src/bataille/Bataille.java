package bataille;

import attaque.Pouvoir;
import protagoniste.Homme;
import protagoniste.Monstre;

public class Bataille {
	private Camp<Homme> campHumains = new Camp<>();
	private Camp<Monstre<?>> campMonstres = new Camp<>();
	
	public void ajouter(Homme homme) {
		campHumains.ajouter(homme);
	}
	public void eliminer(Homme homme) {
		campHumains.eliminer(homme);
	}
	public void ajouter(Monstre<? extends Pouvoir> monstre) {
		campMonstres.ajouter(monstre);
	}
	public void eliminer(Monstre<? extends Pouvoir> monstre) {
		campMonstres.eliminer(monstre);
	}
	public Camp<Homme> getCampHumains() {
		return campHumains;
	}
	public Camp<Monstre<?>> getCampMonstres() {
		return campMonstres;
	}
	
}
