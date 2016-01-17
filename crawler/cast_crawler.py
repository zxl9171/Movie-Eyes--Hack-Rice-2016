import urllib2
from bs4 import BeautifulSoup
#we could learn BeautifulSoup package from "http://www.crummy.com/software/BeautifulSoup/bs4/doc/"
import re
import urlparse  #To get complete URL from the website
from urlparse import urljoin
import os
import sys
import urllib
import csv
import unicodedata
import httplib2
import json
import requests
import time

def downloadpage(url,header):
    h = httplib2.Http(".cache")
    (resp_headers, content) = h.request(url, "GET", headers = header)
    return content

def downloadpage1(url):
    req=urllib2.Request(url)
    con = urllib2.urlopen(req)
    doc = con.read()
    con.close()
    return doc

def querytourl(query):
    query=query.split()
    query='+'.join(query)
    url = 'http://www.bing.com/search?q='+query+'imdb+'+'movie+'+'cast'
    return url

def querytopage(query):
    url=querytourl(query)
    doc=downloadpage1(url)
    return doc

# Get the name, image, and known works of a actor or actress given its corresponding personal page url
def fill_personal_info(page_doc):
    soup = BeautifulSoup(page_doc, 'html.parser')
    name = ''
    image_url = ''
    known_works = {}
    for link0 in soup.find_all('h1'):
        name = link0.span.string # this is the name of actor/actress
    for link0 in soup.find_all('a'):
        for link1 in link0.find_all('img'):
            if link1.get('id') == 'name-poster':
                image_url = link1.get('src')
    for link0 in soup.find_all('div', id="knownfor"):
        for link1 in link0.find_all('a'):
            if 'img' in str(link1):
                known_works[link1.img.get('title')] = link1.img.get('src')
                #print link1.img.get('src')
                #print link1.img.get('title')
    # print known_works
    return [name, image_url, known_works]

# Get the other info of actor/actress
def fill_personal_info1(page_doc):
    # print 'website is: ' + page_doc
    soup = BeautifulSoup(page_doc, 'html.parser')
    birth_monthday = ''
    birth_year = ''
    birth_place = ''
    for link0 in soup.find_all('td'):
        for link1 in link0.find_all('a'):
            if birth_monthday != '':
                break
            if 'birth_monthday' in str(link1.get('href')):
                birth_monthday = link1.string
    for link0 in soup.find_all('td'):
        for link1 in link0.find_all('a'):
            if birth_year != '':
                break
            if 'birth_year' in str(link1.get('href')):
                birth_year = link1.string
    for link0 in soup.find_all('td'):
        for link1 in link0.find_all('a'):
            if birth_place != '':
                break
            if 'birth_place' in str(link1.get('href')):
                birth_place = link1.string
    # print birth_monthday, birth_year, birth_place
    mini_bio_info = ''
    for bio in soup.find_all('div',class_="soda odd"):
        for par in bio.find_all('p'):
            if '<br' in str(par):
                biog=re.sub('<br/>','', str(par))
                biog=re.sub('<p>','',biog)
                biog=re.sub('</p >','',biog)
                b_soup=BeautifulSoup(biog,'html.parser')
                [s.extract() for s in b_soup('a')]
                mini_bio_info = str(b_soup)
                mini_bio_info = re.sub('\n','',mini_bio_info).lstrip()
        #print str(bio)
        break
    return [birth_monthday+', '+birth_year, birth_place, mini_bio_info]

# Get the news of the actors.
def get_news_title(url):
    '''Given a url return all news title on that page'''
    header1={'Host': 'www.imdb.com',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive',
'Content-Type':'text/xml; charset=UTF-8',
         'Pragma':'no-cache'}
    one_doc=downloadpage(url,header1)
    #print one_doc
    one_soup=BeautifulSoup(one_doc,'html.parser')
    news=[]
    for title in one_soup.find_all('h2'):
        newstitle=re.sub('<h2>','',str(title))
        newstitle=re.sub('</h2>','',newstitle)
        news.append(newstitle)
    return news

# jt's methods that used to get the minibio info from actors' biography. Not used in this program.
'''
def getinfo(url):
#while 1:
    header1={'Host': 'www.imdb.com',
'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0',
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Connection': 'keep-alive',
'Content-Type':'text/xml; charset=UTF-8',
         'Pragma':'no-cache'}
    one_doc=downloadpage(url,header1)
    #print one_doc
    one_soup=BeautifulSoup(one_doc,'html.parser')
    for bio in one_soup.find_all('div',class_="soda odd"):
        for par in bio.find_all('p'):
            if '<br' in str(par):
                biog=re.sub('<br/>','', str(par))
                biog=re.sub('<p>','',biog)
                biog=re.sub('</p >','',biog)
                b_soup=BeautifulSoup(biog,'html.parser')
                [s.extract() for s in b_soup('a')]
                print b_soup
        #print str(bio)
        break
'''

def main():
    doc = querytopage('the lives of others')
    # doc = querytopage('big bang theory')
    soup = BeautifulSoup(doc,'html.parser')
    cast_page_url = ''
    for link0 in soup.find_all('h2'):
        for link1 in link0.find_all('a'):
            # print link1
            if 'http://m.imdb.com/title' in str(link1) and 'fullcredits' in str(link1):# what does it mean?
                # print link1['href']
                match = re.search(r'http://m.imdb.com/title/\w*/fullcredits', link1.get('href'))
                if match:
                    #print match.group()
                    cast_page_url = match.group()
                else:
                    print 'did not find the film id'
    print 'the movie page url in imdb is: ' + cast_page_url
    doc = querytopage(cast_page_url)
    header = {'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
              'Accept-Encoding' : 'gzip, deflate',
              'Accept-Language' : 'en-US,en;q=0.5',
              'Connection' : 'keep-alive',
              'Host' : 'www.imdb.com',
              'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:42.0) Gecko/20100101 Firefox/42.0'}
    doc = downloadpage(cast_page_url, header)
    #print doc
    soup = BeautifulSoup(doc,'html.parser')
    personal_page_url = []
    for link0 in soup.find_all('a'):
        # print link0
        if '/name' in str(link0) and 'itemprop=' in str(link0):
            personal_page_url.append('http://www.imdb.com'+link0.get('href'))
            #print link0
    # print personal_page_url # test
    # print 'personal page[0] url is: ' + personal_page_url[0] # test
    # doc = downloadpage1(personal_page_url[3]) # test: personal_page_url[3] is nm0876300
    # fill_personal_info(doc) # test

    # doc = downloadpage1('http://www.imdb.com/name/nm0311476/bio?ref_=nm_ov_bio_sm') # test:
    # fill_personal_info1(doc) # test:
    info = []
    for url in personal_page_url:
        doc = downloadpage1(url)
        name, photo, known_works = fill_personal_info(doc)
        full_bio_page_url = re.sub('\?.+','bio?ref_=nm_ov_bio_sm',url)
        # print full_page_url # test
        doc = downloadpage1(full_bio_page_url)
        date_of_birth, birth_place, bio_info = fill_personal_info1(doc)
        # print date_of_birth
        news_page_url = re.sub('\?.+','news',url)
        news = get_news_title(news_page_url)
        element = {'name' : name, 'avatar' : photo, 'films' : known_works.keys(),
                   'birth_date' : re.sub(r'\xa0',r' ',date_of_birth), 'related_pics' : known_works.values(),
                   'bio' : str(bio_info), 'news' : news}
        info.append(element)
    '''
    for key, value in cast_data.iteritems(): # test
        print key, value, '\n'
    '''
    #print cast_data # test
    #print json.dumps(info) # test
    #print '5 is ' + json.dumps(info[5])
    #print '6 is ' + json.dumps(info[6])
    #print '7 is ' + json.dumps(info[7])
    #print '8 is ' + json.dumps(info[8])
    #print '9 is ' + json.dumps(info[9])
    requests_headers = {'content-type': 'application/json'}
    '''
    with open('movie_eye_data.txt', 'w') as outfile:
        json.dump(info, outfile)
    '''
    for e in info:
        r = requests.post("http://mzpz.me:3000/api/info", data=json.dumps(e), headers = requests_headers)
        print(r.status_code, r.reason)
        print 'the content of the server response is: ' + r.text




if __name__ == '__main__':
    main()