import requests
import json
import gspread
from datetime import datetime
from flask import Flask, request

def restofstuff(cod):

    # Make Strava auth API call with your
    # client_code, client_secret and code
    response = requests.post(
        url = 'https://www.strava.com/oauth/token',
        data = {
                'client_id': INSERTIDHERE,
                'client_secret': 'INSERT SECRET HEAR',
                'code': cod,
                'grant_type': 'authorization_code'
            }
    )

    #Save json response as a variable
    strava_tokens = response.json()

    # Google sheet auth and opening
    # Don't forget to enter the correct path for google api service account credentials
    gc = gspread.service_account(filename='./creds.json')
    sh = gc.open_by_key("YOUR GOOGLE SHEETS FILE KEY").sheet1
    id = None
    token_str = json.dumps(strava_tokens)

    try:
        id = strava_tokens['athlete']['id']
        insetRow = [id, token_str, str(datetime.now())]
        sh.insert_row(insetRow, 2)
    except KeyError:
        print("Couldn't find athlete_id in respose json.")
        print(token_str)


# Server
app = Flask(__name__)
@app.route('/')
def result():
    return "Your server works"

@app.route('/exchange_token')
def login():
    code = request.args.get('code')
    print("code is: "+str(code))
    restofstuff(code)
    return "Thank you."

if __name__ == '__main__':
   app.run(host='0.0.0.0')
