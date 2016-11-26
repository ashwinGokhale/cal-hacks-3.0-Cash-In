from flask import Flask, render_template, request, url_for, redirect
import requests
from config import *
import urllib
import os
import json

auth_code = ""
access_token = ""
post_for_token = "https://connect.squareup.com/oauth2/token"
charge_url = "square-commerce-v1://payment/create?"
fee = 0
event_label = ""

app = Flask(__name__)

@app.route("/")
def hello():
    return redirect(url_for("login"))

@app.route("/login")
def login():
    return render_template("index.html")

@app.route("/eventpage")
def eventpage():
    return render_template("eventpage.html")

@app.route("/eventsetup")
def eventsetup():
    # return render_template("eventsetup.html")
    return redirect(url_for("eventsetup"))

@app.route("/finishsetup")
def finishsetup():
    fee = float(request.args.get("fee"))
    event_label = request.args.get("label")
    return redirect(url_for("eventpage"))

@app.route("/charge")
def charge():
    data = "square-commerce-v1://payment/create?data=%7B%22amount_money%22%3A%7B%22amount%22%3A300%2C%22currency_code%22%3A%22USD%22%7D%2C%22callback_url%22%3A%22https%3A%2F%2Fsquare-cash-in.herokuapp.com%2Fcallback%22%2C%22client_id%22%3A%22sq0idp-v_okHMTbPoixXwGyUzYsJA%22%2C%22version%22%3A%221.1%22%2C%22notes%22%3A%22christmasparty%22%2C%22options%22%3A%7B%22supported_tender_types%22%3A%5B%22CREDIT_CARD%22%2C%22CASH%22%5D%7D%2C%22clear_default_fees%22%3A%22TRUE%22%2C%22auto_return%22%3A%22True%22%2C%22skip_receipt%22%3A%22True%22%7D"
    # data = "square-commerce-v1://payment/create?data=%7B%27auto_return%27%3A+True%2C+%27version%27%3A+%271.1%27%2C+%27amount_money%27%3A+%7B%27amount%27%3A+4%2C+%27currency_code%27%3A+%27USD%27%7D%2C+%27client_id%27%3A+%271235oehaoiduh3%27%2C+%27skip_receipt%27%3A+True%2C+%27notes%27%3A+%27halloween+party%27%2C+%27callback_url%27%3A+%27myapp-url-scheme%3A%2F%2Fpayment-complete%27%2C+%27options%27%3A+%7B%27supported_tender_types%27%3A+%5B%27CREDIT_CARD%27%2C+%27CASH%27%5D%7D%2C+%27clear_default_fees%27%3A+True%7D"
    #data = "square-commerce-v1://payment/create?data%3D%257B%2527notes%2527%253A%2B%2527%2527%252C%2B%2527callback_url%2527%253A%2B%2527myapp-url-scheme%253A%252F%252Fpayment-complete%2527%252C%2B%2527skip_receipt%2527%253A%2BTrue%252C%2B%2527clear_default_fees%2527%253A%2BTrue%252C%2B%2527auto_return%2527%253A%2BTrue%252C%2B%2527options%2527%253A%2B%257B%2527supported_tender_types%2527%253A%2B%255B%2527CREDIT_CARD%2527%252C%2B%2527CASH%2527%255D%257D%252C%2B%2527client_id%2527%253A%2B%2527sq0idp-v_okHMTbPoixXwGyUzYsJA%2527%252C%2B%2527version%2527%253A%2B%25271.1%2527%252C%2B%2527amount_money%2527%253A%2B%257B%2527currency_code%2527%253A%2B%2527USD%2527%252C%2B%2527amount%2527%253A%2B0%257D%257D"
    return redirect(data)
    # data = {"data": {"amount_money": {"amount": fee, "currency_code": "USD"},
    #         "callback_url": "myapp-url-scheme://payment-complete",
    #         "client_id": APPLICATION_ID,
    #         "version": "1.1",
    #         "notes": event_label,
    #         "options": {"supported_tender_types": ["CREDIT_CARD","CASH"]},
    #         "clear_default_fees": True,
    #         "auto_return": True,
    #         "skip_receipt": True}}
    # return redirect(charge_url + urllib.quote(urllib.urlencode(data)))
    

@app.route("/callback")
def callback():
    #if getting auth code...
    #auth_code = request.args.get("code")
    if request.args.get("code"):
        auth_code = request.args.get("code")
        payload = {"client_id": APPLICATION_ID, "client_secret": APP_SECRET, "code": auth_code}
        #print("AUTH_CODE: ", auth_code)
        response = requests.post(post_for_token, data=payload)
        #print( "THE RESPONSE IS: ", response.status_code )
        #access_token = json.loads(response.json())["access_token"]
        return render_template("eventsetup.html")
    #if receiving data from a sent transaction...
    elif request.args.get("data"):
        return render_template("eventpage.html")
    
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
