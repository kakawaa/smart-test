#!/usr/bin/env python
"""Script Demo 支持请求动态生成 python3"""

import sys
import os
import time
import requests

def get_response(url,data,timeout=30):
  """接口请求获取返回报文"""
  headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
  response = requests.request("POST", url, data=data, headers=headers, timeout=timeout)
  return response

def make_request(data):
  """必须打印新的请求在终端才能获取"""
  print(data)

if __name__ == '__main__':

  #新接口请求参数依赖其他接口的返回
  #data = 'username=elver&age=18'
  #phone = get_response('http://xxxx/get_user_info',data)['data']['phone']
  new_data = f'user=rafa7'
  #生成用例的请求报文
  make_request(new_data)