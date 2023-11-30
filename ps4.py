import requests
import sys
import re
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from bs4 import BeautifulSoup
import matplotlib.pyplot as plt


HorrorURL = "https://imsdb.com/genre/Horror"

# Get the page
page = requests.get(HorrorURL)

# Parse the HTML
soup = BeautifulSoup(page.content, "html.parser")

# List for storing movie names
HorrorMovies = []
movie_count = 0
# Find all 'a' tags with href attributes on the page
for a in soup.find_all("a", href=True):
    if movie_count >= 20:  # Stop after 20 movies have been added
        break
    # Check if the text of the link contains '(' since all the movies have ( after them
    if "(" in a.text:
        # Extract the movie name by taking the substring before the first '('
        movie_name = a.text.split(" (")[0].strip()
        HorrorMovies.append(movie_name)
        movie_count += 1
    else:
        # If there is no '(', assume the entire text is the movie name
        HorrorMovies.append(a.text.strip())
        movie_count += 1

#this works and prints the names of the horror mpvies, 
HorrorMovies = HorrorMovies[[62:62+20]  # this is just to get rid of the first 62 eleemtns because they are other things from the page 
for movie in HorrorMovies:
    print(movie)
pagestrings = []
for movie in HorrorMovies:
    # Replace spaces with hyphens
    movie_with_hyphens = movie.replace(" ", "-")
    #this is working and getting the correct links
    URL = "https://imsdb.com/scripts/" + movie_with_hyphens +".html"
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
##WE STILL NEED TO ADD ANY ALL CAPS WORD SO IT REMOVES THE NAMES
stoplist = stopwords.words('english')
stoplist.extend([".", ",", "?", "could", "would", "“", "”", "’", ";", "!","much", "like", "one", "many", "though", "without", "upon"])
nostops = []
for tl in tokenlists:
    nostopwords = [w for w in tl if w.lower() not in stoplist and not w.isupper()]
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
