# python -m flask run
# source activate summarizer
# netstat -an | grep 5000
# kill -9 $(lsof -t -i:5000)

import flask
from flask_cors import CORS, cross_origin
import io
import string
import time
import os

import numpy as np
import tensorflow as tf
from flask import Flask, request

from googlesearch import search
from bs4 import BeautifulSoup
import urllib.request

from transformers import BartTokenizer, BartForConditionalGeneration, BartConfig


app = Flask(__name__)


cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


import nltk
nltk.download('punkt')


from transformers import pipeline
#from summarizer import Summarizer
from nltk import sent_tokenize
import re

def find_doctors_list(disease_name):
  query = disease_name + " doctors in Indore"
  doctor_result=[]
  for j in search(query):
    if j.find("practo.com")!=-1 and j.find("/doctor/")==-1:
      websitepage = urllib.request.urlopen(j)
      soup = BeautifulSoup(websitepage)
      
      doctor_list = soup.find_all('div', class_ = 'info-section')

      for doctor in doctor_list:
        if(doctor):
          doctor_name = ''
          doctor_address = ''
          doctor_clinic = ''
          if(doctor.find(attrs={"data-qa-id": "doctor_name"})):
            doctor_name = doctor.find(attrs={"data-qa-id": "doctor_name"}).string
          if(doctor.find(attrs={"data-qa-id": "practice_locality"})):
            doctor_address = str(doctor.find(attrs={"data-qa-id": "practice_locality"}).parent)
          if(doctor.find(attrs={"data-qa-id": "doctor_clinic_name"})):
            doctor_clinic = doctor.find(attrs={"data-qa-id": "doctor_clinic_name"}).string
          
          if(len(doctor_name)>0):
            doctor_object = {"name": doctor_name, "address": doctor_address, "clinic": doctor_clinic}
            doctor_result.append(doctor_object)
  
  return doctor_result

def read_text(path_to_file):
  f = open(path_to_file, 'r', encoding='utf8')
  text = f.read()
  f.close()
  return text

def preprocess_text(text):
    text = text.strip()
    text = text.replace('\n', ' ').replace('\r', '')
    text = re.sub('\.+', '.', text)
    text = text.replace('«', '"').replace('»', '"')
    text = re.sub('[\.\?\!\;]"', '"', text)
    text = re.sub('[\.\?\!]\;"', ';', text)
    text = re.sub(' +', ' ', text)
    text = re.sub('\t+', ' ', text)
    return text


def smart_tokenization(text):
    sentences = sent_tokenize(text)
    res = []
    cur_text = ''
    for sent in sentences:
        #2000 - max count of symbols for abstractive model
        if len(cur_text + sent) > 2000: 
            res.append(cur_text)
            cur_text = sent
        else:
            cur_text += sent
    if cur_text != '':
      res.append(cur_text)
    return res


class AbstractiveSummarizer():
    def __init__(self):
        self.model = pipeline('summarization')

    def generate_summary(self, text):
        text = preprocess_text(text)
        parts = smart_tokenization(text)
        res = []
        for part in parts:
            res.append(self.model(part)[0]['summary_text'])
        return ' '.join(res)



def do_summarization(text):
    # summarizer = AbstractiveSummarizer()    
    # print("do_summarization called")
    # y = summarizer.generate_summary(text)
    # print(type(y))
    # return y
    model = BartForConditionalGeneration.from_pretrained('facebook/bart-large-cnn')
    tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
    inputs = tokenizer([text], return_tensors='pt')
    summary_ids = model.generate(inputs['input_ids'], max_length=500, early_stopping=False)
    y = [tokenizer.decode(g, skip_special_tokens=True) for g in summary_ids]
    # print(y)
    return y
    

 
TEXT_TO_SUMMARIZE = """
Introduction
The etiology of alopecia areata (AA), a chronic inflammatory
disease that affects the hair follicle and sometimes the nails, has not
yet been fully understood. Besides the genetic background, nonspecific immune response, organ-specific autoimmune reactions,
and environmental factors are among the most frequently discussed
issues in the pathogenesis of this disease [1].
It has long been claimed that AA is a psychosomatic disease
triggered by stressful life events [2]. In a study investigating
comorbid diseases in patients with AA, prevalence of depression
and anxiety was found to be high (25.5%) in an 11-year period [3].
On the other hand, depression may be present before AA [4].
Family problems, work-related problems, and mourning have
also been reported by AA patients [4]. It has been suggested that
neuroendocrine immunology as well as psychosocial factors may
be responsible for the association between AA and depression [5].
It is well known that sleep has important effects on immunity.
There is evidence of a relationship between sleep disorders and
autoimmune diseases including rheumatoid arthritis, ankylosing
spondylitis, Sjögren’s syndrome and systemic lupus erythematosus
[6]. It has been reported that patients with sleep disorders, especially
young people, had an increased risk of AA [7]. In the same study,
sleep disorders were also associated with other autoimmunity
related diseases such as Graves’ disease, Hashimoto’s thyroiditis,
vitiligo and rheumatoid arthritis.
"""

do_summarization(TEXT_TO_SUMMARIZE)

   
@app.route('/summarizer', methods=['POST'])
@cross_origin()
def home():
    request_data = request.get_json()
    text = request_data['text']

    # just for quick debugging adding below lines
    # TODO: should be removed afterwords
    text = """FINAL REPORT ic
              PORTABLE AP CHEST FILM __ AT ___
              CLINICAL INDICATION: __ -year-old with nasogastric tube placement.
              Comparison to prior study dated ___ at ___.
              A series of three portable AP sequential images of the chest, the first at
              ___, the second at __ and the third at ___, are submitted.
              IMPRESSION:
              There has been interval attempted placement of a nasogastric tube which
              courses into the stomach but the tip ends up in the mid esophagus on all three
              images. Overall, cardiac and mediastinal contours are stable. Lungs are
              relatively well inflated. The subtle opacity in the right mid lung on the
              previous study does not persist and therefore is felt to correspond to an area
              of patchy atelectasis. No focal airspace consolidation is seen to suggest
              pneumonia. No pleural effusions or pneumothorax.
              """
    output = do_summarization(text)
    # print(output)
    return {"output": output}


@app.route('/doctors', methods=['POST'])
@cross_origin()
def find_doctors():
    request_data = request.get_json()
    text = request_data['disease']
    output = find_doctors_list(text)
    print(output)
    return {"output": output}


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')