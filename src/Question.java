import java.util.ArrayList;

public class Question {
	String question;
	ArrayList<String> features;
	ArrayList<String> answers;
	String correctAnswer;
	ArrayList<String> wikiAnswers;
	
	/*
	 * Question class definitions
	 */
	public Question(String q) {
		question = q; 
		features = new ArrayList<String>();
		answers = new ArrayList<String>();
		wikiAnswers = new ArrayList<String>();
		correctAnswer = "";
	}
	
	public String toString() {
		return question + "\n" + features + "\n" + answers;
	}
	
	/*
	 * Feature class definitions
	 */
	public ArrayList<String> getFeatures() {
		return features;
	}
	
	public void addFeature(String f) {
		features.add(f);
	}

	class Feature {
		String person;
		String organization;
		String location;
		String date;
		String quote;
		boolean not;
		
	}
	
	
	/*
	 * Answer Class definitions
	 */
	public ArrayList<String> getAnswers() {
		return answers;
	}
	
	public void addAnswer(String a) {
		answers.add(a);
		
		if (a.contains(" "))
			wikiAnswers.add(a.replace(" ", "_"));
		//TODO: write more if cases for wikipedia answers
		else
			wikiAnswers.add(a);
	}
	
	public void setCorrectAnswer(String a) {
		correctAnswer = a;
	}

	class Answer {
		
		
	}
	
}
