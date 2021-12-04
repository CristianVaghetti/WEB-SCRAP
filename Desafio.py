from ctypes import Array
import urllib.request
from bs4 import BeautifulSoup 
import json
from urllib.parse import urlparse
import re

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'  #parametros pro teste do regex para emails
regex_tel = '^\([1-9]{2}\) (?:[2-8]|9[1-9])[0-9]{3}\-[0-9]{4}$' #parametros pro teste do redex para telefones
def getHtmlCode(URLCode):
    resposta = urllib.request.urlopen(URLCode) 
    getHTML = resposta.read().decode("UTF-8") # carrega o código na forma de string 
    HtmlCode = BeautifulSoup(getHTML, 'html.parser') # converte a string em objeto
    for script in HtmlCode(["script", "style"]): # remove as tag script e style do codigo
        script.extract()  

    return HtmlCode # retorna o código HTML na forma de objeto

def getTitle(HtmlCode):
    title = HtmlCode.find('title')

    return title.string

def getURL(HtmlCode):
    array = []    
    for link in HtmlCode.findAll('a'): # procura todas as tag <a> no código HTML
        hrefs = link.get("href") # pega o conteúdo de href
        if hrefs != None and hrefs.startswith('http'): # verifica se href tem conteúdo e verifica de esse conteúdo começa com http
            array.append(hrefs) #se começar com http ele insere no array (presuminto que se começa com http é url)
    jason = json.dumps(list(set(array)))

    return jason


def getH1(HtmlCode):
    array = []
    for h1 in HtmlCode.findAll('h1'):
        array.append(h1.text.strip()) #apos procurar a tag H1, ele insere o conteudo string da tag no array
    jason = json.dumps(array)
    
    return jason


def getMetas(HtmlCode):
    array = []
    for metas in HtmlCode.findAll('meta'):
        array.append(metas.attrs) # depois de achar a tag meta coloca o conteudo dessa tag em um array 
        #if metas.get("content") != None:  
            #array.append(metas.get("content"))   
    jason = json.dumps(array) # transforma o array em um json

    return jason


def getDomain(HtmlCode):
    array = []
    listaURLs= json.loads(getURL(HtmlCode)) # a função getURL retorna um json então tem que converter esse json em um objeto
    for links in listaURLs:
        dominio = urlparse(links).netloc # função que achei na internet pra pegar somente o dominio da url
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
    for link in listaURLs: # for para percorrer todas as urls retornadas da função getURL
        for algum in social: # vai percorrer o array social
            if algum in link: # comparar se o URL possui o conteudo da string do array social
                array.append(algum+": "+link) # concatena a string indice[algum] do array social + o URL que contem o algum 
    jason = json.dumps(array)
    return jason

def getText(HtmlCode):
    array = []
    for stringi in HtmlCode.findAll(): # vai percorrer todas as tags do codigo
        if stringi.string != None:
            array.append(stringi.string) # vai inserir no array somente se a tag possuir uma string 
           
    jason = json.dumps(list(set(array))) ################################ nesse caso, ele não sabe converter os acentos ---bug do codigo--- 
    
    return jason


# def getEmail(HtmlCode):
#     array = []
#     for stringi in HtmlCode.findAll(): # vai percorrer todas as tags do codigo
#         if stringi.string != None and stringi.string.startswith("E-mail"): # neste caso, so vai funcionar se a tag anunciando o email obedecer os formatos oferecidos
#             array.append(stringi.next_sibling.strip()) # uma vez que o enderço de email esta na proxima tag que esta anunciando-o o metodo next_sibling resolve 
#     jason = json.dumps(list(set(array)))
#     return jason

def getEmails(HtmlCode):
    array = []
    for strings in HtmlCode.findAll(): # vai percorrer todas as tags do codigo
        #if stringi.string != None and '@' in stringi.string :  # assim como está se a string conter @ ele já insere no array(pode não ser um email)
        if strings.string != None and re.fullmatch(regex, strings.string): # o regex vai fazer a checagem pra ver se a string é um email válido 
            array.append(strings.string.strip()) # se passar no teste vai pro array
    jason = json.dumps(list(set(array)))
    return jason



def getResume(HtmlCode):
    array = []
    desc = ["charset", "lang"]
    title = HtmlCode.find('title')
    array.append(title.string)
    for mendrulho in HtmlCode.findAll():
        if mendrulho.get("name") == "description":
            array.append(mendrulho.get("content"))
        for descrition in desc:
            if mendrulho.get(descrition) != None:
                array.append(mendrulho.get(descrition))
                        
    #jason = json.dumps(list(set(array)))
    return array

def getPhones(HtmlCode):
    array = []
    for strings in HtmlCode.findAll(): # vai percorrer todas as tags do codigo
        if strings.string != None and re.fullmatch(regex_tel, strings.string): # o regex_tel vai fazer a checagem pra ver se a string é um numer de telefone 
            array.append(strings.string.strip()) # se passar no teste vai pro array
    jason = json.dumps(list(set(array))) # pega o array e tranforma em json
    return jason







HtmlCode = getHtmlCode('https://skeel.com.br/contato/')

#print(getTitle(HtmlCode))
#print(getURL(HtmlCode))
#print(getH1(HtmlCode))
#print(getMetas(HtmlCode))
# print(getDomain(HtmlCode))
#print(getSocialNetworks(HtmlCode))
print(getEmails(HtmlCode))
#print(getText(HtmlCode))
#print(getResume(HtmlCode))
print(getPhones(HtmlCode))
