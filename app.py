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

    result = urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", urlencode({ "chat_id": -242861658, "text": json.dumps(req, indent=4, ensure_ascii=False) }).encode("utf-8")).read()

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
        
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "request":
        return {}
    result = req.get("result")
    parameters = result.get("parameters")
    accomodation = parameters.get("accomodation")
    speech = 'И сколько же нас поедет (не считая меня) ?'
    
    if not (len(accomodation)):
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            "contextOut": [{"name":"no_accomodation", 
                            "lifespan":5, 
                            "parameters":{
                            #    "city":"Rome"
                            }}],
            "source": "agent", #apiai-onlinestore-shipping",
            "followupEvent": {
                  "name": "the_end",
                  "data": {
                  #   "<parameter_name>":"<parameter_value>>"
                  }
            }
        }
    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

    #print("Response:")
    #print(speech)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
