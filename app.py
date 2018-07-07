from flask import Flask
from flask_ask import Ask, statement, question, session, delegate

import json
import requests
import time
import unidecode


app = Flask(__name__)
ask = Ask(app, '/')


def get_dialog_state():
    return session['dialogState']

@ask.launch
def start_alexa():
    welcome_message = 'Hello there, would you like to have some news updates?'
    return question(welcome_message)



@ask.intent("yesIntent")
def share_headlines(news_type):
    dialog_state = get_dialog_state()
    if dialog_state != 'COMPLETED':
        return delegate()

    if news_type is not "None":
        headlines = get_headlines(news_type)
        headline_msg = 'The current news headlines are {}'.format(headlines)
        return statement(headline_msg)
    else:
        no_intent()

def get_headlines(type_of_news):
    user_pass_dict = {'user': 'USERNAME',
                      'passwd': 'PASSWORD',
                      'api_type': 'json'}
    sess = requests.session()
    sess.headers.update({'User-Agent': 'Testing Alexa: Vinay'})
    sess.post('https://wwww.reddit.com/api/login', data=user_pass_dict)
    time.sleep(1)
    url = 'https://reddit.com/r/' + type_of_news + '/.json?limit=2'
    html = sess.get(url)
    data = json.loads(html.content.decode('utf-8'))
    titles = []
    for listing in data['data']['children']:
        titles.append(unidecode.unidecode(listing['data']['title']))
    titles = '... '.join([i for i in titles])
    return titles



@ask.intent("noIntent")
def no_intent():
    bye_text = 'get the hell out of my way then...bye'
    return statement(bye_text)



if __name__ == '__main__':
    app.run(debug=True)
