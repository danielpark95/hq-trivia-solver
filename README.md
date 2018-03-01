## HQ Trivia Solver
Program for answering trivia questions from the popular mobile game HQ with Stanford CoreNLP API, MediaWiki API, and Google Custom Search API in Java.

## Program Demo
***1.*** Question: Which NBA franchise has NOT retired any jersey numbers?  
Answer Choices: [Brooklyn Nets, Dallas Mavericks, Los Angeles Clippers]  
  
My guess is: Los Angeles Clippers  

***2.*** Question: Which of these is a standard cheerleading jump?  
Answer Choices: [Herkie, Flap, Striker]  
  
My guess is: Herkie  

***3.*** Question: Which of these international foods is NOT a kind of dumpling?  
Answer Choices: [Pelmeni, Pecel, Pierogi]  
  
My guess is: Pecel  
  
## NLP
***Named Entity Recognition:***  
>Question = "Which of these agencies began as the North West Police Agency?"  
>NER Output = {"North West Police Agency" - organization}.  

***Open Information Extraction:***   
>Question = "In which college class would you be most likely to study a syzygy?"  
>OpenIE Output = {"you" /subj, "study" /relation, "syzygy" /obj}  

Open IE returns subject entity "you" with relation "study" and object entity "syzygy". We choose either the subject or object entity (the one that doesn't have which / what / how / where / etc) and use it as a feature for our model.  
  
***Grammatical Dependencies:***  
>Dependencies = -> likely/JJ (root)  
>  -> class/NN (nmod)  
>    -> In/IN (case)  
>    -> which/WDT (det)  
>    -> college/NN (compound)  
>  -> would/MD (aux)  
>  -> you/PRP (nsubj)  
>  -> be/VB (cop)  
>  -> most/RBS (advmod)  
>  -> study/VB (xcomp)  
>    -> to/TO (mark)  
>    -> syzygy/NN (dobj)  
>      -> a/DT (det)  
>  -> ?/. (punct)  

***Syntactic Parses:***  
>Parse tree = (ROOT (SBARQ (WHPP (IN In) (WHNP (WDT which) (NN college) (NN class))) (SQ (MD would) (NP (PRP you)) (VP (VB be) (ADJP (RBS most) (JJ likely) (S (VP (TO to) (VP (VB study) (NP (DT a) (NN syzygy)))))))) (. ?)))
