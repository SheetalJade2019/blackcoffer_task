import pandas as pd
import nltk
from nltk.tokenize import word_tokenize
# from .data_extraction import extract_data
# from .text_mining.text_mining import *
import spacy
from extract_data import extract_data
from text_mining import *


mastordictionary_path = "D:/SHEETAL/LEARN/INTERVIEWS/blackcoffer/MasterDictionary"
stopwords_dir = "D:/SHEETAL/LEARN/INTERVIEWS/blackcoffer/StopWords"
output_files_path = "D:/SHEETAL/LEARN/INTERVIEWS/blackcoffer/Task_submission/txt_output/"
input_file = "D:/SHEETAL/LEARN/INTERVIEWS/blackcoffer/Task_submission/Input.xlsx"
result_file = "D:/SHEETAL/LEARN/INTERVIEWS/blackcoffer/Task_submission/result/result.csv"

def start_data_extraction(input_file):
    try:
        data = []
        df = pd.read_excel(input_file)
        output_file_list  = []
        for index, row in df.iterrows():
            r = [row["URL_ID"],row["URL"]]
            print(r)
            # if index <=5:
            output_file_list.append(extract_data(row["URL"],row["URL_ID"],output_files_path)) 
            data.append(r)
        return {"status":True, "output_file_list":output_file_list,"data":data}
    except Exception as e:
        print("Exception in data extraction : ",str(e))
        return {"status":False,"reason":str(e)}

def start_text_mining(output_file_list,stopwords_list, word_dict,data):
    try:
        for file,row in zip(output_file_list, data):
            original_text = read_from_file(file)
            cleaned_txt = remove_stopwords(original_text.split(),stopwords_list)
            tokens = word_tokenize(cleaned_txt.lower())
            scores = get_scores(word_dict,len(tokens))
            words = get_words("".join(tokens))
            list_of_sentences = break_sentences(original_text)
            avg_sent_len = avg_sentence_length(list_of_sentences,words)
            complex_word_cnt = get_complex_word_cnt(words)
            complex_word_percent=0
            if len(words):
                complex_word_percent = complex_word_cnt/len(words) #get_percent_of_complex(words)
            fog_index = get_fog_index(avg_sent_len, complex_word_percent)
            avg_words_per_sentence = get_avg_words_per_sent(words,list_of_sentences)
            avg_word_len = get_avg_word_len(words)
            personal_pronoun = get_personal_pronouns(original_text)
            row.extend([scores['pos_score'],scores['neg_score'],scores['polarity_score'],scores['subjectivity_score'],avg_sent_len,complex_word_percent,fog_index,avg_words_per_sentence,complex_word_cnt,len(words),0,len(personal_pronoun),avg_word_len])
            print(row)
        return data
    except Exception as e:
        print("Exception at text mining : ",str(e))
        return []


if __name__=="__main__":
    pass
    # start data extraction
    print("* * * DATA EXTRACTION START * * * ")
    task1 = start_data_extraction(input_file)
    print("* * * DATA EXTRACTION END * * * ")
    stopwords_list = get_stopwords(stopwords_dir)
    word_dict = create_word_dict(mastordictionary_path, stopwords_list)
    if task1["status"]:
        # start text mining
        print("* * * TEXT MINING START * * *")
        data = start_text_mining(task1["output_file_list"],stopwords_list, word_dict, task1["data"])
        print("* * * TEXT MINING END * * *")
        # write result to csv
        columns = ['URL_ID','URL','POSITIVE SCORE',	'NEGATIVE SCORE','POLARITY SCORE','SUBJECTIVITY SCORE',	'AVG SENTENCE LENGTH',	'PERCENTAGE OF COMPLEX WORDS',	'FOG INDEX', 'AVG NUMBER OF WORDS PER SENTENCE', 'COMPLEX WORD COUNT',	'WORD COUNT',	'SYLLABLE PER WORD','PERSONAL PRONOUNS','AVG WORD LENGTH']
        create_results_csv(data, columns, result_file)

        
        


