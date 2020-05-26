# -*- coding:utf-8 -*-

from flask import jsonify, request
from . import api

#### 네이버 API 사용을 위함
import urllib.request
import requests
from json import loads, dumps


headers = {
            "X-Naver-Client-Id":"3bbuD4tYpcecdPgNgzvo",
            "X-Naver-Client-Secret":"P6av4Cked0"
        }

@api.route('/search', methods=['GET'])
def test():
    '''
    이미지 검색 정렬 옵션 : sim(유사도순), date(날짜)
    '''
    keyword = request.args.get('keyword', None)
    start = request.args.get('start', 1)
    print(start)
    url = "https://openapi.naver.com/v1/search/image"
    query = "?query=" + urllib.parse.quote(keyword)
    option = "&sort=sim&display=30&start={start}".format(start=start)
    url_query = url + query + option
    response = requests.get(url_query, headers=headers)
    rescode = response.status_code
    print(response.text)
    if (rescode == 200):
        return jsonify(loads(response.text))
    else:
        return {"Error Code": rescode}








