package protagoniste;

import java.util.ArrayList;
import java.util.EnumMap;
import java.util.List;
import java.util.Map;
import java.util.NavigableSet;
import java.util.SortedSet;
import java.util.TreeSet;

import attaque.Arme;
import attaque.Pouvoir;
import bataille.Bataille;

public class Homme extends EtreVivant{
	private Map<ZoneDeCombat, List<Arme>> armes;
	private Arme armeChoisie;
	
	public Homme(String nom) {
		super(nom, 70);
		armes = new EnumMap<ZoneDeCombat, List<Arme>>(ZoneDeCombat.class);
		for (ZoneDeCombat keyZone : ZoneDeCombat.values()) {
			armes.put(keyZone, new ArrayList<>());
		}
	}
	public void rejointBataille(Bataille bataille) {
		super.rejointBataille(bataille);
		bataille.ajouter(this);
	}
	public void mourir(Bataille bataille) {
		bataille.eliminer(this);
	}
	@Override
	public String toString() {
		return "Homme [nom=" + nom + ", forceDeVie=" + forceDeVie + "]";
	}
	
	public void ajouterArmes(Arme... armesAAjouter) {
		for (Arme a : armesAAjouter) {
			for (ZoneDeCombat z : a.getZonesDeCombat()) {
				armes.get(z).add(a);
			}
		}
	}
	
	/*public void ajouterArmes(Arme... armeAAjouter) {
        List<Arme> listeAerien= new ArrayList<>();
        List<Arme> listeAquatique=new ArrayList<>();
        List<Arme> listeTerrestre=new ArrayList<>();
        
        for (Arme a : armeAAjouter) {
            if (armes.getClass() = Arc.Class()) {
                listeAerien.add(arme)
            }
            if (armes.containsKey(ZoneDeCombat.AQUATIQUE)) {
                listeAquatique=armes.get(ZoneDeCombat.AQUATIQUE);
            }
            if (armes.containsKey(ZoneDeCombat.TERRESTRE)) {
                listeTerrestre=armes.get(ZoneDeCombat.TERRESTRE);
            }
        }
        System.out.println(liste1);
        System.out.println(liste2);
        System.out.println(liste3);
      }*/
	
	public void supprimerArme(Arme armeASuppr) {
		for(ZoneDeCombat combatzone:armeASuppr.getZonesDeCombat()) {
			armes.get(combatzone).remove(armeASuppr);
		}
	}
	
	public Arme choisirArme(Monstre<? extends Pouvoir> monstreACombattre) {
		Arme armeChoisie = null;
		List<Arme> listeArmes = armes.get(monstreACombattre.getZoneDeCombat());
		if (!listeArmes.isEmpty()) {
			NavigableSet<Arme> armesTriees = new TreeSet<>(listeArmes);
			SortedSet<Arme> armesAdaptees = armesTriees.tailSet(new KeyArme(monstreACombattre.getForceDeVie(), ""));
			if (!armesAdaptees.isEmpty()) {
				armeChoisie = armesAdaptees.first();
			} else {
				armeChoisie = armesTriees.last();
			}
		}
		return armeChoisie;
	}
	
	public Arme getArmeChoisie() {
		return armeChoisie;
	}

}
