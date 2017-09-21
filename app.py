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

    result = urlopen("https://api.telegram.org/bot" + bot_id + "/sendMessage", 
                     urlencode({ "chat_id": -242861658, 
                     "text": json.dumps(req.get('result').get('parameters'), 
                                        indent=4, ensure_ascii=False) }).encode("utf-8")).read()

    res = makeWebhookResult(req)

    res = json.dumps(res, indent=4)
    print(res)
        
    r = make_response(res)
    r.headers['Content-Type'] = 'application/json'
    return r

def makeWebhookResult(req):
    if req.get("result").get("action") != "request":
        return {}
    result       = req.get("result")
    parameters   = result.get("parameters")
    accomodation = parameters.get("accomodation")
    when         = parameters.get("when")
    duration     = parameters.get("duration")
    
    speech = ''
    #speech = 'И сколько же нас поедет (не считая меня) ?'
    
    contextOut = []
    enter = 0
    
    if not(len(accomodation)):
        enter=1
        contextOut = [{"name":"no_accomodation",
                       "lifespan":5,
                       "parameters":{}}]
        #speech = 'Например: сколько людей поедет.'
        

    if not(len(when)):
        enter=1
        contextOut = [{"name":"no_when",
                       "lifespan":5,
                       "parameters":{}}]
        #speech = 'Например: когда вы хотите отправиться.'
        

    if not(len(duration)):
        enter=1
        contextOut = [{"name":"no_duration",
                       "lifespan":5,
                       "parameters":{}}]
        #speech = 'Например: сколько вы хотите провести ночей'
        

    if not(len(when)) and not(len(accomodation)):
        enter=1
        contextOut = [{"name":"no_accomodation",
                       "lifespan":5,
                       "parameters":{}},
                      {"name":"no_when",
                       "lifespan":5,
                       "parameters":{}}]
        #speech = 'Например сколько людей поедет, или когда'
        

    if not(len(duration)) and not(len(when)):
        enter=1
        contextOut = [{"name":"no_duration",
                       "lifespan":5,
                       "parameters":{}},
                      {"name":"no_when",
                       "lifespan":5,
                       "parameters":{}}]
        #speech = 'Например сколько людей поедет и на сколько'
        

    if not(len(accomodation)) and not(len(duration)):
        enter=1
        contextOut = [{"name":"no_accomodation",
                       "lifespan":5,
                       "parameters":{}},
                      {"name":"no_duration",
                       "lifespan":5,
                       "parameters":{}}]
        #speech = 'Например сколько людей поедет и на сколько'
        
    if not(len(accomodation)) and not(len(duration)) and not(len(when)):
        enter=1
        contextOut = [{"name":"no_accomodation",
                       "lifespan":5,
                       "parameters":{}},
                      {"name":"no_duration",
                       "lifespan":5,
                       "parameters":{}},
                      {"name":"no_when",
                       "lifespan":5,
                       "parameters":{}}]
        #speech = 'Например сколько людей поедет и на сколько'
    if enter==1:
        return {
            "speech": speech,
            "displayText": speech,
            #"data": {},
            "contextOut": contextOut,
            "source": "agent" #apiai-onlinestore-shipping",
        }

    #speech = "The cost of shipping to " + zone + " is " + str(cost[zone]) + " euros."

    #print("Response:")
    #print(speech)


if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))

    print ("Starting app on port %d" % port)

    app.run(debug=True, port=port, host='0.0.0.0')
