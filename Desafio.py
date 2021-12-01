import urllib.request
from bs4 import BeautifulSoup 
import json
from urllib.parse import urlparse

def getHtmlCode(URLCode):
    resposta = urllib.request.urlopen(URLCode)
    getStringHTML = resposta.read().decode("UTF-8")
    HtmlCode = BeautifulSoup(getStringHTML, 'html.parser')
    for script in HtmlCode(["script", "style"]):
        script.extract()

    return HtmlCode

def getTitle(HtmlCode):
    title = HtmlCode.find('title')

    return title.string

def getURL(HtmlCode):
    array = []    
    for link in HtmlCode.findAll('a'):
        hrefs = link.get("href")
        if hrefs != None and hrefs.startswith('http'):
            array.append(hrefs)
    jason = json.dumps(list(set(array)))  

    return jason


def getH1(HtmlCode):
    array = []
    for h1 in HtmlCode.findAll('h1'):
        array.append(h1.text.strip())
    jason = json.dumps(array)
    
    return jason

# def getText(HtmlCode):    
#     texto = HtmlCode.get_text()

#     return texto

def getMetas(HtmlCode):
    array = []
    for metas in HtmlCode.findAll('meta'):
        array.append(metas.attrs)
        #if metas.get("content") != None:  
            #array.append(metas.get("content"))   
    jason = json.dumps(array)

    return jason

def getDomain(HtmlCode):
    array = []
    listaURLs= json.loads(getURL(HtmlCode))
    for links in listaURLs:
        dominio = urlparse(links).netloc
        array.append(dominio)
    
    jason = json.dumps(list(set(array)))

    return jason

# def getSocialNetworks(HtmlCode):
#     array = []
#     media = ['facebook', 'linkedin', 'whatsapp', 'youtube', 'twitter', 'instagram']  
#     listaURLs = json.loads(getURL(HtmlCode))
#     for social in listaURLs:
#         if 'facebook' in social:
#             array.append("FACEBOOK: "+social)
#         elif 'instagram' in social:
#             array.append("INSTAGRAM: "+social)
#         elif 'linkedin' in social:
#             array.append("LINKEDIN: "+social)
#         elif 'youtube' in social:
#             array.append("YOUTUBE: "+social)
#         elif 'whatsapp' in social:
#             array.append("WHATSAPP: "+social)
#         elif 'twitter' in social:
#             array.append("TWITTER: "+social)
    
#     jason = json.dumps(array)
#     return jason

def getSocialNetworks(HtmlCode):
    array = []
    social = ['facebook', 'linkedin', 'whatsapp', 'youtube', 'twitter', 'instagram']  
    listaURLs = json.loads(getURL(HtmlCode))
    for link in listaURLs:
        for algum in social:
            if algum in link:
                array.append(algum+": "+link)
    jason = json.dumps(array)
    return jason












HtmlCode = getHtmlCode('https://skeel.com.br/contato/')
#print(getTitle(HtmlCode))
#print(getURL(HtmlCode))
#print(getH1(HtmlCode))
#print(getMetas(HtmlCode))
#print(getDomain(HtmlCode))
print(getSocialNetworks(HtmlCode))
