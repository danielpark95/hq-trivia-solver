import java.util.ArrayList;

public class Question {
	String question;
	ArrayList<String> features;
	ArrayList<String> answers;
	
	public Question(String q) {
		question = q;
		features = new ArrayList<String>();
		answers = new ArrayList<String>();
	}
	
	public String getQuestion() {
		return question;
	}
	
	public ArrayList<String> getFeatures() {
		return features;
	}
	
	public void addFeature(String f) {
		features.add(f);
	}
	public ArrayList<String> getAnswers() {
		return answers;
	}
	
	public void addAnswer(String a) {
		answers.add(a);
	}
	
	class Feature {
		String person;
		String organization;
		String location;
		String date;
		String quote;
		boolean not;
		
	}
	
	class Answer {
		
		
	}
	
	public String toString() {
		return question + "\n" + features + "\n" + answers;
	}
	
	
	
}
