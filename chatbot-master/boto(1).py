"""
This is the template server side for ChatBot
"""
import random
import requests
import bottle
from bottle import route, run, template, static_file, request
import json

bottle.TEMPLATE_PATH.insert(0, '')
count = 0


def hello(name):
    global count
    count += 1
    user_name = name.split()
    return "hi {0}, nice to meet you".format(user_name[-1])


def swear_words(msg):
    return "Oh Please !! Don't say {0} i don't like when you speak like that".format(msg)


def question():
    return "Good question! i'll think about it"


def good_bye():
    return "Bye-bye my friend !!! I'll miss you"


def joke():
    link = 'http://api.icndb.com/jokes/random?firstName=John&amp;lastName=Doe'
    data = requests.get(link).text
    data = json.loads(data)
    value = data['value']
    return value["joke"]


def weather():
    link = "https://samples.openweathermap.org/data/2.5/weather?lat=35&lon=139&appid=b6907d289e10d714a6e88b30761fae22"
    data = requests.get(link).text
    data = json.loads(data)
    main = data["main"]
    temp = main["temp"]
    pressure = main["pressure"]
    humidity = main["humidity"]
    return "Actually, the temperature is {0} the pressure is {1} and the humidity is {2}.".format(temp, pressure,
                                                                                                  humidity)


def teacher(name):
    user_name = name.split()
    return "Hi {0}, you are super cool and you will give me a DONE.".format(user_name[-1])


def emotion(elem):
    user_emotions = elem.split()
    for word in user_emotions:
        if word in emotions:
            return "i'm feeling so {0}".format(word)
        else:
            return "i'm  sorry ! My english is so comme-ci comme-ca. what did you mean?!"


emotions = ["afraid", "bored", "confused", "crying", "dancing", "dog", "excited", "giggling", "heartbroke", "inlove",
            "laughing", "money", "no", "ok", "takeoff", "waiting"]
swear = ['fuck', 'asshole', 'bitch', 'dump', 'shit']
my_quest = ["?", "what", "which", "where", "how", "why"]
bye = ['bye', 'goodbye', 'by', 'bye-bye', 'au revoir']
make_joke = ["laugh", "joke", "farce", "gag", "humor", "parody", "jokes", "laughing"]
weather_words = ["temperature", "temp", "weather", "humidity", "climat"]
hello_list = ["my name is", "i'm", "my name", "call me"]
others = ["Good", "Interesting!", "Ok my friend", "Ok fine:)", "Okay;)", "If you want ask me a question",
          "If you want call me Boto"]


def principal(msg):
    global count
    if count == 0:
        return hello(msg)
    if any(x in msg for x in hello_list):
        return hello(msg)
    if any(x in msg for x in my_quest):
        return question()
    if any(x in msg for x in swear):
        return swear_words(msg)
    if any(x in msg for x in bye):
        return good_bye()
    if any(x in msg for x in make_joke):
        return joke()
    if any(x in msg for x in emotions):
        return emotion(msg)
    if "ariel" in msg:
        return teacher(msg)
    if "yoav" in msg:
        return teacher(msg)
    if "yifftach" in msg:
        return teacher(msg)
    if any(x in msg for x in weather_words):
        return weather()
    if msg == "boto":
        return "Yes honey , it's me"
    else:
        return random.choice(others)


@route('/', method='GET')
def index():
    return template("chatbot.html")


@route("/chat", method='POST')
def chat():
    user_message = request.POST.get('msg').lower()
    if any(x in user_message for x in my_quest):
        return json.dumps({"animation": "confused", "msg": principal(user_message)})
    if any(x in user_message for x in swear):
        return json.dumps({"animation": "crying", "msg": principal(user_message)})
    if any(x in user_message for x in bye):
        return json.dumps({"animation": "heartbroke", "msg": principal(user_message)})
    if any(x in user_message for x in make_joke):
        return json.dumps({"animation": "giggling", "msg": principal(user_message)})
    user_emotions = user_message.split()
    for word in user_emotions:
        if word in emotions:
            return json.dumps({"animation": word, "msg": principal(user_message)})
    return json.dumps({"animation": "inlove", "msg": principal(user_message)})


@route("/test", method='POST')
def chat():
    user_message = request.POST.get('msg')
    return json.dumps({"animation": "inlove", "msg": user_message})


@route('/js/<filename:re:.*\.js>', method='GET')
def javascripts(filename):
    return static_file(filename, root='js')


@route('/css/<filename:re:.*\.css>', method='GET')
def stylesheets(filename):
    return static_file(filename, root='css')


@route('/images/<filename:re:.*\.(jpg|png|gif|ico)>', method='GET')
def images(filename):
    return static_file(filename, root='images')


def main():
    run(host='localhost', port=7000)


if __name__ == '__main__':
    main()
