import java.util.ArrayList;

public class Pipeline {
	public static void main (String[] args) throws Exception {
		FileReader fr = new FileReader("hq_data.txt");
		ArrayList<Question> questions = fr.questions;
		
		/*
		 * Question 0:
		 *Which NBA franchise has NOT retired any jersey numbers?
		 * #		retired
		 * #		jersey
		 * #		numbers
		 * #		NOT
		 *		Brooklyn Nets
		 *		Dallas Mavericks
		 *		Los Angeles Clippers
		 */
		
		Question q0 = questions.get(0);
		WikiAnswerModel wiki0 = new WikiAnswerModel(q0);
		
		System.out.println("Question = " + q0.question);
		System.out.println("Features = " + q0.features);
		System.out.println("Answer Choices = " + q0.answers);
		System.out.println("Total Cooccurrences = " + wiki0.cooccurrence + "\n");
		
		System.out.println("My guess is: " + wiki0.guess + "\n");
		
		Question q1 = questions.get(1);
		WikiAnswerModel wiki1 = new WikiAnswerModel(q1);
		
		System.out.println("Question = " + q1.question);
		System.out.println("Features = " + q1.features);
		System.out.println("Answer Choices = " + q1.answers);
		System.out.println("Total Cooccurrences = " + wiki1.cooccurrence + "\n");
		System.out.println("My guess is: " + wiki1.guess + "\n");
		
		Question q2 = questions.get(2);
		WikiAnswerModel wiki2 = new WikiAnswerModel(q2);
		
		System.out.println("Question = " + q2.question);
		System.out.println("Features = " + q2.features);
		System.out.println("Answer Choices = " + q2.answers);
		System.out.println("Total Cooccurrences = " + wiki2.cooccurrence + "\n");
		System.out.println("My guess is: " + wiki2.guess + "\n");
		
		
		//System.out.println(q.answers.get(0) + " Cooccurrence = " + wiki.cooccurrence.get(0));
		//System.out.println(q.answers.get(1) + " Cooccurrence = " + wiki.cooccurrence.get(1));
		//System.out.println(q.answers.get(2) + " Cooccurrence = " + wiki.cooccurrence.get(2));
		
		
	}
}
