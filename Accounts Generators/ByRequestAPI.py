import requests,json
from bs4 import BeautifulSoup
from faker import Faker

from openpyxl import Workbook
wb = Workbook()
ws = wb['Sheet']


def gen_email(username):
    def Check_msg(email,timestemp):
        while True:
            key_pay = {
            "email":email,
            "timestamp":timestemp,
            "server":"server-1",
            "type":"alias"
            }
            r = requests.post('https://smailpro.com/app/key',data=key_pay)
            key = json.loads(r.text)['items']
            url = f"https://public-sonjj.p.rapidapi.com/email/gm/check?key={key}&rapidapi-key=f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081&email={email}&timestamp={timestemp}&server=server-1&type=alias"
            r = requests.get(url)
            items = json.loads(r.text)['items']
            if len(items)>0:
                return items[0]
    def Parse_sms(item):
        payload = {
            "email":item['textTo'],
            "message_id":item['mid'],
            "server":"server-1",
            "type":"alias"
        }
        r = requests.post('https://smailpro.com/app/key',data=payload)
        key = json.loads(r.text)['items']
        url = "https://public-sonjj.p.rapidapi.com/email/gm/read"
        read_payload = {
            "key": key,
            "rapidapi-key": "f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081",
            "email": item['textTo'],
            "message_id": item['mid'],
            "server": "server-1",
            "type": "alias",
        }
        r = requests.get('https://public-sonjj.p.rapidapi.com/email/gm/read',params=read_payload)
        body = json.loads(r.text)['items']['body']
        return body
    def html_parse(source):
        soup = BeautifulSoup(str(source),'html.parser')
        ar = soup.findAll('a')
        for a in ar:
            href = a['href']
            if str(href).find("token")>-1:
                token = str(href).split('token=')[1]
                return token
    key_payload={"username":"random",
    "domain":"gmail.com",
    "server":"server-1",
    "type":"alias"
    }    
    r = requests.post('https://smailpro.com/app/key',data=key_payload)
    if r.status_code == 200:
        key = json.loads(r.text)['items']
        print(key)
        email_params = {
            "key": key,
            "rapidapi-key": "f871a22852mshc3ccc49e34af1e8p126682jsn734696f1f081",
            "username": "random",
            "domain": "gmail.com",
            "server": "server-1",
            "type": "alias",
        }
        r = requests.get('https://public-sonjj.p.rapidapi.com/email/gm/get',params=email_params)
        email = json.loads(r.text)['items']['email']
        time_stemp = json.loads(r.text)['items']['timestamp']
        payload={
        "newsletter": 1,
        "captchaToken": "03AGdBq27x-b9Krfm96uZo56Aaoqj-ckmf_CytoWKMDglIlQP11eUo6XgCerLi-cdMuXiVfCKyZhCkCOyT6ypE5eMJIc6UsQ6uxj77LzAr9ZqIlCT91K2JkMdMV8IEMw36F7JMH7MLdLxERFjfnSM4RH_56Udrum4oHqg4hpJhZrxORBDa5AMHoPEvO_gygLhiRO2VN6Fn-AkaLRDiQFUpZA5PDkcm9IbwafMAUUmnbDi6jigRlOZcXRcog08ScJP6Z1jd3tKOPLJmmIRet3fk5ZkMbfhCQb2tmpgOv2uzJRw5ZAlZ3HB_ug322b74dgVW0ZbuYm8DP2mgwF69zk42qWmD5V7wryOYp--KARW_71sMOalHDmq19sS9SJPPi5iGzZ8k-dOIoYPLdZ5ymGfQ6FZlyjP4kamE7k2RSR35kvRxUVy5ebmLyXKu8-xs3SuqELiluZ_ye0lH",
        "name": "Ahmad Raza",
        "email": email,
        "login": username,
        "password": "Pakistan99"
        }
        r = requests.post('https://stocktwits.com/api/register',data = payload)
        print(r.text)
        if r.status_code==200:
            mainToken = json.loads(r.text)['token']
            header = {
                "authorization":f"OAuth {mainToken}"
            }
            r = requests.get('https://api.stocktwits.com/api/2/account/verify_resend',headers=header)
            print(r.text)
            item = Check_msg(email,time_stemp)
            body = Parse_sms(item) 
            vtoken = html_parse(body)
            token_payload = {"token":f"{vtoken}"}
            r = requests.post('https://api.stocktwits.com/api/2/account/verify_identity.json',headers=header,data=token_payload)
            print(r.text)
            ws.append([username,email,'Pakistan99'])
            wb.save('AccountGenerated.xlsx')

import random
if __name__ =="__main__":
    x = int(input('Generate Accounts: '))
    username = Faker().name().replace(' ', str(random.randint(1,500)))
    for i in range(x):
         gen_email(f"{username}{i}")
