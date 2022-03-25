import requests

url = 'https://ipinfo.io'
username = 'mgcoder5'
password = 'OnceMoretry!27'

proxy = f'http://{username}:{password}@gate.smartproxy.com:10009'
  
response = requests.get(url, proxies={'http': proxy, 'https': proxy})

print(response.text)
