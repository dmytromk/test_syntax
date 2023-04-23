# App to generate combinations (paraphrases) of the same syntax tree without changing its meaning
Get started: 

1. Clone the repository `git clone https://github.com/dmytromk/test_syntax`
2. Move to the newly created folder `cd test_syntax`
3. Set up a virtual environment `python -m venv env`
4. Start the virtual environment `.env/Scripts/activate`
5. Update pip `python -m pip install --upgrade pip`
6. Install all dependencies `python -m pip install --no-cache-dir -r requirements.txt`
7. Set up a local server `uvicorn app:app --reload`
8. At `http://localhost:8000/paraphrases?tree=TEST&limit=INT` you can get INT (deafult INT = 20, replace INT with any number OR delete `&limit=INT` tp leave default) paraphrases of the TEST tree (replace TEST with your tree). 
Example: `http://localhost:8000/paraphrases?tree=(S (NP (NP (DT The) (JJ charming) (NNP Gothic) (NNP Quarter) ) (, ,) (CC or) (NP (NNP Barri) (NNP Gòtic) ) ) (, ,) (VP (VBZ has) (NP (NP (JJ narrow) (JJ medieval) (NNS streets) ) (VP (VBN filled) (PP (IN with) (NP (NP (JJ trendy) (NNS bars) ) (, ,) (NP (NNS clubs) ) (CC and) (NP (JJ Catalan) (NNS restaurants) ) ) ) ) ) ) )`
9. ALTERNATIVELY, if you want to see the result in cosole, then change 'test_str' (tree) and 'test_limit' in the 'console_test' function call and run the file
