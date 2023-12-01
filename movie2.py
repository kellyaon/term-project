import requests
from bs4 import BeautifulSoup, NavigableString
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# URL of the Horror genre page
HorrorURL = "https://imsdb.com/genre/Horror"

# Fetching the page
page = requests.get(HorrorURL)

# Parsing the HTML of the genre page
soup = BeautifulSoup(page.content, "html.parser")

# Extracting movie names
HorrorMovies = []
for a in soup.find_all("a", href=True):
    if "(" in a.text:
        movie_name = a.text.split(" (")[0].strip()
        HorrorMovies.append(movie_name)
    else:
        HorrorMovies.append(a.text.strip())

# Remove the first 62 elements (non-movie items)
HorrorMovies = HorrorMovies[62:]

# List for storing script texts
pagestrings = []
for movie in HorrorMovies:
    movie_with_hyphens = movie.replace(" ", "-")
    movie_url = "https://imsdb.com/scripts/" + movie_with_hyphens + ".html"
    movie_page = requests.get(movie_url)
    movie_soup = BeautifulSoup(movie_page.content, "html.parser")

    script_text = ''
    bold_tags = movie_soup.find_all('b')

    for b_tag in bold_tags:
        sibling = b_tag.next_sibling
        while sibling and sibling.name != 'b':
            if sibling.string:
                script_text += sibling.string.strip() + ' '
                sibling = sibling.next_sibling
            print(script_text)
    script_text = re.sub("\n", " ", script_text)
    script_text = re.sub("\s+", " ", script_text)
    script_text = re.sub("\[.*?\]", " ", script_text)
    pagestrings.append(script_text)
    print(pagestrings)
# Tokenizing
tokenlists = []
for s in pagestrings:
    alltokens = nltk.word_tokenize(s)
    tokenlists.append(alltokens)

# Removing stop words
stoplist = stopwords.words('english')
stoplist.extend([".", ",", "?", "could", "would", "“", "”", "’", ";", "!", "much", "like", "one", "many", "though", "without", "upon"])
nostops = []
for tl in tokenlists:
    nostopwords = [w for w in tl if w.lower() not in stoplist]
    nostops.append(nostopwords)

# Lemmatizing
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()
lemmatized = []
for tl in nostops:
    all_lemmas = [lemmatizer.lemmatize(w) for w in tl]
    lemmatized.append(all_lemmas)

# Creating Word Clouds for Individual Pages
counter = 1
for all_lemmas in lemmatized:
    figurename = "wordcloud" + str(counter) + ".png"
    counter += 1
    text = " ".join(all_lemmas)

    wordcloud = WordCloud(max_font_size=40).generate(text)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.savefig(figurename)

# Word Cloud for All Pages
text = [" ".join(t) for t in lemmatized]
alltext = " ".join(text)

wordcloud = WordCloud(max_font_size=40).generate(alltext)
plt.figure()
plt.imshow(wordcloud, interpolation="bilinear")
plt.axis("off")
plt.savefig("allwordcloud.png")

