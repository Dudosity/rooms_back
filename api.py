#!flask/bin/python
# -*- coding: utf-8 -*-
from flask import Flask, jsonify
import requests
from lxml import html
import json
import http.client, urllib.parse
import datetime, time
from flask import send_file
from flask_cors import CORS

app = Flask(__name__)
cors = CORS(app, resources={r"/*": {"origins": "*"}})
cian_object = ""
time = datetime.datetime.now()
trip_object = ""
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpZCI6ImFiNzNkZWZjLTdkNzEtNDY1Mi05MjY2LTA4YWI4MjMzZjg4MCIsImlzUmVnaXN0ZXJlZCI6ZmFsc2V9.NsuoKFnd9TsiJwVFpkwBg5HdwFlxACU8bXi-uPKUhZs'

def getAuth():
    headers = {
    'Host': 'api.cian.ru'
    ,'os': 'android'
    ,'buildnumber': '2.129.1'
    ,'versioncode': '21271300'
    ,'device': 'Phone'
    ,'applicationid': 'ac6e86c0-2861-4dd1-95f7-18f40bf8e107'
    ,'package': 'ru.cian.main'
    ,'user-agent': 'Cian/2.129.1 (Android; 21291300; Phone; PRO 7-S; 24; ac6e86c0-2861-4dd1-95f7-18f40bf8e107)'
    ,'content-length': 0
    ,'accept-encoding': 'utf-8'
    }
    URL = "api.cian.ru"
    con = http.client.HTTPConnection(URL)
    con.request("POST", "/1.4/ios/get-session-anonymous" , body = '', headers = headers)
    response = con.getresponse()
    print(response.status, response.reason)
    if response.status == 200:
        sid = json.loads(response.read().decode('utf-8'))['data']['sid']
        print(sid)
        return sid
    else:
        handle = open("logs.txt", "a")
        handle.write(str(datetime.datetime.now())+'  Something wrong with CIAN_AUTH\n')
        print(str(datetime.datetime.now())+'    Something wrong with CIAN_AUTH\n')
        handle.close() 
        return ''
    


#??? ????!!!!!!!!!!!!!!!!!!!!!!!!!!!!_----------------------------------------------------------------------------------------------
def cian_request():
    time = datetime.datetime.now()
    query = u"""{"query":{"_type":"flatrent","sort":{"type":"term","value":"price_object_order"},"is_by_homeowner":{"type":"term","value":true},"foot_min":{"type":"range","value":{"lte":"15"}},"only_foot":{"type":"term","value":"2"},"for_day":{"type":"term","value":"!1"},"with_neighbors":{"type":"term","value":false},"region":{"type":"terms","value":[-2]},"room":{"type":"terms","value":[1,2,3,4,9]},"object_type":{"type":"terms","value":[0]},"building_status":{"type":"term","value":0},"engine_version":{"type":"term","value":"2"},"page":{"type":"term","value":1},"limit":{"type":"term","value":20},"price":{"type":"range","value":{"lte":40000}},"commission_type":{"type":"term","value":0},"zalog":{"type":"term","value":false}}}"""
    headers = {
    'Host': 'api.cian.ru'
    ,'authorization':'simple ' + getAuth()
    ,'os': 'android'
    ,'buildnumber': '2.129.1'
    ,'versioncode': '21271300'
    ,'device': 'Phone'
    ,'applicationid': 'ac6e86c0-2861-4dd1-95f7-18f40bf8e107'
    ,'package': 'ru.cian.main'
    ,'user-agent': 'Cian/2.129.1 (Android; 21291300; Phone; PRO 7-S; 24; ac6e86c0-2861-4dd1-95f7-18f40bf8e107)'
    ,'content-type': 'application/json; charset=UTF-8'
    ,'content-length': len(query)
    ,'accept-encoding': 'utf-8'
    }
    URL = "api.cian.ru"
    con = http.client.HTTPConnection(URL)
    con.request("POST", "/search-offers/v4/search-offers-mobile-apps/" , body = query, headers = headers)
    response = con.getresponse()
    print(response.status, response.reason)
    if response.status == 200:
        cian_object = response.read().decode('utf-8')
        handle = open("response.json", "w", encoding="utf-8")
        handle.write(cian_object)
        handle.close()
    else:
        handle = open("logs.txt", "a")
        handle.write(str(datetime.datetime.now())+'  Something wrong with CIAN\n')
        print(str(datetime.datetime.now())+'    Something wrong with CIAN\n')
        handle.close()  
    #print(cian_object)
    #r = requests.post(url = URL, headers = headers, params = query)
    #print(r.text)
    con.close()




#??? ???!!!!!!!!!!!!!!!!!!!!!!!!!!!!!_----------------------------------------------------------------------------------------------



def trip_request():
    time = datetime.datetime.now()
    headers = {
    'Host': 'ru.trip.com',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:75.0) Gecko/20100101 Firefox/75.0',
    'Accept': 'application/json',
    'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3',
    'Accept-Encoding': 'gzip, deflate, br',
    'P': '32713300349',
    'Content-Type': 'application/json;charset=UTF-8',
    'Content-Length': '2338',
    'Origin': 'https://ru.trip.com',
    'Connection': 'keep-alive',
    'Referer': 'https://ru.trip.com/hotels/list?city=798&countryId=30&checkin=2020/03/16&checkout=2020/03/22&optionId=798&optionType=IntlCity&display=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%2C%20%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%2C%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F&crn=2&adult=2&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0&highPrice=-1&barCurr=RUB&showtotalamt=2&sort=price0',
    'Cookie': 'ibu_h5_site=RU; ibu_h5_group=trip; ibu_h5_local=ru-ru; ibu_h5_lang=ru; ibu_h5_curr=RUB; IBU_TRANCE_LOG_P=11835450053; IBU_TRANCE_LOG_URL=/m/hotels/list?cityId=366&checkIn=2020/03/10&checkOut=2020/03/11&adult=1&crn=1&optionid=366&optiontype=IntlCity; librauuid=abFpOcg1Uu3TGk3uLH; hoteluuid=Fp6oubfa7DBG2cq5; _bfa=1.1583843634996.1tjac4n.1.1583843634996.1583843644940.1.2.10320668590; _gcl_au=1.1.1866587029.1583843635; _ga=GA1.2.1678331854.1583843638; _gid=GA1.2.176504266.1583843638; _gat=1; _ym_uid=1583843638600848322; _ym_d=1583843638; _ym_visorc_48015557=w; _ym_isad=2; _fbp=fb.1.1583843638300.637865781',
    'TE': 'Trailers'
    }
    checkin1 = str((datetime.datetime.now() + datetime.timedelta(days=5,hours=0, minutes=0)).strftime("%Y-%m-%d"))
    checkout1 = str((datetime.datetime.now() + datetime.timedelta(days=12,hours=0, minutes=0)).strftime("%Y-%m-%d"))
    checkin2 = str((datetime.datetime.now() + datetime.timedelta(days=5,hours=0, minutes=0)).strftime("%Y/%m/%d"))
    checkout2 = str((datetime.datetime.now() + datetime.timedelta(days=12,hours=0, minutes=0)).strftime("%Y/%m/%d"))
    checkin3 = str((datetime.datetime.now() + datetime.timedelta(days=5,hours=0, minutes=0)).strftime("%Y-%m-%d"))
    checkout3 = str((datetime.datetime.now() + datetime.timedelta(days=12,hours=0, minutes=0)).strftime("%Y-%m-%d"))
    query = '{"meta":{"fgt":"","hotelId":"","priceToleranceData":"","priceToleranceDataValidationCode":"","mpRoom":[],"hotelUniqueKey":"","shoppingid":""},"seqid":"","deduplication":[],"filterCondition":{"star":[],"rate":"","priceRange":{"lowPrice":0,"highPrice":-1},"priceType":2,"breakfast":[],"payType":[],"bedType":[],"bookPolicy":[],"bookable":[],"discount":[],"zone":[],"landmark":[],"metro":[],"airportTrainstation":[],"location":[],"cityId":[],"amenty":[],"category":[],"feature":[],"brand":[],"popularFilters":[]},"searchCondition":{"sortType":"price0","adult":2,"child":0,"age":"","pageNo":1,"optionType":"IntlCity","optionId":"798","lat":0,"destination":"","keyword":"","cityName":"Санкт-Петербург","lng":0,"cityId":798,"checkIn":"' + checkin1 + '","checkOut":"' + checkout1 + '","roomNum":2,"mapType":"gg","travelPurpose":0,"countryId":30,"url":"https://ru.trip.com/hotels/list?city=798&countryId=30&checkin=' + checkin2 + '&checkout=' + checkout2 + '&optionId=798&optionType=IntlCity&display=%D0%A1%D0%B0%D0%BD%D0%BA%D1%82-%D0%9F%D0%B5%D1%82%D0%B5%D1%80%D0%B1%D1%83%D1%80%D0%B3%2C%20%D0%9B%D0%B5%D0%BD%D0%B8%D0%BD%D0%B3%D1%80%D0%B0%D0%B4%D1%81%D0%BA%D0%B0%D1%8F%20%D0%BE%D0%B1%D0%BB%D0%B0%D1%81%D1%82%D1%8C%2C%20%D0%A0%D0%BE%D1%81%D1%81%D0%B8%D1%8F&crn=2&adult=2&children=0&searchBoxArg=t&travelPurpose=0&ctm_ref=ix_sb_dl&domestic=0&highPrice=-1&barCurr=RUB&showtotalamt=2&sort=price0","pageSize":20,"timeOffset":10800,"radius":0},"queryTag":"NORMAL","genk":true,"genKeyParam":"a=0,b=' + checkin3 + ',c=' + checkout3 + ',d=ru-ru,e=2","webpSupport":false,"platform":"online","pageID":"10320668148","head":{"Version":"","userRegion":"RU","Locale":"ru-RU","LocaleController":"ru-RU","TimeZone":"3","Currency":"RUB","PageId":"10320668148","webpSupport":false,"userIP":"","P":"32713300349","ticket":"","clientID":"1583843634996.1tjac4n","Union":{"AllianceID":"","SID":"","Ouid":""},"HotelExtension":{"hasAidInUrl":false,"Qid":"150676971968","hotelUuidKey":"puHRA6j51YghwfprnJPfJlmwHJ0GYNpWqhi4bILJ50WuDR95KqpiDJXGRn9RG5rmViUJ9FJdaRCpRzgimJLsvB6KsurF5iqmvQgYSUJ4qxQ7rOJMpeQ3JBQrNuiUNv09xP6Jq1i6GrUJOJApvuLYOFJHOjFzJqJzfvFlJ1lyLSw8GiA8RPAYqlvFTYLCi5mrVJCJMUYzBrMHjPmj0Qi7JUaWVLwozr16wLbyh3yGTWMdyFJ7DWgFyPpi5HjqCvh8WFfvuORHMwp5J49WPbWDZiQJ7owQhyzQr9BwVFWXuR3bxaBWBprhZvo0jB3ROaiNBEGDjNPv17eZCvVJ6hW9hyFHiHdjahiZVw6mjslRo6j9Hw3nvTdvPf","hotelUuid":"abFpOcg1Uu3TGk3uLH"}}}'
    URL = "https://ru.trip.com/restapi/soa2/16709/json/HotelSearch"
    #print(query)
    response = requests.post(URL,query.encode('utf-8'),headers)
    response.encoding = 'utf-8' 
    #print(response.json())
    if response.status_code  == 200:
        handle = open("response_trip.json", "w", encoding="utf-8")
        handle.write(response.text)
        handle.close()
    else:
        handle = open("logs.txt", "a")
        handle.write(str(datetime.datetime.now())+'   Something with TRIP\n')
        print(str(datetime.datetime.now())+'  Something with TRIP\n')
        handle.close()  





#???--------------------------------------------------------------####################################################################

@app.route('/', methods=['GET'])
def getrooms():
    #file = open("response.json", "r")
    # read ALL the lines!
    cian_request()
    if (datetime.datetime.now() - time) > datetime.timedelta(hours=1, minutes=0):
        cian_request()
    return send_file("response.json", mimetype='application/json')
    #file.close()

@app.route('/hotels', methods=['GET'])
def gethotels():
    #file = open("response_trip.json", "r")
    # read ALL the lines!
    trip_request()
    if (datetime.datetime.now() - time) > datetime.timedelta(hours=2, minutes=0):
        trip_request()
    return send_file("response_trip.json", mimetype='application/json')
    #file.close()

if __name__ == '__main__':
    app.run(debug=True)