package bataille;

import java.util.Comparator;
import java.util.LinkedList;
import java.util.List;
import java.util.SortedMap;
import java.util.TreeMap;
import java.util.TreeSet;

import attaque.Arme;
import attaque.Pouvoir;
import protagoniste.Homme;
import protagoniste.Monstre;

public class GroupeHommes {

	private TreeSet<Homme> groupe;

	public GroupeHommes() {
		groupe = new TreeSet<Homme>();
	}

	public void ajouterHommes(Homme... hommes) {
		for (Homme h : hommes) {
			groupe.add(h);
		}
	}

	public List<Homme> choixCampHomme(Bataille bataille) {
		Monstre<? extends Pouvoir> monstre = bataille.getCampMonstres().selectionner();
		TreeMap<Arme, TreeSet<Homme>> hommesArmes = new TreeMap<>(new ComparateurArmes(monstre));
		for (Homme h : groupe) {
			Arme armeSelectionnee = h.choisirArme(monstre);
			if (armeSelectionnee != null) {
				if (!hommesArmes.containsKey(armeSelectionnee)) {
					hommesArmes.put(armeSelectionnee, new TreeSet<>(new ComparateurHommes()));
				}
				hommesArmes.get(armeSelectionnee).add(h);
			}
		}
		List<Homme> hommesSelectionnes = new LinkedList<Homme>();
		while (hommesSelectionnes.size() != 3 && !hommesArmes.isEmpty()) {
			for (Homme h : hommesArmes.get(hommesArmes.firstKey())) {
				if (hommesSelectionnes.size() < 3) {
					hommesSelectionnes.add(h);
					h.rejointBataille(bataille);
					bataille.ajouter(h);
				}
			}
			hommesArmes.remove(hommesArmes.firstKey());//FAIRE UN ITERATEUR
		}
		return hommesSelectionnes;
	}

	public class ComparateurHommes implements Comparator<Homme> {

		@Override
		public int compare(Homme homme1, Homme homme2) {
			int compare = 0;
			if (homme1.getForceDeVie() == homme2.getForceDeVie()) {
				compare = homme1.compareTo(homme2);
			} else {
				compare = homme2.getForceDeVie() - homme1.getForceDeVie();
			}
			return compare;
		}

	}

	public class ComparateurArmes implements Comparator<Arme> {
		private Monstre<? extends Pouvoir> monstre;

		public ComparateurArmes(Monstre<? extends Pouvoir> m) {
			monstre = m;
		}

		@Override
		public int compare(Arme arme1, Arme arme2) {
			int compare = 0;
			if (arme1.getPointDeDegat() != arme2.getPointDeDegat()) {
				TreeMap<Integer, Arme> classementForce = new TreeMap<>();
				classementForce.put(arme1.getPointDeDegat(), arme1);
				classementForce.put(arme2.getPointDeDegat(), arme2);
				SortedMap<Integer, Arme> armesValables = classementForce.tailMap(monstre.getForceDeVie());
				if (armesValables.isEmpty()) {
					compare = arme2.getPointDeDegat() - arme1.getPointDeDegat();
				} else {
					compare = (armesValables.get(armesValables.firstKey()) == arme2) ? 1 : -1;
				}
			} else {
				compare = arme1.compareTo(arme2);
			}
			return compare;
		}
	}
}
