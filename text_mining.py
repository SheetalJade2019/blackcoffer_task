import pandas as pd
import nltk
# nltk.download('all')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
import os
import spacy
import re

def create_results_csv(data, columns, result_file):
    df = pd.DataFrame(data,columns=columns)
    df.to_csv(result_file)

def read_from_file(file):
  f = open(file, "r+", encoding='utf8',errors='ignore')
  original_text = f.read()
  f.close()
  return original_text

def get_stopwords(stopwords_dir):
  entries = os.listdir(stopwords_dir)
  stopwords = []
  for e in entries:
    f = open(f"{stopwords_dir}/{e}", "r+", encoding='utf8',errors='ignore')
    stopwords.extend(f.read().split("\n"))
  return stopwords

def remove_stopwords(original_text_ls,stopwords):
  text_words_without_sw = [ t for t in original_text_ls if not t in stopwords]
  return " ".join(text_words_without_sw)

def create_word_dict(mastordictionary_path, stopwords):
  word_dict = {}
  file = open(f'{mastordictionary_path}/negative-words.txt', 'r+', encoding='utf8',errors='ignore')
  neg_words = file.read().split()
  word_dict["neg_words"] = [ w for w in neg_words if w not in stopwords ]
  file = open(f'{mastordictionary_path}/positive-words.txt', 'r+', encoding='utf8',errors='ignore')
  pos_words = file.read().split()
  word_dict["pos_words"] = [ w for w in pos_words if w not in stopwords ]
  return word_dict

def get_scores(word_dict,tokens_without_sw):
  scores = {}
  scores["pos_score"] = len(word_dict["pos_words"])
  scores["neg_score"] = len( word_dict["neg_words"])*-1
  scores["polarity_score"] = (scores["pos_score"] - scores["neg_score"])/ ((scores["pos_score"] + scores["neg_score"]) + 0.000001)
  scores["subjectivity_score"] = (scores["pos_score"] + scores["neg_score"])/ ((tokens_without_sw) + 0.000001)
  return scores

# Returns Number of Words in the text
def get_words(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(text)
    words = [token for token in tokens if token not in stopwords.words('english')]
    return words

def get_syllable_cnt(word):
  word = word.split()
  cnt = 0
  for i in range(len(word)):
    if word[i] in ['a','e','i','o','u']:
      if i == len(word)-2 and word[i+1] in ['s','d']:
        pass
      else:
        cnt += 1
  return cnt

def get_complex_word_cnt(words):
  complex_cnt=0
  for w in words:
    if get_syllable_cnt(w) > 2:
      complex_cnt += 1
  return complex_cnt

def get_personal_pronouns(text):
   pronounRegex = re.compile(r'\bI\b|\bwe\b|\bWe\b|\bmy\b|\bMy\b|\bours\b|\bus\b')
   pronoun = pronounRegex.findall(text)
   return pronoun

def get_avg_word_len(words):
  if len(words)==0:
     return 0
  sum = 0
  for w in words:
    sum += len(w)
  return sum/len(words)


def break_sentences(text):
    nlp = spacy.load('en_core_web_sm')
    doc = nlp(text)
    return list(doc.sents)

# Returns the number of sentences in the text
def sentence_count(text):
    sentences = break_sentences(text)
    return len(sentences)

# Returns average sentence length
def avg_sentence_length( sentences,words):
    if len(sentences)==0:
      return 0
    average_sentence_length = float(len(words) / len(sentences))
    return average_sentence_length

def get_percent_of_complex(words,complex_word_cnt):
  if len(words)==0:
        return 0
  return complex_word_cnt/len(words)

def get_fog_index(avg_sent_len, percent_of_complex):
  return 0.4 * (avg_sent_len + percent_of_complex)

def get_avg_words_per_sent(words,sentence_list):
  if len(sentence_list)==0:
      return 0
  return len(words) / len(sentence_list)

