import random
from preprocess import preprocess_raw_sent
from preprocess import sim_with_title
from preprocess import sim_with_doc
from preprocess import sim_2_sent
from preprocess import count_noun
import numpy as np
import nltk
import os.path
import statistics as sta
import re
from preprocess import preprocess_for_article
from preprocess import preprocess_numberOfNNP
import time


def load_a_doc(filename):
    file = open(filename, encoding='utf-8')
    article_text = file.read()
    file.close()
    return article_text


def load_docs(directory):
    docs = list()
#    count = 0 #add from Dinh
    for name in os.listdir(directory):
        #        if count == 100: break   #add from DInh
        filename = directory + '/' + name
        doc = load_a_doc(filename)
        docs.append((doc, name))
#        count += 1 # add from Dinh
    return docs


def main():
    # foder lưu các file
    directory = 'input'

    # list of documents
    stories = load_docs(directory)
    start_time = time.time()
    for example in stories:
        try:
            #            raw_sentences = example[0].split("\n")
            raw_sentences = re.split("\.\s+", example[0])
            #raw_sentences = list(filter(lambda x: len(x) > 10, raw_sentences))
            if len(raw_sentences) == 0:
                continue
            print('raw', len(raw_sentences), stories.index(example))
            title_raw = raw_sentences[0]
            # Preprocessing
            print("Preprocessing...")
            sentences = []
            sentences_for_NNP = []
            for raw_sent in raw_sentences:
                sent = preprocess_raw_sent(raw_sent)
                sent_tmp = preprocess_numberOfNNP(raw_sent)
                if len(sent.split(' ')) < 2:
                    raw_sentences.remove(raw_sent)
                else:
                    sentences.append(sent)
                    sentences_for_NNP.append(sent_tmp)
            title = preprocess_raw_sent(title_raw)
            number_of_nouns = count_noun(sentences_for_NNP)

            simWithTitle = sim_with_title(sentences, title)
            sim2sents = sim_2_sent(sentences)
            simWithDoc = []
            for sent in sentences:
                simWithDoc.append(sim_with_doc(sent, sentences))

    #        x = int(len(sentences)*0.2)
            if len(sentences) < 3:
                NUM_PICKED_SENTS = len(sentences)
            else:
                #            NUM_PICKED_SENTS = x
             #       NUM_PICKED_SENTS = int(len(sentences)*0.2)
                NUM_PICKED_SENTS = 3

            print("Done preprocessing!")
            # DONE!

            print("--- %s mins ---" %
                  ((time.time() - start_time)/(60.0*len(stories))))


if __name__ == '__main__':
    main()
