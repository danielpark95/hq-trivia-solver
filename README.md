## HQ Trivia Solver
Basic pipeline for answering trivia questions from the popular mobile game HQ with Stanford CoreNLP API and Google Custom Search API in Java.

## Sample Questions
Which organization began as the North West Police Agency?  
	FBI	  
	NRA  
	Pinkerton*  

Stanford CoreNLP's Named Entity Recognition annotator identifies "North West Police Agency" as an organization, so we can query to Google Custom Search with each of the answer choices to see which choice is the most probable.

Another useful annotator I started using is the Open Information Extraction (Open IE), its use is shown below:

In which college class would you be most likely to study a syzygy?  
	Astronomy*  
	Philosophy  
	Russian  

Open IE returns subject entity "In which college class would you be most likely" with relation "study" and object entity "syzygy". Then we would search either the subject or object entity (the one that doesn't have which/what/how/where/etc) with answer choices and assign a probability distribution over the answer choices.

Using the second question as an example, CoreNLP also produces the following dependenies and parse trees that can be used for determining key words/phrases:

Dependencies = -> likely/JJ (root)  
  -> class/NN (nmod)  
    -> In/IN (case)  
    -> which/WDT (det)  
    -> college/NN (compound)  
  -> would/MD (aux)  
  -> you/PRP (nsubj)  
  -> be/VB (cop)  
  -> most/RBS (advmod)  
  -> study/VB (xcomp)  
    -> to/TO (mark)  
    -> syzygy/NN (dobj)  
      -> a/DT (det)  
  -> ?/. (punct)  

Parse tree = (ROOT (SBARQ (WHPP (IN In) (WHNP (WDT which) (NN college) (NN class))) (SQ (MD would) (NP (PRP you)) (VP (VB be) (ADJP (RBS most) (JJ likely) (S (VP (TO to) (VP (VB study) (NP (DT a) (NN syzygy)))))))) (. ?)))
