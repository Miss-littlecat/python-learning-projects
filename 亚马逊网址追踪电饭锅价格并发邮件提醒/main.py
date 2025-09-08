from bs4 import BeautifulSoup
import requests
import smtplib
import os
from dotenv import load_dotenv

load_dotenv()
target_price = 100


headers = {
    "Accept-Language":"zh-CN,zh;q=0.9,en;q=0.8",
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36"
}
url="https://appbrewery.github.io/instant_pot/"
#live_url="https://www.amazon.com/dp/B075CYMYK6?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1"
response = requests.get(url=url,headers=headers)
soup = BeautifulSoup(response.text, 'html.parser')
print(soup.prettify()[:2000])
price = soup.select_one("span.a-price span.a-offscreen") #soup.find(name='span', class_='aok-offscreen').get_text()
pure_num_price = price.split('$')[1]

price = float(pure_num_price)

def send_email():
    with smtplib.SMTP_SSL('smtp.qq.com', 465) as smtp:
        smtp.ehlo()
        email_address = os.environ.get('my_email')
        password = os.environ.get('password')
        smtp.login(email_address, password)

        subject = "Come on and buy instant pot!"
        body = f"Instant Pot Duo Plus 9-in-1 Electric Pressure Cooker has been {price} dollars now."

        msg = f"Subject: {subject}\nFrom: {email_address}\nTo: {email_address}\n\n{body}"

        #sent email
        smtp.sendmail(email_address, email_address, msg=msg.encode('utf-8'))
        print("Email sent!")
        smtp.quit()


if price < target_price:
    send_email()



