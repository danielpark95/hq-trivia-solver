import edu.stanford.nlp.ling.HasWord;
import edu.stanford.nlp.parser.lexparser.LexicalizedParser;
import edu.stanford.nlp.parser.nndep.DependencyParser;
import edu.stanford.nlp.process.DocumentPreprocessor;
import edu.stanford.nlp.semgraph.SemanticGraphCoreAnnotations.BasicDependenciesAnnotation;
import edu.stanford.nlp.tagger.maxent.MaxentTagger;
import edu.stanford.nlp.trees.GrammaticalStructure;
import edu.stanford.nlp.trees.GrammaticalStructureFactory;
import edu.stanford.nlp.trees.PennTreebankLanguagePack;
import edu.stanford.nlp.trees.Tree;
import edu.stanford.nlp.trees.TreebankLanguagePack;
import edu.stanford.nlp.trees.TypedDependency;

import java.io.StringReader;
import java.util.Collection;
import java.util.List;

/**
 * Demonstrates how to first use the tagger, then use the NN dependency
 * parser. Note that the parser will not work on untagged text.
 *
 * @author Daniel Park
 */
public class Parse  {

	public static void main(String[] args) {
		String text = "Which animals race at the Kentucky Derby? ";

		//POS Tagger
		MaxentTagger tagger = new MaxentTagger("edu/stanford/nlp/models/pos-tagger/english-left3words/english-left3words-distsim.tagger");
		
		//Dependency Parser
		DependencyParser parser = DependencyParser.loadFromModelFile(DependencyParser.DEFAULT_MODEL);

		//PCFG Parser
		LexicalizedParser lp = LexicalizedParser.loadModel(
				"edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz",
				"-maxLength", "80", "-retainTmpSubcategories");
		
		//PennTreebankLanguagePack with Universal Dependency.
		TreebankLanguagePack tlp = new PennTreebankLanguagePack();
		tlp.setGenerateOriginalDependencies(true); //set to false for Stanford Dependency
		
		//Factory for making GrammaticalStructures with custom language pack and dependency.
		GrammaticalStructureFactory gsf = tlp.grammaticalStructureFactory();
		
		DocumentPreprocessor tokenizer = new DocumentPreprocessor(new StringReader(text));
		for (List<HasWord> sentence : tokenizer) {
			//Parse sentence using LexicalizedParser of choice (PCFG seems to work well).
			Tree parseTree = lp.apply(sentence);
			System.out.println(parseTree.toString());
			
			//Store dependency relations between nodes in a tree.
			GrammaticalStructure gs = gsf.newGrammaticalStructure(parseTree);
			
			//SemanticGraph dependencies = sentence.get(BasicDependenciesAnnotation.class);
			
			//Generate dependency relations between word pairs in the order they appear in sentence.
			Collection<TypedDependency> tdl = gs.typedDependenciesCCprocessed();
			System.out.println(tdl);
		}
	}
}