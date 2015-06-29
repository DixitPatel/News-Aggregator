# -*- coding: utf-8 -*-
"""
Created on Wed Apr 09 12:30:05 2014

@author: dhake
"""
import BeautifulSoup
import urllib
import urllib2
import json
 
def main():
    query = "science"+" "
    print bing_search(query, 'News')
   # print bing_search(query, 'Image')
 
def bing_search(query, search_type):
    try:
        #search_type: Web, Image, News, Video
        key= 'osplyqfLOwWE29rH2VDyfBZQTMBkuiMpfqOOouE8tzM'
        query = urllib.quote(query)
        # create credential for authentication
        user_agent = 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1; Trident/4.0; FDM; .NET CLR 2.0.50727; InfoPath.2; .NET CLR 1.1.4322)'
        credentials = (':%s' % key).encode('base64')[:-1]
        auth = 'Basic %s' % credentials
        url = 'https://api.datamarket.azure.com/Data.ashx/Bing/Search/'+search_type+'?Query=%27'+query+'India%27&$top=25&$format=json'
        request = urllib2.Request(url)
        request.add_header('Authorization', auth)
        request.add_header('User-Agent', user_agent)
        request_opener = urllib2.build_opener()
        response = request_opener.open(request) 
        response_data = response.read()
        json_result = json.loads(response_data)
        print json_result
        for i in range(0,12):
            cname = json_result['d']['results'][i]['Source'] 
            print cname
            src_name(cname,json_result,i)
    except urllib2.URLError:
        print ''
    except IndexError:
        print ''
        
    
           
def src_name(result_src,json_result,x):
    result_url = json_result['d']['results'][x]['Url']
    print result_url
    page = urllib2.urlopen(result_url).read()
    soup = BeautifulSoup.BeautifulSoup(page)
    soup.prettify()
    try:
        if result_src=="DNA India":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'content-story'})
            res = res.find('img').get('src')
        elif result_src=="Hindustan Times":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'body_txt'})
            print res.text
        elif result_src=="Money Control":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'op_gd14 FL'})
            print res.text
        elif result_src=="Yahoo Finance":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'body yom-art-content clearfix'})
            print res.text
        elif result_src=="Times of India":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'Normal'})
            print res.text      
        elif result_src=="Yahoo! India News":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'yom-mod yom-art-content '})
            print res.text     
        elif result_src=="NDTV":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'pdl200'})
            print res.text
        elif result_src=="The Hindu":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'article-text'})
            print res.text
        elif result_src=="India TV":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'standard'})
            print res.text
        elif result_src=="MSN India":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'svrichtxt cf'})
            print res.text
        elif result_src=="The Business Times":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'real-content'})
            print res.text
        elif result_src=="The Huffington Post":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'content'})
            print res.text
        elif result_src=="Zee News":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'lft-con'})
            print res.text
        elif result_src=="India Today":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'fullstorytext'})
            print res.text
        elif result_src=="The Indian Express":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'section-stories'})
            print res.text
        elif result_src=="The Hindu Business Line":
            r_title = json_result['d']['results'][x]['Title']
            print r_title
            res = soup.find('div' , {'class': 'article-text '})
            print res.text
    except AttributeError:
         print ''
    except urllib2.HTTPError, e:
         print e.code
    except urllib2.URLError, e:
         print e.args
    
    
    
    #print res
  #  result_list = json_result['d']['results']
   # print json_result['d']['results'][0]['Description'] 
    #print len(result_list)
   # for i in range(0,12):
   #   print json_result['d']['results'][i]['Description'] 

#    for i in range(len(result_list)):
 #   print result_list[0]
   # return result_list
 
if __name__ == "__main__":
    main()