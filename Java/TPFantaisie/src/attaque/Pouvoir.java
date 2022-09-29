package attaque;

public class Pouvoir extends ForceDeCombat{
	private int nbUbtilisationPouvoir;
	private int nbUtilisationPouvoirInitial;
	
	public Pouvoir(int pointDeDegat, String nom, int nbUtilisationPouvoir) {
		super(pointDeDegat, nom);
		this.nbUbtilisationPouvoir=nbUtilisationPouvoir;
	}
	
	public void regenererPouvoir() {
		this.nbUbtilisationPouvoir = nbUtilisationPouvoirInitial;
		operationnel = true;
	}
	
	public int utiliser() {
		if(nbUbtilisationPouvoir == 0)
			operationnel = false;
		else
			nbUbtilisationPouvoir--;
		return nbUbtilisationPouvoir;
	}
}
