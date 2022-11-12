# python -m flask run

import flask
import io
import string
import time
import os
import numpy as np
import tensorflow as tf
from flask import Flask, jsonify, request

import nltk
nltk.download('punkt')

from transformers import pipeline
#from summarizer import Summarizer
from nltk import sent_tokenize
import re

app = Flask(__name__)

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


class ExtractiveSummarizer():
    def __init__(self):
        self.model = Summarizer()

    def generate_summary(self, text):
        text = preprocess_text(text)
        return self.model(text)


TEXT_TO_SUMMARIZE = """
# Introduction
# The etiology of alopecia areata (AA), a chronic inflammatory
# disease that affects the hair follicle and sometimes the nails, has not
# yet been fully understood. Besides the genetic background, nonspecific immune response, organ-specific autoimmune reactions,
# and environmental factors are among the most frequently discussed
# issues in the pathogenesis of this disease [1].
# It has long been claimed that AA is a psychosomatic disease
# triggered by stressful life events [2]. In a study investigating
# comorbid diseases in patients with AA, prevalence of depression
# and anxiety was found to be high (25.5%) in an 11-year period [3].
# On the other hand, depression may be present before AA [4].
# Family problems, work-related problems, and mourning have
# also been reported by AA patients [4]. It has been suggested that
# neuroendocrine immunology as well as psychosocial factors may
# be responsible for the association between AA and depression [5].
# It is well known that sleep has important effects on immunity.
# There is evidence of a relationship between sleep disorders and
# autoimmune diseases including rheumatoid arthritis, ankylosing
# spondylitis, Sjögren’s syndrome and systemic lupus erythematosus
# [6]. It has been reported that patients with sleep disorders, especially
# young people, had an increased risk of AA [7]. In the same study,
# sleep disorders were also associated with other autoimmunity
# related diseases such as Graves’ disease, Hashimoto’s thyroiditis,
# vitiligo and rheumatoid arthritis.
# Alopecia areata may occur in different clinical types. In the most
# common type, there is hair loss in the scalp[8]. If all of the scalp
# hair is involved, it is called alopecia totalis and, if all of the body
# hair is involved, it is called alopecia universalis. In the ophiasis
# type hair loss is seen at the junction of occipital hair line and dermis, and in the reticular type the hair loss is reticular [8].
# Nail changes are seen in 30% of patients with AA [9]. The most
# common nail finding is small pits, and the other findings are
# the Beau line, longitudinal line, koilonychia, onychorhexis,
# onychomadesis, leukonychia, red-staine lunula, and other nail
# defects can [9]. It has been suggested that nail change is related to
# the severity of the disease and indicates possible resistance [10].
# It is hard to predict natural course in alopecia areata. In some
# patients, hair completely reappears, in some others, some
# improvement in AA occurs, and, in still others, the hair loss further
# increases [11]. Poor prognostic criteria include presence of atopia,
# extensive involvement, family history, onychodystrophy, presence
# of disease for more than 5 years, autoimmune disease, ophiasis
# type, asthma, and the presence of nevus flammeus, allergic rhinitis,
# and atopic dermatitis [12].
# The aim of our study was to evaluate the frequency of depression
# and sleep quality in patients with AA, and to investigate the
# relationship between the clinical characteristics of the disease such
# as duration, severity, and type of illness and depression, and sleep
# quality.
# Material and Methods
# Sample
# This study was conducted in Skin and Venereal Diseases
# Department of the Medical School of Hitit University. This study
# included 52 patients above 18 years of age who admitted to the
# dermatology clinic and were diagnosed as alopecia areata and 51
# healthy volunteers. Healthy volunteers were selected from hospital
# staff and the relatives of hospital staff who didn’t have any history
# of psychiatric, systemic or dermatological disease and agreed to
# participate in the study. The patients and control group included
# in the study were informed about the study, and the questionnaires
# were completed after obtaining their written informed consents.
# Illiterate patients and those couldn’t fill the scales due to cognitive
# dysfunction were not included in the study. Patients who were
# being treated for a systemic disease or who had treatment for a
# psychiatric disease during the last year were excluded. This study
# was approved by the local ethics committee and performed in
# accordance with the ethical standards of the Helsinki Declaration.
# Instruments
# Beck Depression Inventory (BDI): This scale has been developed
# by Beck et al and aims to measure the severity of depression[13].
# The scale consists of 21 items and is scored between 0 to 3.
# Pittsburgh Sleep Quality Index (PSQI): It was developed by Buysse
# et al.[14] and consists of 24 questions, 19 questions are filled by
# the subject himself and 5 questions are filled by the spouse or a
# room partner. From the scored questions of the scale 7 subscale
# scores are obtained: subjective sleep quality, sleep latency, sleep
# duration, habitual sleep efficiency, sleep disturbance, use of sleep
# medications, and daytime dysfunction. The total score of seven
# subscales gives total scale score which varies between 0 and 21.
# Severity of Alopecia Areata Tool; SALT: This scale was developed
# by Olsen et al. [15] and calculated by measuring how much of the
# total body surface is affected considering involved body parts. In
# this study, patients with hair loss below 25% were classified as
# mild, 25-50% moderate and above 50% as severe loss.
# Procedures
# All of the included cases were informed about the study, informed
# consent forms were obtained, and then sociodemographic data
# form, BDI, and PSQI were filled by the patients. In addition to
# these, information about the severity of alopecia areata, duration
# of the disease, treatments they received, and information about
# their illnesses were also recorded.
# Statistical Analysis
# To summarize data obtained from the study, descriptive statistics
# were given as mean ± standard deviation or median and
# interquartile ranges depending on the distribution for continuous
# variables. The normality of the numerical variables was checked
# by the Kolmogorov-Smirnov test. Independent Samples t test
# was used in the comparison of two independent groups when
# the numerical variables showed normal distribution, and Mann
# Whitney U test was used otherwise. In comparison of more than
# three independent groups, one-way ANOVA was used where the
# numerical variables were normally distributed and Kruskall Wallis
# test was used otherwise. For between group differences, Tukey’s
# test was used when the distribution of the data was homogenous
# and Games-Howell test was used otherwise. Between group
# differences in nonparametric tests were evaluated with DwassSteel-Critchlow-Fligner test. Pearson Chi-Square test was used for
# categorical variables, and Fisher’s exact test was used for RXC
# tables. To evaluate the associations between numerical variables,
# Pearson test was used when the data were normally distributed
# and Spearman’s Rho was used otherwise. Statistical analyses were
# performed with Jamovi Project software (2019; Version 0.9.5.12)
# and p<0.05 was considered to be significant in statistical analyses.
# Results
# This study included 52 AA patients and 51 controls. There was
# no significant difference in age, sex, education status, cigarette
# smoking, height, weight, and body mass index (BMI) values
# between the groups (Table 1).
# Alopecia areata was localized only to scalp hair in 24 patients
# (%46.2). In 20 (38.5%) patients the disease duration was less than
# 1 month. In 29 patients (55.8%) single, patchy AA was found.
# According to SALT, the severity of AA was mild in 46 (86.4%)
# of the patients. The number of patients who had at least one poor
# prognostic criteria was 28 (53.8%). The most common poor
# prognostic criterion was family history (n=10, 19.2%). Beginning
# age of the disease was mean 27.5 (± 7.8) (Table 2).
# Median BDI total score of AA patients (8.5) was higher than that of
# the control group (2) (p<0.001). In AA patients, besides PSQI total
# score, subjective sleep quality, sleep latency, sleep disturbance,
# and daytime dysfunction subscale scores were statistically higher
# than those of the control group (p<0.001, p=0.002, p=0.001, and
# p<0.001 respectively). 
# Table 1. Comparisons of age, sex, education status, cigarette smoking, height, weight, and BMI values between the groups
# Group
# Patient (n=52) Control (n=51) p
# Age, Mean ± SD 28.8 ± 7.7 29.3 ± 8.7 0.792
# Sex Male. n (%) 40 (76.9) 40 (78.4)
# 0.854
# Female. n (%) 12 (23.1) 11 (21.6)
# Education status Primary school. n (%) 6 (11.5) 4 (7.8)
# 0,637
# Secondary school. n (%) 6 (11.5) 5 (9.8)
# High school. n (%) 19 (36.5) 15 (29.4)
# University. n (%) 21 (40.4) 27 (52.9)
# Cigarette smoking No. n (%) 27 (51.9) 31 (60.8)
# 0.365
# Yes. n (%) 25 (48.1) 20 (39.2)
# Height (cm), Mean± SD 174.3 ± 9.3 171.4 ± 8.6 0.107
# Weight (kg), Mean ± SD 70.5 ± 11.6 71.3 ± 11.6 0.741
# BMI (kg/m2), Mean ± SD 23.2 ± 3.3 24.1 ± 2.6 0.103
# BMI: body mass index, SD: standard deviation
# Table 2. Clinical features of the individuals
# n (%)
# Localization of alopecia areata Only scalp 24 (46.2)
# Only beard 18 (34.6)
# Only scalp, eyelashes 5 (9.6)
# Scalp+ beard 4 (7.7)
# Scalp + eyelashes + eyebrows 1 (1.9)
# Type of alopecia areata Single patch 29 (55.8)
# Multiple patches 23 (44.2)
# Alopecia areata severity (Mild) Hair loss < %25 46 (88.5)
# (Moderate) Hair loss %26-50 5 (9.6)
# (Severe) Hair loss %50 1 (1.9)
# Onychodistrophy No 45 (86.54)
# Yes 7 (13.46)
# Poor prognostic criteria No 28 (53.8)
# Yes 24 (46.2)
# Atopy history 8 (15.4)
# Family history 10 (19.2)
# Longer than 5 years 3 (5.8)
# Asthma 3 (5.8)
# Allergic rhinitis 4 (7.7)
# Atopic dermatitis 3 (5.8)
# Age of onset of disease 27.5 ± 7.8
# Previous treatments No 36 (69.2)
# Topical 8 (15.4)
# Intralesion 7 (13.5)
# Systemic 1 (1.9)
# Onychodystrophy was detected in 7 patients (13.46%). As
# onychodystrophy type, 5 patients (9.6%) had pitting, 1 patient
# had longitudinal striation, and 1 patient (1.9%) had opaque nail.
# No difference could be found between patients who had or who
# didn’t have onychodystrophy in BDI, PSQI total score, and PSQI
# subscale scores.
# Comparisons for Beck Depression Inventory scores demonstrated
# that the localization of alopecia areata didn’t cause any effect
# (p=0.303). BDI scores of the patients who had moderate or severe
# alopecia areata were higher than those of the patients who had
# mild disease (p=0.023). No difference could be found in BDI score
# according to the presence or absence of poor prognostic criteria.
# Evaluation for the presence of poor prognostic criteria separately
# demonstrated that the BDI score was higher in the presence of
# only atopic dermatitis (p=0.016). Prior treatment did not affect the
# mean BDI score (Table 3).
# Comparisons for the Pittsburgh Sleep Quality Index (PSQI)
# revealed no difference for alopecia areata localization. Although
# scores were higher in patients with moderate or severe alopecia
# areata, the difference couldn’t reach statistical significance
# (p=0.092). No difference could be found in PSQI scores according
# to the presence or absence of poor prognostic criteria. Evaluation
# of the PSQI scores in the presence of separate poor prognostic
# criteria revealed that the presence of alopecia areata for more than
# 5 years (p=0.001) and presence of atopic dermatitis (p=0.016)
# were associated with higher PSQI scores (Table 3).
# Comparisons in terms of gender revealed that in the patient group
# the median BDI (16) and PSQI (7.5) scores in females were
# statistically significantly higher than BDI (7.5) and PSQI (6)
# scores in males (p=0.026 and p=0.012, respectively). Also in the
# control group the median BDI (9) and PSQI (4) scores in females
# were statistically significantly higher than BDI (1.5) and PSQI (2)
# scores in males (p=0.001 and p=0.035, respectively)
# Table 3. Association between the clinical features of alopecia areata and BDI, PSQI scores
# BDI p PSQI p
# Localization of alopecia areata
# Limited to scalp, (n=24) 9 [3.5 – 16]
# 0.303
# 7.5 [4.5 – 9]
# 0.740
# Limited to beard, (n=18) 7 [4 – 16] 5.5 [5 – 8]
# Only eyebrows, eyelashes, (n=5) 17 [13 – 19] 7 [6 – 13]
# Scalp + beard, (n=4) 11 [9 – 15] 7 [3 – 11.5]
# Scalp + eyebrows, eyelashes (n=1) α 1 [1 – 1] 5 [5 – 5]
# Severity of alopecia areata
# Mild hair loss 25%, (n=46) 8 [4 – 15]
# 0.023*
# 6 [4 – 8]
# 0.092
# Moderate hair loss 26-50%, (n=6) 17.5 [12 – 18] 9 [9 – 9]
# Poor prognostic criteria
# No, (n=28) 8.5 [4.5 – 15.5]
# 0.576
# 6 [4.5 – 9]
# 0.372
# Yes, (n=24) 9 [4 – 17.5] 7 [5 – 9]
# Poor prognostic criteria
# Atopy, (n=8) 12.5 [6.5 – 23] 0.361 8 [5.5 – 10.5] 0.417
# Family history, (n=10) 6 [2 – 19] 0.862 8.5 [5 – 13] 0.160
# Onychodystrophy (n=7) 17 [6 – 18] 0.243 7 [5 – 9] 0.639
# More than 5 years (n=3) 6 [4 – 12] 0.569 5 [4 – 5] 0.001*
# Asthma (n=3) 6 [0 – 15] 0.376 4 [2 – 7] 0.184
# Allergic rhinitis (n=4) 8.5 [3.5 – 12.5] 0.570 7.5 [4.5 – 8] 0.671
# Atopic dermatitis (n=3) 28 [18 – 39] 0.016* 12 [9 – 14] 0.016*
# Previous treatments
# No, (n=36) 8 [4 – 15]
# 0.393
# 6 [5 – 8.5]
# 0.434
# Yes, (n=16) 11 [5 – 18.5] 7 [4.5 – 10]
# *p<0.05 Mann Whitney U test was used. Descriptive statistics were given as median [IQR].
# α: Not included in analyses. AA, alopecia areata; BDI: Beck Depression Inventory, IQR: Interquartile Range, PSQI: Pittsburgh Sleep Quality Index
# Discussion
# In our study sleep quality of alopecia areata patients which was
# measured by PSQI scale was lower than that of the control group.
# There may be a two-way relationship between sleep and AA. Sleep
# deprivation was reported to increase serum interleukin (IL)-1 and
# tumor necrosis factor in mice[16]. By this way, decreased sleep
# quality might induce autoimmunity and cause AA in addition to
# other autoimmune diseases. On the other hand, AA may increase
# susceptibility to depression by causing loss of self-esteem due to
# induction of a loss in self-esteem [3]. In a previous study which
# evaluated sleep quality in AA patients, the Epworth Sleepiness
# Scale was applied to 105 AA patients and the mean ESS score was
# found to be 5.66±3.93 [17]. Although there was no control group
# in this study, considering that no difference could be found from
# a previous study on the normal Japanese population, the sleep
# quality in AA patients was hypothesized to be normal. Absence
# of a control group is a major limitation of this study. This might
# have prevented finding a significant result. To the best of our
# knowledge, no previous study had evaluated sleep quality in AA
# patients with PSQI.
# In our study, the BDI scores in the AA group was higher than the
# control group. This result suggests the findings of the previous
# studies in the literature. Sellami et al used the Hospital Anxiety and
# Depression Scale and found higher depression and anxiety scores
# in the AA group than the control group [18]. Another controlled
# study using the Hamilton Depression Scale found that depression
# scores of the AA patients were higher than the control group [19].
# The prevalence of onyschodystrophy in AA patients was reported
# to be between 7-66% in previous studies [9]. The rate we detected
# (13.46%) was in accordance with previous studies. Pitting, which
# was the most common nail change in our study, has also been
# reported as the most frequent nail change in most of the previous
# studies[10]. Nail changes were more commonly reported in severe
# AA forms like AA totalis (AAT) and AA universalis (AAU) [20].
# In our study, the absence of more severe AA types like AAU and
# AAT may have caused low rate of onychodystrophy and absence
# of a relationship between the presence of onychodystrophy and the
# PSQI and the BDI scores.
# In our study, depression level was significantly higher in patients with severe disease measured by SALT; the disturbance in sleep
# quality was also higher in these patients but the difference could
# not reach statistical significance. In most of the studies in the
# literature, severity of the psychiatric symptoms like depression and
# anxiety increased with increasing severity of the disease [18,19].
# We couldn’t find a relationship between the localization of AA
# and depression or sleep quality. Aghaei et al. reported higher rates
# of depression in AA patients with face involvement [21] which
# couldn’t be found in other two studies [19,22].
# No association could be found in our study between the beginning
# age of the study or disease duration and depression or sleep
# quality similar to the findings of previous studies [19,22]. Firooz
# et al. reported longer disease duration was associated with higher
# hopelessness about the treatment [23].
# In most of the studies that evaluated depression and anxiety levels,
# women were found to have higher levels than men [18,19,22].
# This finding was evaluated by some authors as that the aesthetic
# stress of women was higher than that of men [19]. In our study,
# the level of depression in female AA patients was higher and sleep
# quality was more impaired than male patients. However, we think
# that it would be wrong to interpret this finding as AA has more
# psychological effects in women. Because, in this age group, the
# level of depression is higher in females than that in males and sleep
# quality is more impaired [24]. However, the results emphasize the
# importance of screening for women with AA in terms of psychiatric
# symptoms.
# In our study, the evaluation of the effect of poor prognostic criteria
# on AA patients in depression and sleep quality revealed that the
# presence of atopic dermatitis was associated with an increase in
# depression level and deterioration in sleep quality. Considering the
# association between atopic dermatitis and psychiatric symptoms,
# this finding is not a surprise. The evaluation of sleep quality in
# 100 patients with atopic dermatitis by PSQI revealed poor sleep
# quality [25].
# Conclusion
# The results of our study support the long-standing relationship
# between AA and psychiatric disorders and indicate that sleep
# quality is impaired as well as the increase in depression level. In
# particular, a more careful assessment of female AA patients and
# patients with comorbid atopic dermatitis is important in order not
# to miss comorbid psychiatric problems.
# """

summarizer = AbstractiveSummarizer()
summarizer.generate_summary(TEXT_TO_SUMMARIZE) 

# TEXT_TO_SUMMARIZE = """
# FINAL REPORT -
# PORTABLE AP CHEST FILM __ AT ___
# CLINICAL INDICATION: __ -year-old with nasogastric tube placement.
# Comparison to prior study dated ___ at ___.
# A series of three portable AP sequential images of the chest, the first at
# ___, the second at ___ and the third at ___, are submitted.
# IMPRESSION:
# There has been interval attempted placement of a nasogastric tube which
# courses into the stomach but the tip ends up in the mid esophagus on all three
# images. Overall, cardiac and mediastinal contours are stable. Lungs are
# relatively well inflated. The subtle opacity in the right mid lung on the
# previous study does not persist and therefore is felt to correspond to an area
# of patchy atelectasis. No focal airspace consolidation is seen to suggest
# pneumonia. No pleural effusions or pneumothorax.
# """


# summarizer.generate_summary(TEXT_TO_SUMMARIZE)
# print(summarizer.generate_summary(TEXT_TO_SUMMARIZE))
    
@app.route('/summarizer', methods=['POST'])
def home():
    request_data = request.get_json()
    text = request_data['text']
    return str(text)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')