import requests
import urllib
import pandas as pd
from requests_html import HTML
from requests_html import HTMLSession
from bs4 import BeautifulSoup
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from flask import Flask
from flask import jsonify
app = Flask(__name__)

class GoogleCrawler():
    
    def __init__(self):
        self.url = 'https://www.google.com/search?q='    
    #  URL 萃取 From Google Search上 , using 第三方套件
    #  https://python-googlesearch.readthedocs.io/en/latest/
    def google_url_search_byOpenSource(query,tbs='qdr:m',num=10):
        array_url = [url for url in search('tsmc', tbs='qdr:m' , num=10)]
        return array_url
    # 網路擷取器
    def get_source(self,url):
        try:
            session = HTMLSession()
            response = session.get(url)
            return response
        except requests.exceptions.RequestException as e:
            print(e)
    # URL 萃取 From Google Search上
    def scrape_google(self,query):

        response = self.get_source(self.url + query)
        links = list(response.html.absolute_links)
        google_domains = ('https://www.google.', 
                          'https://google.', 
                          'https://webcache.googleusercontent.', 
                          'http://webcache.googleusercontent.', 
                          'https://policies.google.',
                          'https://support.google.',
                          'https://maps.google.',
                          'https://taipeitimes.com')

        for url in links[:]:
            if url.startswith(google_domains):
                links.remove(url)
        return links
    
# URL萃取器，有link之外，也有標題
#     qdr:h (past hour)
#     qdr:d (past day)
#     qdr:w (past week)
#     qdr:m (past month)
#     qdr:y (past year)
    def google_search(self,query,timeline='',page='0'):
        url = self.url + query + '&tbs={timeline}&start={page}&filter=0&lr=lang_en'.format(timeline=timeline,page=page)
        print('[Check][URL] URL : {url}'.format(url=url))
        response = self.get_source(url)
        return self.parse_googleResults(response)
    # Google Search Result Parsing
    def parse_googleResults(self,response):

        css_identifier_result = "tF2Cxc"
        css_identifier_title = "h3"
        css_identifier_link = "yuRUbf"
        css_identifier_text = "VwiC3b"
        soup = BeautifulSoup(response.text, 'html.parser')
        results = soup.findAll("div", {"class": css_identifier_result})
        output = []
        for result in results:
            item = {
                'title': result.find(css_identifier_title).get_text(),
                'link': result.find("div", {"class": css_identifier_link}).find(href=True)['href'],
                'text': result.find("div", {"class": css_identifier_text}).get_text()
            }
            output.append(item)
        return output
    
    # 網頁解析器
    def html_parser(self,htmlText):
        soup = BeautifulSoup(htmlText, 'html.parser')
        return soup
    # 解析後，取<p>文字
    def html_getText(self,soup):
        orignal_text = ''
        for el in soup.find_all('p'):
            orignal_text += ''.join(el.find_all(text=True))
        return orignal_text
    
    def word_count(self, text):
        counts = dict()
        stop_words = set(stopwords.words('english'))
        words = word_tokenize(text)
        #words = text.replace(',','').split()
        for word in words:
            if word not in stop_words:
                if word in counts:
                    counts[word] += 1
                else:
                    counts[word] = 1
        return counts
    def get_wordcount_json(self,whitelist , dict_data):
        data_array = []
        for i in whitelist:
            json_data = {
                'Date' : 'Hour1',
                'Company' : i , 
                'Count' : 0
            }
            data_array.append(json_data)
        return data_array
    def get_wordcount(self,whitelist , dict_data):
        for i in whitelist:
            if (i in dict_data):
                return dict_data[i]
        return 0
    def jsonarray_toexcel(self,data_array):
        df = pd.DataFrame(data=data_array)
        df.to_excel('result.xlsx' , index=False)
        return
@app.route("/")
def Hello():
    return "Hellow World"

@app.route('/google_search/<company>', defaults={'_from':None, '_to':None})
@app.route('/google_search/<company>/<_from>/<_to>')
def google_search(company, _from, _to):
    '''
    _from : (DD.MM.YYYY)
    _to : (DD.MM.YYYY)
    '''
    crawler = GoogleCrawler()
    query = '\"{company}\"'.format(company=company)
    if _from and _to:
        timeline = f"cdr:1,cd_min:{_from.replace('.', '/')},cd_max:{_to.replace('.', '/')}"
    else:
        timeline = "qdr:h"
    results = crawler.google_search(query, timeline, '1')
    print(results)
    arr = []
    with open('{company}.txt'.format(company=company), "w") as f:
        for i in results:
            arr.append(i['link'])
            f.write(i['link'] + '\n')
        f.close()
    return jsonify(arr)

@app.route("/query/<company>")
def query(company):
    result_wordcount = dict()
    crawler = GoogleCrawler()
    whitelist = [str(company)]
    end_result = crawler.get_wordcount_json(whitelist , [])
    try:
        with open('{company}.txt'.format(company=company),"r") as f:
            Target_URL = f.readline()
            while Target_URL != '':
                print(Target_URL.split('\n')[0])
                response = crawler.get_source(Target_URL.split('\n')[0])
                soup = crawler.html_parser(response.text)
                orignal_text = crawler.html_getText(soup)
                result_wordcount = crawler.word_count(orignal_text)
                count = crawler.get_wordcount(whitelist , result_wordcount)
                end_result[0]['Count'] = end_result[0]['Count'] + count
                Target_URL = f.readline()
            crawler.jsonarray_toexcel(end_result)
            f.close()
            return str(end_result)
    except:
        return 'Has no {company}.txt before'.format(company=company)

if __name__ == "__main__":
    print("app running")
    app.run(debug=True, host='0.0.0.0', port=8080)