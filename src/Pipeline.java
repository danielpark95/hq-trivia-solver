import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.ling.CoreAnnotations.NamedEntityTagAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.PartOfSpeechAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.SentencesAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TextAnnotation;
import edu.stanford.nlp.ling.CoreAnnotations.TokensAnnotation;
import edu.stanford.nlp.ling.CoreLabel;
import edu.stanford.nlp.semgraph.SemanticGraph;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.BasicDependenciesAnnotation;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreeCoreAnnotations.TreeAnnotation;
import edu.stanford.nlp.util.CoreMap;
import edu.stanford.nlp.util.PropertiesUtils;

import java.util.*;

/**
 * Pipeline
 *
 * @author Daniel Park
 */
class Pipeline {
	
	public SemanticGraph ExtractKeyPhrase (SemanticGraph dependencies) {
		return dependencies;
	}

	public static void main(String[] args) {
		//Import file and retrieve questions
		String fileName = "hq_data.txt";
		FileHandler fh = new FileHandler(fileName);
		ArrayList<Question> questions = fh.getQuestions();

		System.out.println("Building pipeline...");
		// creates a StanfordCoreNLP object, with POS tagging, parsing
		Properties props = new Properties();
		props.setProperty("annotators", "tokenize, ssplit, parse, lemma, ner");
		props.setProperty("parse.model", "edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz"); //Lexicalized PCFG parser
		props.setProperty("parse.maxlen", "30");

		StanfordCoreNLP pipeline = new StanfordCoreNLP(props);

		System.out.println("Built pipline!");

		// read some text in the text variable
		String text = 
				"In which college class would you be most likely to study a syzygy? " + 
						"In 2017, what did Twitter do to its 140-character limit on tweets? " +
						"On a compass, what does the letter N typically stand for? " +
						"In which profession would you be most likely to use a psychrometer? ";
		System.out.println("Text = " + text);

		// create an empty Annotation just with the given text
		Annotation document = new Annotation(text);
		System.out.println("Created Annotation document.");

		// run all Annotators on this text
		pipeline.annotate(document);

		System.out.println("Ran all Annotators on the text");

		// these are all the sentences in this document
		// a CoreMap is essentially a Map that uses class objects as keys and has values with custom types
		List<CoreMap> sentences = document.get(SentencesAnnotation.class);
		for(CoreMap sentence: sentences) {
			CoreLabel remove_token = new CoreLabel();

			// traversing the words in the current sentence
			// a CoreLabel is a CoreMap with additional token-specific methods
			for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
				// this is the text of the token
				String word = token.get(TextAnnotation.class);

				// this is the POS tag of the token
				String pos = token.get(PartOfSpeechAnnotation.class);
				if (pos.equals("WDT"))
					remove_token = token;
				// this is the NER label of the token
				String ne = token.get(NamedEntityTagAnnotation.class);
				System.out.println("word = " + word + ", pos = " + pos + ", ne = " + ne);
			}

			String label_WDT = "WDT";

			// this is the parse tree of the current sentence
			Tree tree = sentence.get(TreeAnnotation.class);			
			System.out.println("Parse tree = \n" + tree.toString());


			// this is the Stanford dependency graph of the current sentence
			SemanticGraph dependencies1 = sentence.get(BasicDependenciesAnnotation.class);
			System.out.println("Basic Dependencies = \n" + dependencies1.toString());
			System.out.println("List = \n" + dependencies1.toList());
			System.out.println("POS List = \n" + dependencies1.toPOSList());
			System.out.println("Nodes by POS = \n" + dependencies1.getAllNodesByPartOfSpeechPattern("WDT").toString());
			System.out.println("Leaf vertices = \n" + dependencies1.getLeafVertices().toString());

			//remove words
			//IndexedWord remove_word = new IndexedWord(remove_token);
			//dependencies1.removeVertex(remove_word);
			//System.out.println("Removed Token = \n" + dependencies1.toString());			
		}
	}
}