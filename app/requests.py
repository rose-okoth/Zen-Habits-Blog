import urllib.request,json 
from flask import render_template,request
from . import main
from config import QUOTES_BASE_URL
from .models import quotes

def configure_request(app):
    global QUOTES_BASE_URL
    QUOTES_BASE_URL = app.config['QUOTES_BASE_URL']

def get_quotes(quote):
    get_quotes_url = QUOTES_BASE_URL.format(quote)

    with urllib.request.urlopen(get_quotes_url) as url:
        get_quotes_data = url.read()
        get_quotes_response = json.loads(get_quotes_data)

        quotes_results = None

        if get_quotes_response['quote']:
            quotes_results_list = get_quotes_response['quote']
            quotes_results = process_results(quotes_results_list)

    return quotes_results

def process_results(quotes_list):
    '''
    Function that processes the quotes results
    '''
    author = []
    quote = []

    for quotes_item in quotes_list:

        author.append(quotes_item.get('author'))
        quote.append(quotes_item.get('quote'))
        
    quotes_results=zip(author,quote)
    return quotes_results
