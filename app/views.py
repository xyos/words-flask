# -*- coding: utf-8 -*-
import os
import operator
from flask import Flask, request, redirect, url_for
from werkzeug import secure_filename
from app import app
from flask import render_template
import unicodedata
import re
import codecs

ALLOWED_EXTENSIONS = set(['txt'])

import random
import bisect
import collections

def cdf(weights):
    total = sum(weights)
    result = []
    cumsum = 0
    for w in weights:
        cumsum += w
        result.append(cumsum / total)
    return result

def choice(population, weights):
    assert len(population) == len(weights)
    cdf_vals = cdf(weights)
    x = random.random()
    idx = bisect.bisect(cdf_vals, x)
    return population[idx]

def remove_accents(input_str):
    nkfd_form = unicodedata.normalize('NFKD', input_str)
    return u"".join([c for c in nkfd_form if not unicodedata.combining(c)])

def ngram(text, n):
    ngrams = [text[i:i+n] for i in range(len(text)-n+1)]
    wordcount = {}
    total = 0
    for word in ngrams:
        match = re.match('^[a-zA-Zñ]+$', word, re.UNICODE)
        if match:
            if word not in wordcount:
                wordcount[word] = 1
            else:
                wordcount[word] += 1
            total += 1
    population = []
    weigths = []
    for k, val in wordcount.items():
        population.append(k)
        weigths.append(1.0 * val/total * 1.0)

    return population, weigths

def random_text(pop, wei,n):
    text = ""
    for i in range(120/n):
        text += choice(pop, wei)
    return text

def count_words(file):
    text = unicode(file.read().decode('Latin-1'))
    text = remove_accents(text.lower())
    pop_ngram1, wei_ngram1 = ngram(text, 1)
    pop_ngram2, wei_ngram2 = ngram(text, 2)
    pop_ngram3, wei_ngram3 = ngram(text, 3)
    n1grams = random_text(pop_ngram1,wei_ngram1,1)
    n2grams = random_text(pop_ngram2,wei_ngram2,2)
    n3grams = random_text(pop_ngram3,wei_ngram3,3)
    
    return render_template('results.html', n1grams=n1grams, n2grams=n2grams, n3grams=n3grams)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            return count_words(file)
    return render_template('index.html')
