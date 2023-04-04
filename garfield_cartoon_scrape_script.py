#!/usr/bin/env python
# coding: utf-8

# In[ ]:


### scrapnąć wszystkie komiksy garfielda ze strony mirrora. >> 01.iv.23 vB
# http://pt.jikos.cz/garfield/


# In[24]:


from bs4 import BeautifulSoup as bs
import requests
import re
  
# function to extract html document from given url
def getHTMLdocument(url):
    # request for HTML document of given url
    response = requests.get(url)
    # response will be provided in JSON format
    return response.text


## najpierw trzeba rozpracować strukturę elementów strony
# assign URL
url= "http://pt.jikos.cz/garfield/1989/1/"
  
# scrape html document
html_document = getHTMLdocument(url)

##zeby zobaczyć tresc strony zwrócona przez bs:
#print(html_document)
  
# create soap object
soup = bs(html_document, 'html.parser')
  
# # find all the <a> anchor tags  
# # with "href" attribute starting with "/gar" ,jak garfield
# for link in soup.find_all('a', 
#                           attrs={'href': re.compile("^/gar")}):
#     # display the actual urls
#     print(link.get('href'))  

# analogicznie: find all the <img> tags  
# with "src" attribute starting with "http" 
for link in soup.find_all('img', 
                          attrs={'src': re.compile("^http")}):
    # display the actual urls
    print(link.get('src'))  


# In[68]:


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


# In[70]:


#braki:
'''
http://picayune.uclick.com/comics/ga/2017/ga171029.jpg
http://picayune.uclick.com/comics/ga/2019/ga190108.gif
http://picayune.uclick.com/comics/ga/2019/ga190410.gif
http://picayune.uclick.com/comics/ga/2020/ga200411.gif
'''

