package livre;

import java.util.Comparator;
import java.util.Iterator;
import java.util.LinkedList;
import java.util.List;
import java.util.NavigableSet;
import java.util.Set;
import java.util.TreeSet;

import attaque.Pouvoir;
import bataille.Bataille;
import bataille.Camp;
import protagoniste.Domaine;
import protagoniste.Heros;
import protagoniste.Homme;
import protagoniste.Monstre;
import protagoniste.ZoneDeCombat;

public class AideEcrivain {
	private Bataille bataille;
	private List<Homme> listeTriee = new LinkedList<>();
	private NavigableSet<Monstre<? extends Pouvoir>> monstresDeFeu = new TreeSet <Monstre<? extends Pouvoir>>();
	private NavigableSet <Monstre<? extends Pouvoir>> monstresDeGlace = new TreeSet <Monstre<? extends Pouvoir>>();
	private NavigableSet <Monstre<? extends Pouvoir>> monstresTranchants = new TreeSet <Monstre<? extends Pouvoir>>();
	
	private NavigableSet<Monstre<? extends Pouvoir>> monstresDomaineSet = new TreeSet<>(new Comparator<Monstre<? extends Pouvoir>>() {
		public int compare(Monstre<? extends Pouvoir> m1, Monstre<? extends Pouvoir> m2) {
			if(m1.getDomaine() != m2.getDomaine())
				return m1.getDomaine().compareTo(m2.getDomaine());
			else
				return m2.compareTo(m2);
		}
	});
	private NavigableSet<Monstre<? extends Pouvoir>> monstresZoneSet = new TreeSet<>(new Comparator<Monstre<?>>() {
		public int compare(Monstre<? extends Pouvoir> m1, Monstre<?> m2) {
			if (m1.getZoneDeCombat() != m2.getZoneDeCombat())
				return m1.getZoneDeCombat().compareTo(m2.getZoneDeCombat());
			else if (m1.getForceDeVie() != m2.getForceDeVie())
				return m1.getForceDeVie() - m2.getForceDeVie();
			else
				return m1.compareTo(m2);
		}
	});
	
	
	public AideEcrivain(Bataille bataille) {
		this.bataille = bataille;
	}
	
	public String visualiserForcesHumaines () {
		int indiceDebutHero = 0;
		Camp <Homme> campHumain = bataille.getCampHumains();
		Iterator<Homme> it = campHumain.iterator();
		LinkedList <Homme> listeTriee = new LinkedList<Homme>();
		while(it.hasNext()){
		      Homme courant = it.next();
		      if (courant instanceof Heros) 
		      {
		    	  listeTriee.add(indiceDebutHero, courant);
		    	  indiceDebutHero++;
		      }
		      else 
		      {
		    	  listeTriee.add (courant); 
		      }
		}
		return listeTriee.toString();
	}
	
	public String ordreNaturelMonstre() {
		Set<Monstre<? extends Pouvoir>> tableauMonstre = new TreeSet<>();
		Monstre<?> courant;
		for(Iterator<Monstre<? extends Pouvoir>> iterMonstre = bataille.getCampMonstres().iterator(); iterMonstre.hasNext();) {
			courant = iterMonstre.next();
			tableauMonstre.add(courant);
		}
		String resultat = "";
		for(Iterator<Monstre<? extends Pouvoir>> m = bataille.getCampMonstres().iterator(); m.hasNext();) {
			courant = m.next();
			if(m.hasNext()) {
				resultat += courant.getNom() + ", ";
			}
			else {
				resultat += courant.getNom();
			}
		}
		return resultat;
	}
	
	public void updateMonstresDomaine() {
		for(Monstre<? extends Pouvoir> monstre : bataille.getCampMonstres())
			monstresDomaineSet.add(monstre);
	}
	
	public void updateMonstresZone() {
		for (Monstre<? extends Pouvoir> monstre : bataille.getCampMonstres())
			monstresZoneSet.add(monstre);
	}
	
	public String ordreMonstreDomaine () {
		updateMonstresDomaine ();
		String tmpFeu = "FEU : \n";
		String tmpGlace = "\nGLACE : \n";
		String tmpTranchant = "\nTRANCHANT : \n";
		Monstre<?> courant;
		for (Iterator<Monstre<? extends Pouvoir>> it = monstresDomaineSet.iterator();it.hasNext();) {
			courant = it.next();
			if (courant.getDomaine() == Domaine.FEU) {
				if (tmpFeu != "FEU : \n")
					tmpFeu+=", ";
				tmpFeu += courant.getNom();
			}
			else if (courant.getDomaine() == Domaine.GLACE) {
				if (tmpGlace != "\nGLACE : \n")
					tmpGlace+=", ";
				tmpGlace += courant.getNom();
			}
			else {
				if(tmpTranchant != "\nTRANCHANT : \n")
					tmpTranchant+=", ";
				tmpTranchant += courant.getNom();
			}
		}
		return tmpFeu + tmpGlace + tmpTranchant; 
	}
	
	public String ordreMonstreZone () {
		updateMonstresZone ();
		String tmpAeri = "AERIEN : \n";
		String tmpAqua = "\nAQUATIQUE : \n";
		String tmpTerre = "\nTERRESTRE : \n";
		for (Iterator<Monstre<? extends Pouvoir>> it = monstresZoneSet.iterator();it.hasNext();) {
			Monstre<?> m = it.next();
			if (m.getZoneDeCombat() == ZoneDeCombat.AERIEN) {
				if (tmpAeri != "AERIEN : \n")
					tmpAeri+=", ";
				tmpAeri += m.getNom() + " : " + m.getForceDeVie();
			}
			else if (m.getZoneDeCombat() == ZoneDeCombat.AQUATIQUE) {
				if (tmpAqua != "\nAQUATIQUE : \n")
					tmpAqua+=", ";
				tmpAqua += m.getNom() + " : " + m.getForceDeVie();
			}
			else {
				if(tmpTerre != "\nTERRESTRE : \n")
					tmpTerre+=", ";
			tmpTerre += m.getNom() + " : " + m.getForceDeVie();
			}
		}
		return tmpAeri+tmpAqua+tmpTerre;
	  }
	
	
/*	public Monstre<?> firstMonstreDomaine (Domaine dom ){
		for (Monstre<?> monstre: monstresDomaineSet) {
			if (monstre.getDomaine() == dom) {
				return monstre;
			}
			else {
				monstresDeFeu.add(monstre);
			}
		}
		return null;
	}
	public void initMonstresDeFeu() {
		monstresDeFeu = monstresDomaineSet.headSet(firstMonstreDomaine(Domaine.GLACE), false);
	}*/
	
	public void initMonstresDeFeu() {
		monstresDeFeu = monstresDomaineSet.headSet(new Monstre<>(" ",0,null,Domaine.GLACE), false);
		
	}
	
	public void initMonstresDeGlace() {
		
		monstresDeGlace = monstresDomaineSet.subSet(new Monstre<>(" ", 0, null, Domaine.GLACE), true, new Monstre<>(" ", 0, null, Domaine.TRANCHANT), false);
		
	}
	
	public void initMonstresTranchant() {
		monstresTranchants = monstresDomaineSet.tailSet(new Monstre<>(" ", 0, null, Domaine.TRANCHANT), true);
	}
	
	
	public NavigableSet<Monstre<?>> getMonstresDeFeu() {
		updateMonstresDomaine();
		initMonstresDeFeu();
		return monstresDeFeu;
	}

	public NavigableSet<Monstre<?>> getMonstresDeGlace() {
		updateMonstresDomaine();
		initMonstresDeGlace();
		return monstresDeGlace;
	}

	public NavigableSet<Monstre<?>> getMonstresTranchants() {
		updateMonstresDomaine();
		initMonstresTranchant();
		return monstresTranchants;
	}

	
}
