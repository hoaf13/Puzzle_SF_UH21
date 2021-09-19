# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 20:27:14 2021

@author: PC
"""
from tensorflow.keras.models import load_model
import tensorflow as tf
import re
from vncorenlp import VnCoreNLP
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle
import numpy as np
import os


num2label = ['affirm_confirm', 'ask_gender_wrong', 'no_date', 'provide_gender', 
             'ask_age_wrong', 'ask_date_wrong','provide_age', 'ask_name_wrong',
             'pick_date', 'provide_name', 'cant_hear', 'choose_department', 'deny_confirm']
            

print("----------LOADING ANOTATOR----------")
ANOTATOR = VnCoreNLP("intent_classification/VnCoreNLP/VnCoreNLP-1.1.1.jar", annotators="wseg", max_heap_size='-Xmx2g') 
print("Successfully loading word segment anotator !")


def normalize_sentence(s):
    s = s.lower()
    s = re.sub('-', '', s)
    s = re.sub(',', '', s)
    s = re.sub("\.", '', s)
    s = re.sub('\?','', s)
    s = re.sub('\!','', s)
    s = re.sub('_','', s)
    s = s.strip()
    annotator = ANOTATOR
    annotated_text = annotator.annotate(s)
    words = annotator.tokenize(s)[0]
    s = ' '.join(words)  
    return s
          

def padding_sentence(s):
    with open('intent_classification/tokenizer.pickle', 'rb') as handle:
         tokenizer = pickle.load(handle)
    test_sequence = tokenizer.texts_to_sequences([s])
    padded_test_sequences = pad_sequences(test_sequence, maxlen=20, truncating="post", padding="post")
    return padded_test_sequences


class NLPModel:
    def __init__(self, dir2model):
        self.model = load_model(dir2model)
    
    def predict(self, sentence):
        normal_sentence = normalize_sentence(sentence)
        padded_sentence = padding_sentence(normal_sentence)
        prediction = self.model.predict(padded_sentence)
        p = round(np.max(prediction, axis=1)[0],2)
        if p > 0.5:
            label = num2label[np.argmax(prediction, axis = 1)[0]]
        else:
            label = 'intent_fallback'
        return label, p

