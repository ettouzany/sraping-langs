from asyncore import write
from cgitb import html
from operator import countOf, truediv
from pickle import TRUE
from bs4 import BeautifulSoup as bs
import json
import requests
url = "https://www.learnjavaonline.org/"


output = {}
parts_num = 0
file_ = "csharp"
title = "Learn C#"
desc = "C# is a static programming language which lets us write code that runs atop Microsoft's .NET framework."
pre = []
def get_lecture(ht):
    parts = []
    print(ht.find('h1'))
    print('\t',ht.find_all('h3'))
    for item in ht.find_all(['h1','h2','h3']):
        # print('\t',item.find_next_siblings()[2])
        global parts_num
        parts_num += 1
        nextNode = item
        ml = ""
        while True:
            nextNode = nextNode.find_next_sibling()
            try:
                tag_name = nextNode.name
            except AttributeError:
                tag_name = "h3"
            if tag_name == "h3" or tag_name == "h2" :
                break
            else:
                ml += str(nextNode)
        if item.text != 'Exercise':
            parts.append({'title':item.name !="h1" and item.text or "Introduction",'html':ml})
    return(parts)

res = requests.get(url)
with open(file_+'.json', 'w') as file:
    soup = bs(res.content, 'lxml')
    chapters = soup.find('h3').find_next_sibling()
    # print(chapters.text)
    chaps = {}
    contents = {}
    output['course'] = title
    output['description'] = desc
    output['prerequisites'] = pre
    output['lectures'] = []
    for item in chapters:
        if '\n' not in item.text:
            chaps[item.text] = item.find('a', href=True)['href']
            contents[item.text] = requests.get(url+chaps[item.text])
            contents[item.text] = bs(contents[item.text].content, 'lxml')
            output['lectures'].append({'title':item.text,'parts':get_lecture(contents[item.text])})
    output['parts'] = parts_num
    json.dump(output, file, indent=4, separators=(',',': '))

# file.wite(str(contents[item.text]))