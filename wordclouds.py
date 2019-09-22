import json
import os
import matplotlib.pyplot as plt
import numpy as np
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from nltk.stem import PorterStemmer
from PIL import Image
from nltk.tokenize import sent_tokenize, word_tokenize
from langdetect import detect
import langdetect as ld

nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

PS = PorterStemmer()
MASK_LOC = "images/wordclouds/mymask.png"
LD_EXC = ld.lang_detect_exception.LangDetectException

def wordcloud():
    """
    Analysing users' posts,comments and friends data.
    
    Generate wordclouds of commonly used words from users' posts and comments
    Find out the most used language in posts and comments
    Generate wordcloud of friends' names, most tagged in your posts
    """
    
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
    
    final_text = None
    final_comments = None
    languages = []
    ctr=0
    
    if "comments" in base_data:
        data = base_data["comments"]
        
        for ele in data:
            if 'data' in ele:
                ctext = ele["data"][0]["comment"]["comment"]
                try:
                    b = detect(ctext)
                    if b not in languages:
                        languages.append(b)
                except LD_EXC:
                    ctr+=1
                if final_comments is None:
                    final_comments ="" + ctext
                else:
                    final_comments = final_comments + " " + ctext
                words = word_tokenize(ctext)
                for w in words:
                    if final_text is None:
                        final_text ="" + PS.stem(w)
                    else:
                        final_text = final_text + " " + PS.stem(w)
    else:
        print("No Comments found in data")
    
    fname = loc+'/posts/your_posts_1.json'
    if not os.path.isfile(fname):
        print("The file your_posts.json is not present at the entered location.")
        exit(1)
        
    with open(fname) as f:
        base_data = json.load(f)

    if "status_updates" in base_data:
        data = base_data["status_updates"]
        
        for ele in data:
            if "data" in ele:
                if "post" in ele["data"][0]:
                    try:
                        b = detect(ele["data"][0]["post"])
                        #if b not in languages:
                        languages.append(b)
                    except LD_EXC:
                        ctr+=1
                    words = word_tokenize(ele["data"][0]["post"])
                    for w in words:
                        if final_text is None:
                            final_text ="" + PS.stem(w)
                        else:
                            final_text = final_text + " " + PS.stem(w)
    
    print("Your Most Common Language: ")
    print(max(languages,key=languages.count))
        
    if final_text != "":
        mask = np.array(Image.open(MASK_LOC))
        wordcloud = WordCloud(background_color = "white", collocations=False, mask = mask, max_font_size=300, relative_scaling = 1.0,
                          stopwords = set(STOPWORDS)
                          ).generate(final_text)
        image_colors = ImageColorGenerator(mask)
        
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation="bilinear")
        plt.axis("off")
        print("WordCloud of Your Comments & Posts text generated.")
        plt.show()
    else:
        print("No Comments and Posts Text Found")

        
    #Friends Tagged
    
    flist = []
    fname = loc+'/friends/friends.json'
    if not os.path.isfile(fname):
        print("The file friends.json is not present at the entered location.")
        exit(1)
    with open(fname) as f:
        base_data = json.load(f)
    base_data = base_data["friends"]
    for ele in base_data:
        fwords = word_tokenize(ele["name"])
        if fwords[0]!="Md" and fwords[0]!="Kumar":
            flist.append(fwords[0])
        else:
            flist.append(fwords[1])
            
    if final_comments!="":
        friend_names = ""
        for sent in nltk.sent_tokenize(final_comments):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label'):
                    if(chunk.label()[0]=='P'):
                        if ''.join(c[0] for c in chunk.leaves()) in flist:
                            friend_names = friend_names + " " + ' '.join(c[0] for c in chunk.leaves())

        wordcloud = WordCloud(background_color = "white", mask = mask,relative_scaling = 1.0,
                          stopwords = set(STOPWORDS)
                          ).generate(friend_names)

        plt.imshow(wordcloud)
        plt.axis("off")
        print("WordCloud of Your friends mostly tagged by you")
        plt.show()
    else:
        print("No Comments and Posts Text Found")
    
if __name__ == '__main__':
    wordcloud()
