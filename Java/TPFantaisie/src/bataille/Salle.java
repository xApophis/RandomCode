package bataille;

import java.util.Objects;

import protagoniste.ZoneDeCombat;

public class Salle {
	private int numSalle;
	private ZoneDeCombat zoneDeCombat;
	
	public Salle(int numSalle, ZoneDeCombat zoneDeCombat) {
		this.numSalle = numSalle;
		this.zoneDeCombat = zoneDeCombat;
	}

	public int getNumSalle() {
		return numSalle;
	}

	public ZoneDeCombat getZoneDeCombat() {
		return zoneDeCombat;
	}

	@Override
	public String toString() {
		return "Salle n°" + numSalle + " de type combat " + zoneDeCombat;
	}

	@Override
	public int hashCode() {
		return Objects.hash(numSalle);
	}
	
}
