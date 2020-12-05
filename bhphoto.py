from urllib import request
import json
import os
import smtplib

values = b'{"params":{"itemList":[{"skuNo":1595780,"itemSource":"REG"}],"channels":["priceInfo"],"channelParams":{"priceInfo":{"PRICING_CONTEXT":"DETAILS_CART_LAYER"}}}}'

headers = {
    "Authority": "www.bhphotovideo.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
    "Content-Type": "application/json;charset=UTF-8",
    "X-Csrf-Token": "53cb7bf2966e02adaee00c68fcf5660f",
    "Accept": "application/json, text/plain, */*"

}

link = "https://www.bhphotovideo.com/c/product/1595780-REG/pny_technologies_vcg308010tfxmpb_geforce_rtx_3080_10gb.html"

api_url = "https://www.bhphotovideo.com/api/item/p/product-details?from=cli&aperture=1&cliReqId=a41c1e91-9ef2c6-a409-2105d52f7b22-cli-7"

req = request.Request(api_url, values, headers)
recpt = "bfemiano@fastmail.com"
with request.urlopen(req) as response:
    data_back = json.loads(response.read())
    for item in data_back['data']:
        can_add_to_cart = item['priceInfo']['addToCartButton']
        name = item['core']['shortDescription']
        if can_add_to_cart != 'NONE' and not os.path.exists("/Users/bfemiano/bhphoto_email.sent"):
            gmail_server = 'smtp.gmail.com'
            username = 'bfemiano@gmail.com'
            password = "REPLACE WITH REAL APP PASSWORD"
            server = smtplib.SMTP(gmail_server, 587)
            server.starttls()
            server.login(username,password)

            msg = """From: bfemiano@gmail.com\nTo: {recpt}\nSubject: BH Photo might have your item in stock!\n

                {name}\n\n{url}

            """.format(recpt=recpt, url=link, name=name)

            server.sendmail(username, recpt, msg)
            with open("/Users/bfemiano/bhphoto_email.sent", 'w') as foo:
                pass