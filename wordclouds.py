import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re
from wordcloud import WordCloud, STOPWORDS
import nltk
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def wordcloud():
    loc = input('Enter facebook archive extracted location: ')
    if not os.path.isdir(loc):
        print("The provided location doesn't seem to be right")
        exit(1)
    
    fname = loc+'/comments/comments.json'
    if not os.path.isfile(fname):
        print("The file posts_and_commments.json is not present at the entered location.")
        exit(1)

    with open(fname) as f:
        base_data = json.load(f)
    
    data = base_data["comments"]
    final_text = ""
    for ele in data:
        if 'data' in ele:
            ctext = ele["data"][0]["comment"]["comment"]
            final_text = final_text + " " + ctext
    
    wordcloud = WordCloud(relative_scaling = 1.0,
                      stopwords = set(STOPWORDS)
                      ).generate(final_text)
    plt.imshow(wordcloud)
    plt.axis("off")
    print("WordCloud of Your Comments text generated.")
    plt.show()
    
    
    #Friends Tagged
    
    friend_names = ""
    for sent in nltk.sent_tokenize(final_text):
        for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
            if hasattr(chunk, 'label'):
                if(chunk.label()[0]=='P'):
                    friend_names = friend_names + " " + ' '.join(c[0] for c in chunk.leaves())
    
    wordcloud = WordCloud(relative_scaling = 1.0,
                      stopwords = set(STOPWORDS)
                      ).generate(friend_names)
    
    plt.imshow(wordcloud)
    plt.axis("off")
    print("WordCloud of Your friends mostly tagged by you")
    plt.show()
    
if __name__ == '__main__':
    wordcloud()