import requests
import sys
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt

# Here's a Category page for Simple English Wikipedia
#URL = "https://en.wikipedia.org/wiki/Category:Endangered_animals"
HorrorURL = "https://imsdb.com/genre/Horror"

# Get that page.
page = requests.get(URL)

# Now parse the html.
soup = BeautifulSoup(page.content, "html.parser")

# List for storing the links to pages we want to get.
HorrorMovies = []

# Find the heading associated with "Pages in category"
# Depending on the Category page you are looking at.
# you might need to change the text you want to match.
for h2 in soup.find_all("h2"):
    if "Horror Movie Scripts" in h2.text:

        # Find all subsequent a href tags. 
        for a in h2.find_all_next("a", href=True, limit=int(10)):
            if "Movie%20Scripts" in a["href"]:
                for j in h2.find_all_next("j", href=True, limit=1):
                    if "scripts" in j["href"]:
                        HorrorMovies.append(j["href"])


pagestrings = []

for h in HorrorMovies:

    # You need to add the rest of the URL to the beginning.
    URL = "https://imsdb.com/scripts/" + h

    # Go get it and parse the html.
    page = requests.get(URL)
    newsoup = BeautifulSoup(page.content, "html.parser")

    # Print out all the text.
    mystring = ""
    for info in newsoup.find_all("p"):
        mystring = mystring + " " + info.get_text()


    mystring = re.sub("\n", " ", mystring)
    mystring = re.sub("\s+", " ", mystring)
    mystring = re.sub("\[.*?\]", " ", mystring)

    pagestrings.append(mystring)



## TOKENIZE                                                                                         
tokenlists = []
for s in pagestrings:
    alltokens = nltk.word_tokenize(s)
    tokenlists.append(alltokens)

## REMOVE STOP WORDS                                                                                

stoplist = stopwords.words('english')
stoplist.extend([".", ",", "?", "could", "would", "“", "”", "’", ";", "!","much", "like", "one", "many", "though", "withzout", "upon"])
nostops = []
for tl in tokenlists:
    nostopwords = [w for w in tl if w.lower() not in stoplist]
    nostops.append(nostopwords)


## LEMMATIZE                                                                                                    
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

# create a new list of tokens, alllemmas by lemmatizing allcontenttokens                                        
lemmatized = []
for tl in nostops:
    all_lemmas = [lemmatizer.lemmatize(w) for w in tl]
    lemmatized.append(all_lemmas)


## WORD CLOUDS FOR INDIVIDUAL PAGES                                                                                 
# The wordcloud library expects a string not a list,                                                            
# so join the list back together with spaces   
counter = 1
for all_lemmas in lemmatized:
    figurename = "wordcloud" + str(counter) + ".png"
    counter += 1
    text = " ".join(all_lemmas)

    # Generate a word cloud image                                                                               
    wordcloud = WordCloud().generate(text)

    # Display the generated image:                                                                              
    # the matplotlib way:                                                                                       

    # lower max_font_size                                                                                       
    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(figurename)


## WORD CLOUD FOR ALL PAGES  
text = [" ".join(t) for t in lemmatized]
alltext = " ".join(text)

wordcloud = WordCloud(max_font_size=40).generate(alltext)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("allwordcloud.png")
