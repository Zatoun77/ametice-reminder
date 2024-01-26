from dotenv import load_dotenv
import os
import requests
import re
import json

LOGIN_AMU_URL_GET = "https://ident.univ-amu.fr/cas/login?service=https://ametice.univ-amu.fr/login/index.php?authCAS=CAS"
LOGIN_AMU_URL_POST = "https://ident.univ-amu.fr/cas/login"

HOME_AMU_URL = "https://ametice.univ-amu.fr/my/"

CALENDAR_AMU_URL_POST = "https://ametice.univ-amu.fr/lib/ajax/service.php?sesskey={}&info=core_calendar_get_action_events_by_timesort"

calendar_json = {"headers": {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7,de;q=0.6",
    "cache-control": "no-cache",
    "content-type": "application/json",
    "pragma": "no-cache",
    "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"macOS\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest"
},
    "body": "[{\"index\":0,\"methodname\":\"core_calendar_get_action_events_by_timesort\",\"args\":{\"limitnum\":11,\"timesortfrom\":1704063600,\"limittononsuspendedevents\":true}}]",
}


def connect(username, password):
    global session, login_data, calendar_json
    session = requests.Session()
    login_data = {
        "username": username,
        "password": password,
        "execution": "",
        "_eventId": "submit",
        "geolocation": "",
    }

    login_data["execution"] = get_value_from_html(
        "execution", session.get(LOGIN_AMU_URL_GET).text)
    session.post(LOGIN_AMU_URL_POST, data=login_data)


# def disconnect():
#     session.get(LOGOUT_AMU_URL.format(get_sessionkey()))
#     session.cookies.clear()
#     print("Disconnected")
#     return if_connected()


def get_value_from_html(name, html):
    return re.search('name="{}" value="(.*?)"'.format(name), html).group(1)


def get_sessionkey():
    return get_value_from_html("sesskey", session.get(HOME_AMU_URL).text)


def getTasks():
    return session.post(CALENDAR_AMU_URL_POST.format(get_sessionkey()), headers=calendar_json["headers"], data=calendar_json["body"]).json()


def jsonToFile(dict):
    with open('tasks_data.json', 'w') as outfile:
        json.dump(dict, outfile)


if __name__ == '__main__':

    load_dotenv()
    username = os.getenv('USERNAME')
    password = os.getenv('PASSWORD')

    connect(username, password)
    jsonToFile(getTasks()[0])
