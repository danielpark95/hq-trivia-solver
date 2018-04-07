# HQ-Trivia-Solver

Program for answering trivia questions from the popular mobile game HQ with Bing Web Search API, MediaWiki API, and NLTK in Python 3.

## Usage
### pip3
If you don't already have pip3 installed, you'll need to run the following command in your terminal before proceeding:
```
$ sudo apt-get install python3-pip
```
### Python dependencies
You'll need to install the following python modules:
```
$ pip3 install nltk
$ pip3 install beautifulsoup4
$ pip3 install requests
$ pip3 install markdown
$ pip3 install html5lib
$ pip3 install urllib3
```

### Testing
The following command runs the Bing Search Model and Wiki Search Model on sample questions located in /src/input_files and outputs the results:
```
$ python3 test.py
```
## Models
***Bing Search Model***   
The Bing Search Model uses Microsoft Azure's Bing Web Search API to retrieve a search term's top 5 results, and then counts how many times each of the answer choices appear across the 5 pages. 

***Wikipedia Answer Model***   
The Wikipedia Answer Model uses MediaWiki's Web API to retrieve JSON pages of Wikipedia articles for each of the answer choices, and then counts the number of times the key words co-occur within a 10-15 word window.  

## Sample Results 
***Example 1***  
>Q: Which of these is a standard cheerleading jump?  
>A: ['Herkie', 'Flap', 'Striker']  
>  
>BING SEARCH MODEL  
>Bing Guess: Herkie  
>Guess is correct!  
>Bing Search Model took 2.7611379623413086 seconds  
>  
>WIKI SEARCH MODEL  
>Wiki Guess: Herkie  
>Guess is correct!  
>Wiki Search Model took 0.8776249885559082 seconds  

***Example 2***  
>Q: Which of these companies is NOT owned by Williams-Sonoma, Inc.?  
>A: ['Pottery Barn', 'West Elm', 'Crate & Barrel']  
>  
>BING SEARCH MODEL  
>Bing Guess: Crate & Barrel  
>Guess is correct!  
>Bing Search Model took 4.79827880859375 seconds  
>  
>WIKI SEARCH MODEL  
>Wiki Guess: Crate & Barrel  
>Guess is correct!  
>Wiki Search Model took 1.7192120552062988 seconds  

***Example 3***  
>Q: In a standard deck of playing cards, which king is holding an axe and facing sideways?  
>A: ['King of Diamonds', 'King of Hearts', 'King of Clubs']  
>  
>BING SEARCH MODEL  
>Bing Guess: King of Hearts  
>Wrong!  
>Bing Search Model took 2.2626800537109375 seconds  
>  
>WIKI SEARCH MODEL  
>Wiki Guess: King of Diamonds  
>Guess is correct!  
>Wiki Search Model took 1.7012982368469238 seconds  

***Example 4***  
>Q: Which is the only actor to appear as both a student and a guest on "Inside the Actors Studio"?  
>A: ['Ryan Gosling', 'Tobey Maguire', 'Bradley Cooper']  
>  
>BING SEARCH MODEL  
>Bing Guess: Bradley Cooper  
>Guess is correct!  
>Bing Search Model took 5.403349876403809 seconds 
>  
>WIKI SEARCH MODEL  
>Wiki Guess: Ryan Gosling  
>Wrong!  
>Wiki Search Model took 1.438279151916504 seconds  


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

## Acknowledgments
I'd like to thank Professor Tim Hunter for guiding me with the project and providing key insights necessary to complete the project as part of UCLA's Student Research Program 199.
