from locale import currency
from this import d
from django.shortcuts import render
from searchapp import func
import requests

from bs4 import BeautifulSoup

def parse_currency():
    DOLLAR_URL = 'https://finance.rambler.ru/currencies/USD'
    dollar_response = requests.get(DOLLAR_URL)
    dollar_parser = BeautifulSoup(dollar_response.text, 'html.parser')
    dollar_currency_item = dollar_parser.find('div', 'finance-currency-plate__currency').text.strip()
    dollar_string = '1 $ = ' + str(round(float(dollar_currency_item), 2)) + ' ₽'
    EURO_URL = 'https://finance.rambler.ru/currencies/EUR'
    euro_response = requests.get(EURO_URL)
    euro_parser = BeautifulSoup(euro_response.text, 'html.parser')
    euro_currency_item = euro_parser.find('div', 'finance-currency-plate__currency').text.strip()
    euro_string = '1 € = ' + str(round(float(euro_currency_item), 2)) + ' ₽'
    return [dollar_string, euro_string]

def search_sentence(request): #функция для отправки списка в html
    search_check = False
    [dollar, euro] = parse_currency()
    if 'q' in request.GET and request.GET["q"] != '':
        search_check = True
        result = func.search_sentence(request.GET["q"], "words.txt") #отправка слова которое нужно найти и файла с текстом
        return render(request, 'index.html', context={"sentences": result, 'check': search_check, "dollar": dollar, "euro": euro}) #отправка списка и переменную которая проверяет есть ли запрос
    return render(request, 'index.html', {"dollar": dollar, "euro": euro})  #если пустое то обновляется страница


