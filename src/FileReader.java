import java.io.BufferedReader;
import java.io.FileInputStream;
import java.io.InputStreamReader;
import java.util.ArrayList;

public class FileReader {
	ArrayList<Question> questions;

	public FileReader(String fileName) {
		try {
			FileInputStream fstream = new FileInputStream(fileName);
			BufferedReader br = new BufferedReader(new InputStreamReader(fstream));
			String line;
			questions = new ArrayList<Question>();
			Question q = new Question("");

			while ((line = br.readLine()) != null) {
				//Question
				if(line.matches("^[A-Z].*$")) {
					q = new Question(line);
				}
				else if (line.contains("\t")) {
					//Feature
					if (line.startsWith("#")) {
						q.addFeature(line.substring(1, line.length()).trim());
					}
					//Correct Answer
					else if (line.startsWith("*")) {
						String answer = line.substring(1, line.length()).trim();
						q.addAnswer(answer);
						q.setCorrectAnswer(answer);
					}
					//Wrong Answer
					else {
						q.addAnswer(line.trim());
					}
				}
				//New Line
				else {
					questions.add(q);
				}
			}
			fstream.close();
			System.out.println("Successfully read file!\n");
		} catch (Exception e) {
			System.err.println("Error: " + e.getMessage());
		}
	}
}
