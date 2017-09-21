#!/usr/bin/env python

import urllib
import json
import os

from flask import Flask
from flask import request
from flask import make_response

from urllib.parse import urlencode
from urllib.request import urlopen


# Flask app should start in global layout
app = Flask(__name__)

bot_id = "438707605:AAEJceFWg-q8dGsTcZJrXCojCTL8gKN_VUI"

@app.route('/webhook', methods=['POST'])
def webhook():
    req = request.get_json(silent=True, force=True)

    print("Request:")
    print(json.dumps(req, indent=4))
   
    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
    
    result = urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urlencode({ "chat_id": 383189785, "text": res }).encode("utf-8")).read()
    
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "shipping.cost":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    zone = parameters.get("shipping-zone")

    cost = {'Europe':100, 'North America':200, 'South America':300, 'Asia':400, 'Africa':500}

    speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

    print("Response:")
    print(speech)

    return {
        "speech": speech,
        "displayText": speech,
        #"data": {},
        # "contextOut": [],
        "source": "apiai-onlinestore-shipping"
    }


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
