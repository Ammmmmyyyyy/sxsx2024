import urllib.request,  sys
import ssl
import json

host = 'https://ali-star-lucky.showapi.com'
path = '/star'
method = 'GET'
appcode = '6685c9f6da73471dba8f2e0e6dc0f27c'
querys = 'needMonth=0&star=baiyang&needWeek=0&needTomorrow=0&needYear=0'
bodys = {}
url = host + path + '?' + querys

request = urllib.request.Request(url)
request.add_header('Authorization', 'APPCODE ' + appcode)
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE
response = urllib.request.urlopen(request, context=ctx)
content = response.read()
if content:
    # 解码字节串为字符串
    decoded_content = content.decode('utf-8')
    # 解析字符串为JSON对象
    json_content = json.loads(decoded_content)
    # 格式化JSON对象为字符串并打印
    formatted_json = json.dumps(json_content, ensure_ascii=False, indent=4)
    print(formatted_json)