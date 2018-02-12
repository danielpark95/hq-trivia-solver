import edu.stanford.nlp.pipeline.*;
import edu.stanford.nlp.coref.CorefCoreAnnotations.CorefChainAnnotation;
import edu.stanford.nlp.coref.data.CorefChain;
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
import java.util.*;

class Pipeline {
	class data {
		String question;
		String[] answers;
		int correctAnswer;
	}
	
	
    public static void main(String[] args) {
        System.out.println("Building pipeline...");
        // creates a StanfordCoreNLP object, with POS tagging, parsing
        Properties props = new Properties();
        props.setProperty("annotators", "tokenize, ssplit, pos, lemma, ner, parse, natlog, openie");
        StanfordCoreNLP pipeline = new StanfordCoreNLP(props);
        System.out.println("Built pipline!");

        // read some text in the text variable
        String text = "In which college class would you be most likely to study a syzygy?";
        
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
	       // traversing the words in the current sentence
	       // a CoreLabel is a CoreMap with additional token-specific methods
	       for (CoreLabel token: sentence.get(TokensAnnotation.class)) {
	         // this is the text of the token
	         String word = token.get(TextAnnotation.class);
	         // this is the POS tag of the token
	         String pos = token.get(PartOfSpeechAnnotation.class);
	         // this is the NER label of the token
	         String ne = token.get(NamedEntityTagAnnotation.class);
	         System.out.println("word = " + word + ", pos = " + pos + ", ne = " + ne);
	       }
	
	       // this is the parse tree of the current sentence
	       Tree tree = sentence.get(TreeAnnotation.class);
	       System.out.println("Parse tree = " + tree.toString());
	
	       // this is the Stanford dependency graph of the current sentence
	       SemanticGraph dependencies = sentence.get(BasicDependenciesAnnotation.class);
	       System.out.println("Dependencies = " + dependencies.toString());
	     }
	
	     // This is the coreference link graph
	     // Each chain stores a set of mentions that link to each other,
	     // along with a method for getting the most representative mention
	     // Both sentence and token offsets start at 1!
	     Map<Integer, CorefChain> graph = 
	       document.get(CorefChainAnnotation.class);
	    }
}