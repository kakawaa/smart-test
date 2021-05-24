import os
import datetime,time
import requests
import json
import urllib.parse


def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

def getTopost(url):
    r = requests.get(str(url).strip(),verify=False)
    return r.text

def get_file_name_list(file_dir):
    '''
    :brief:获取文件夹下内，所有文件
    :param file_dir:文件夹目录
    :return: 文件列表
    '''
    for root,dirs,files in os.walk(file_dir):
        return files

def getDatesByTimes(sDateStr, eDateStr):
    '''
    获取区间日期
    '''
    list = []
    datestart = datetime.datetime.strptime(sDateStr, '%Y-%m-%d')
    dateend = datetime.datetime.strptime(eDateStr, '%Y-%m-%d')
    list.append(datestart.strftime('%Y-%m-%d'))
    while datestart < dateend:
        datestart += datetime.timedelta(days=1)
        list.append(datestart.strftime('%Y-%m-%d'))
    return list


def getTojson(data):
    datalist = str(data).split('&')
    request_data_list=[]
    i= 0
    while len(datalist)>i:
        datalist_value = datalist[i].split('=')
        request_data_list.append(datalist_value)
        i=i+1
    return str(dict(request_data_list))

def jsonToget(data):
    jsondata = json.loads(data)
    key_list = list(jsondata.keys())
    value_list = list(jsondata.values())
    k=0
    h = 0
    request_data = ''
    request_data_list = []
    while len(key_list)>k:
        r_data = key_list[k]+"="+value_list[k]
        request_data_list.append(r_data)
        k = k+1
    while len(request_data_list)>h:
        if(h==len(request_data_list)-1):
            request_data = request_data + request_data_list[h]
        else:
            request_data = request_data+request_data_list[h]+"&"
        h = h+1
    datalist = request_data.split('&')
    urlencode_jsondata=''
    i= 0
    while len(datalist)>i:
        if i == len(datalist)-1:
            if len(datalist[i].split("="))==2:
                urlencode = datalist[i].split("=")[0] + "=" + urllib.parse.quote(datalist[i].split("=")[1])+"&"
            else:
                j = 2
                moredata = "="
                while  len(datalist[i].split("="))>j+1:
                    moredata = datalist[i].split("=")[j]+"="
                    j = j+1
                urlencode = datalist[i].split("=")[0] + "=" + urllib.parse.quote(datalist[i].split("=")[1]) +moredata+ "&"
            urlencode_jsondata= urlencode_jsondata+urlencode.replace("&","")
        else:
            if len(datalist[i].split("="))==2:
                urlencode = datalist[i].split("=")[0] + "=" + urllib.parse.quote(datalist[i].split("=")[1])+"&"
            else:
                j = 2
                moredata = "="
                while  len(datalist[i].split("="))>j+1:
                    moredata = datalist[i].split("=")[j]+"="
                    j = j+1
                urlencode = datalist[i].split("=")[0] + "=" + urllib.parse.quote(datalist[i].split("=")[1]) +moredata+ "&"
            urlencode_jsondata = urlencode_jsondata + urlencode
        i = i+1
    return urlencode_jsondata

def GetResponse(request,url,name):
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0',
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", url, data=jsonToget(request), headers=headers, timeout=60)
    if name == 'code':
        code = str(response.status_code)
        print("code:"+code)
        return code
    else:
        return response.text


def Equal(name,a,b,error_list):
    try:
        if a == b:
            return 'false'
        else:
            errorinfo = {
                "name": name,
                "type": "Equal",
                "wrong": a,
                "right": b
            }
            error_list.append(errorinfo)
            return 'true'
    except:
        errorinfo = {
            "name": name,
            "type": "Not existed"
        }
        error_list.append(errorinfo)
        return 'true'

def LengthCheck(name,a,error_list):
    try:
        if a > 0:
            pass
        else:
            errorinfo = {
                "name": name,
                "type": "LengthCheck",
                "wrong": a
            }
            error_list.append(errorinfo)
    except:
        errorinfo = {
            "name": name,
            "type": "Not existed"
        }
        error_list.append(errorinfo)

def dingding_robot(data):
    dingding_robot_token = "https://oapi.dingtalk.com/robot/send?access_token=7eb8bd14b0647f3d57f3b6a74dc5e734cfffe77d8b6c4a245b6b880f3c5f5c3b"
    headers = {'content-type': 'application/json'}
    r = requests.post(dingding_robot_token, headers=headers, data=json.dumps(data))
    r.encoding = 'utf-8'
    print(r.text)
    return (r.text)


def decode(data):
    '''
    v2解密
    '''
    data = str(data).strip().replace(" ", "+")
    cmd = "java -jar HilloDataDecode.jar " + data
    r = os.popen(cmd)
    text = r.read()
    r.close()
    decode_data = text.replace('============ decode result ============', '').strip()
    return decode_data


def vdm_decode(data):
    '''
    v1解密
    '''
    data = str(data).strip().replace(" ", "+")
    headers = {
        'User-Agent': 'User-Agent:Mozilla/5.0',
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache"
    }
    response = requests.request("POST", "http://14.23.91.210:5907/coder/vdm_decrypt", data="data="+data, headers=headers, timeout=30)
    decode_data = json.loads(response.text)
    return decode_data
