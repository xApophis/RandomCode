package bataille;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.HashSet;
import java.util.LinkedHashMap;
import java.util.LinkedList;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Random;

import attaque.Pouvoir;
import protagoniste.Monstre;
import protagoniste.ZoneDeCombat;

public class Grotte {
	private LinkedHashMap<Salle, List<Salle>> planGrotte = new LinkedHashMap<>();
	private HashMap<Salle,Bataille> batailles = new HashMap<>();
	private HashSet<Salle> sallesExplorees = new HashSet<>();
	private int numeroSalleDecisive;
	
	public void ajouterSalle(ZoneDeCombat zoneDeCombat, Monstre<? extends Pouvoir>... monstres) {
		Salle s = new Salle(planGrotte.size(), zoneDeCombat);
		Bataille b = new Bataille();
		
		for(Monstre<? extends Pouvoir> m : monstres) {
			b.ajouter(m);;
		}
		planGrotte.put(s, new ArrayList<Salle>());
		batailles.put(s,b);
	}
	
	public String afficherPlanGrotte() {
		String affichage = "";
		for (Map.Entry<Salle, List<Salle>> entry : planGrotte.entrySet()) {
			Salle salle = entry.getKey();
			List<Salle> acces = planGrotte.get(salle);
			affichage += ("La " + salle + ".\nElle possede " + acces.size() + " acces : ");
			for (Salle access : acces) {
				affichage += (" vers la " + access);
			}
			Bataille bataille = batailles.get(salle);
			Camp<Monstre<? extends Pouvoir>> camp = bataille.getCampMonstres();
			Monstre<?> monstre = camp.selectionner();
			if (camp.nbCombattants() > 1) {
				affichage += ("\n" + camp.nbCombattants() + " monstres de type ");
			} else {
				affichage += ("\nUn monstre de type ");
			}
			affichage += (monstre.getNom() + " la protege.\n");
			if (salle.getNumSalle() == numeroSalleDecisive) {
				affichage += ("C'est dans cette salle que se trouve la pierre de sang.\n");
			}
			affichage += ("\n");
		  	}
		 return affichage.toString();
	}
	
	public void setNumeroSalleDecisive(int numeroSalleDecisive) {
		this.numeroSalleDecisive = numeroSalleDecisive;
	}
	
	public Salle trouverSalle (int numeroSalle) {
		for (Map.Entry<Salle, List<Salle>> entry :planGrotte.entrySet()) {
			Salle s = entry.getKey();
			if (s.getNumSalle()+1 == numeroSalle) {
				return s;  
			}
		}
		return null;
	}
	
	public void configurerAcces(int numSalleBase, int... salles) {
		Salle salleBase = trouverSalle(numSalleBase);
		List<Salle> listeSalle = this.planGrotte.get(salleBase);
		for(int numSalle:salles) {
			listeSalle.add(trouverSalle(numSalle));
		}
	}
	
	public Boolean salleDecisive(Salle salle) {
		return trouverSalle(this.numeroSalleDecisive) == salle;
	}
	
	public Salle premiereSalle() {
		this.sallesExplorees.add(trouverSalle(1));
		return trouverSalle(1);
	}
	
	public Salle salleSuivante(Salle currentSalle) {
        List<Salle> SallesDispo = new LinkedList<>();
        
        for(Salle s : this.planGrotte.get(currentSalle)) {
            if(! this.sallesExplorees.contains(s)) {
                SallesDispo.add(s);
            }
        }
        
        if(SallesDispo.isEmpty()) {
            SallesDispo = this.planGrotte.get(currentSalle) ;
        }
        
        int rand = (new Random()).nextInt(SallesDispo.size());
        
        Salle sSuiv = SallesDispo.get(rand);
        
        sallesExplorees.add(currentSalle);
        
        return sSuiv;
    }
	
}
