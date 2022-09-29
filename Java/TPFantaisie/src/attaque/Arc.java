package attaque;

public class Arc extends Arme{
	private int nbFlechesRestantes;
	
	public Arc(int nbFlechesRestantes) {
		super(50, "Arc");
		this.nbFlechesRestantes=nbFlechesRestantes;
	}
	
	public int utiliser() {
		if(nbFlechesRestantes == 0)
			operationnel = false;
		else 
			nbFlechesRestantes--;
		return nbFlechesRestantes;
	}
}
