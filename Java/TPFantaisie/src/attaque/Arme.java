package attaque;

import java.util.HashSet;

import protagoniste.ZoneDeCombat;

public class Arme extends ForceDeCombat implements Orderable<Arme>{
	private HashSet<ZoneDeCombat> zonesDeCombat = new HashSet<>();
	
	public Arme(int pointDeDegat, String nom, ZoneDeCombat...combats) {
		super(pointDeDegat, nom);
		for(ZoneDeCombat z : combats) {
			this.zonesDeCombat.add(z);
		}
	}

	public HashSet<ZoneDeCombat> getZonesDeCombat() {
		return zonesDeCombat;
	}
	
	public int compareTo(Arme arme) {
		int res = 0;
		if (this.isOperationnel() == arme.isOperationnel()) {
			if (this.getPointDeDegat() == arme.getPointDeDegat()) {
				res = this.getNom().compareTo(arme.getNom());
			} else {
				res = this.getPointDeDegat() - arme.getPointDeDegat();
			}
		} else {
			res = this.isOperationnel() ? 1 : -1;
		}
		return res;
	}

}
