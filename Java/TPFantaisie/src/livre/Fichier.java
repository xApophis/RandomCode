package livre;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

public class Fichier implements Livre {

	@Override
	public void ecrire(String s) {
		/*String chemin = "./src/livre/histoire.txt";
		File writer = new File(chemin);
		try {
			FileWriter fichier = new FileWriter(writer, true);
			try {
				fichier.write(s);
			} finally {
				fichier.close();
			}
		} catch (IOException e) {
			e.printStackTrace();
		}*/
		
		String chemin = "./src/livre/histoire.txt";
		File writer = new File(chemin);
		try(FileWriter fichier = new FileWriter(writer, true)) {
			fichier.write(s);
		} catch (IOException e) {
			e.printStackTrace();
		}

	}

}