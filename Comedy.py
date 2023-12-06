import requests
from bs4 import BeautifulSoup, NavigableString
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import nltk
from nltk import bigrams, FreqDist
from nltk.collocations import BigramCollocationFinder, BigramAssocMeasures
from nltk.tokenize import word_tokenize

custom_stop_words = [".", ",", "Mike", "Adam", "?", "could", "would", "“", "”", "’", ";", "!", "much", "like", "one", "many", "though", "without", "upon", "back", "know", "knows", "see", "sees", "seen"]
stop_words = set(stopwords.words("english") + custom_stop_words)

all_text=""


# URL of the Comedy genre page
ComedyURL = "https://imsdb.com/genre/Comedy"

# Fetching the page
page = requests.get(ComedyURL)

# Parsing the HTML of the genre page
soup = BeautifulSoup(page.content, "html.parser")

# Extracting movie names
ComedyMovies = []
for a in soup.find_all("a", href=True):
    if "(" in a.text:
        movie_name = a.text.split(" (")[0].strip()
        ComedyMovies.append(movie_name)
    else:
        ComedyMovies.append(a.text.strip())



# Remove the first 62 elements (non-movie items)
ComedyMovies = ComedyMovies[62:82]


# List for storing urls
url_list = []
for movie in ComedyMovies:
    movie_with_hyphens = movie.replace(" ", "-")
    movie_url = "https://imsdb.com/scripts/" + movie_with_hyphens + ".html"
    movie_page = requests.get(movie_url)
    movie_soup = BeautifulSoup(movie_page.content, "html.parser")
    #print(movie_url)
    url_list.append(movie_url)


# Traverse url_list
for links in url_list:
    script=requests.get(links)
    if script.status_code==200:
        # Parse the html content of the page
        soup=BeautifulSoup(script.text,'html.parser')

        # Find all text lines within the body
        lines=soup.body.stripped_strings
        # Filter lines that are not in all capital letters and remove stop words
        filtered_lines = [' '.join(word for word in line.split() if word.lower() not in stop_words) for line in lines if not line.isupper()]
        # Combine the filtered lines into a single text
        text = ' '.join(filtered_lines)

        # Append the text to the overall text
        all_text += text
    else:
        print(f"Failed to retrieve content from {links}. Status code: {script.status_code}\n")

# NLTK's required resources
nltk.download('punkt')
nltk.download('stopwords')

# Tokenize the text
tokens = word_tokenize(all_text)

# Generate bigrams
bigram_list = list(bigrams(tokens))

# Filter out bigrams with stop words
filtered_bigrams = [bigram for bigram in bigram_list if bigram[0].lower() not in stop_words and bigram[1].lower() not in stop_words]

# Calculate frequencies of bigrams
freq_dist = FreqDist(filtered_bigrams)

# Top 10 bigrams
top_10_bigrams = freq_dist.most_common(30)

# Finding collocations
bigram_measures = BigramAssocMeasures()
finder = BigramCollocationFinder.from_words(tokens)
finder.apply_freq_filter(3)
finder.apply_word_filter(lambda w: len(w) < 3 or w.lower() in stop_words)

# Top 10 collocations
top_10_collocations = finder.nbest(bigram_measures.pmi, 30)

# Prints bigrams and collocations
print("Top 10 Bigrams:", top_10_bigrams)
print("\nTop 10 Collocations:", top_10_collocations)


# Generate a WordCloud
wordcloud = WordCloud(width=800, height=400, background_color='white').generate(all_text)

# Display the WordCloud
plt.figure(figsize=(10, 5))
plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title("Comedy Wordcloud")
plt.show()
