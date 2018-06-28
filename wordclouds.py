import json
import os
import matplotlib.pyplot as plt
import numpy as np
import re
import random
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import nltk
from PIL import Image
nltk.download('maxent_ne_chunker')
nltk.download('words')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')

def grey_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    return "hsl(0, 0%%, %d%%)" % random.randint(1, 50)

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
    
    final_text = ""
    if "comments" in base_data:
        data = base_data["comments"]
        
        for ele in data:
            if 'data' in ele:
                ctext = ele["data"][0]["comment"]["comment"]
                final_text = final_text + " " + ctext
        final_comments = final_text
    else:
        print("No Comments found in data")
        
    fname = loc+'/posts/your_posts.json'
    with open(fname) as f:
        base_data = json.load(f)

    if "status_updates" in base_data:
        data = base_data["status_updates"]
        
        for ele in data:
            if "data" in ele:
                if "post" in ele["data"][0]:
                    #print(ele["data"][0]["post"])
                    final_text = final_text + ' ' + ele["data"][0]["post"]

    if final_text != "":
        mask = np.array(Image.open("images/mymask.png"))
        wordcloud = WordCloud(background_color = "white", mask = mask, max_font_size=300, relative_scaling = 1.0,
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
    if final_comments!="":
        friend_names = ""
        for sent in nltk.sent_tokenize(final_comments):
            for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sent))):
                if hasattr(chunk, 'label'):
                    if(chunk.label()[0]=='P'):
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