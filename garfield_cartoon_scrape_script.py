#!/usr/bin/env python
# coding: utf-8

### scrapnąć wszystkie komiksy garfielda ze strony mirrora. >> 01.iv.23 vB
# http://pt.jikos.cz/garfield/


import urllib.request
from bs4 import BeautifulSoup as bs
import requests
import re
from time import sleep

  

def getHTMLdocument(url):
    # function to extract html document from given url
    # request for HTML document of given url
    response = requests.get(url)
    return response.text

def get_linki_lat(url):
    # zwraca liste urli poszczególnych roczników garfielda
    lista_ul = []
    html_document = getHTMLdocument(url)
    soup = bs(html_document, 'html.parser')
    for link in soup.find_all('a',                #znajdź wszystkie pola <a...
                          attrs={'href': re.compile("^/gar")}):  #gdzie atrybut href zaczyna się od "/gar"
        lista_ul.append("http://pt.jikos.cz"+link.get('href'))  
    return(lista_ul)  

def get_linki_obrazow(url):
    # zwraca liste urli poszczególnych komiksów garfielda z miesiąca określonego linkiem podanym w argumencie
    lista_uo = []
    html_document = getHTMLdocument(url)
    soup = bs(html_document, 'html.parser')
    for link in soup.find_all('img',              #znajdź wszystkie pola <img...
                          attrs={'src': re.compile("^http")}):   #gdzie src zaczyna się od "http"
        lista_uo.append(link.get('src'))  
    return(lista_uo)

def get_obrazek(sciezka, url):
    # zapisuje obrazek z podanego url używając ostatniego segmentu urla po znaku "/" jako nazwy pliku
    # uwzględnia ściezkę do zapisu podaną w argumencie
    # jezeli napotka wyjątek, wypisze jaki to błąd i dla jakiego url wystąpił, potem zakończy
    try:
        urllib.request.urlretrieve(url, filename=sciezka+url.split("/")[-1])
    except Exception as e:
        print(e, "in: ")
        print(url)

        
        
# __main__        
        
## url startowy z którego pobrana zostaje lista urli roczników        
roczniki = get_linki_lat("http://pt.jikos.cz/garfield/1978/1/")
#print(roczniki)

i =0  #taki sobie licznik sprawdzonych urli plików
sciezka = "./garf78/"  #sciezka do zapisu

for rocznik in [roczniki[0]]:   #ewentualnie zdefiniować ograniczenie listy np.: ...in [roczniki[0]] lub in roczniki[39:]
    print("--> rocznik ", rocznik)
    for miesiac in range(1,13):
        print("-> mc ", miesiac, end=".. ")
        obrazky = get_linki_obrazow(rocznik+str(miesiac)+"/")
        #print(obrazky)
        sleep(9)  #opcja odciążenia serwera przez dodanie dodatkowej przerwy między pobraniami 
        for obrazek in obrazky:
            print(".", end="")  #kropka postępu pobierania
            get_obrazek(sciezka,obrazek)
            #sleep(1) #opcja odciążenia serwera przez dodanie 1 sekundowej przerwy między pobraniami 
            i+=1
        print()
    print(i, "# \n")
print("\n fin as of", i, " files.")


