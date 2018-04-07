# HQ-Trivia-Solver

Program for answering trivia questions from the popular mobile game HQ with Bing Custom Search API, MediaWiki API, and NLTK in Python 3.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

What things you need to install the software and how to install them

```
pip3 install nltk
pip3 install beautifulsoup4
pip3 install requests
```

### Installing

A step by step series of examples that tell you have to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

```
python3 test.py
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* I'd like to thank Professor Tim Hunter for guiding me with the project and providing key insights necessary to complete the project as part of UCLA's Student Research Program 199.

## HQ Trivia Solver
Program for answering trivia questions from the popular mobile game HQ with Stanford CoreNLP API, MediaWiki API, and Google Custom Search API in Java.

## Program Demo
***Example 1***  
>Question: Which NBA franchise has NOT retired any jersey numbers?  
>Answer Choices: [Brooklyn Nets, Dallas Mavericks, Los Angeles Clippers]  
>  
>My guess is: Los Angeles Clippers  

***Example 2***  
>Question: Which of these is a standard cheerleading jump?  
>Answer Choices: [Herkie, Flap, Striker]  
>  
>My guess is: Herkie  

***Example 3***  
>Question: Which of these international foods is NOT a kind of dumpling?  
>Answer Choices: [Pelmeni, Pecel, Pierogi]  
>  
>My guess is: Pecel  
  
## NLP
***Named Entity Recognition:***  
>Question = "Which of these agencies began as the North West Police Agency?"  
>NER Output = {"North West Police Agency" - organization}.  

***Open Information Extraction:***   
>Question = "In which college class would you be most likely to study a syzygy?"  
>OpenIE Output = {"you" /subj, "study" /relation, "syzygy" /obj}  

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
