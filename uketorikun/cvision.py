import difflib
import json
import os
import requests
from base64 import b64encode
from os.path import join, basename
from sys import argv
from slackbot_settings import GOOGLE_API_KEY, ENDPOINT_URL
from slackbot_settings import MEMBERS, DELIVERERS


def ocr_image(image_bin):
    req_data = []
    result = ""
    image_context = b64encode(image_bin).decode()
    req_data.append({
        'image': {'content': image_context},
        'features': [{
            'type': 'TEXT_DETECTION',
            'maxResults': 1
        }]
    })
    request_data = {'requests': req_data}
    response = requests.post(ENDPOINT_URL,
                  data=json.dumps(request_data).encode(),
                  params={'key': GOOGLE_API_KEY},
                  headers={'Content-Type': 'application/json'})
    if response.status_code != 200 or response.json().get('error'):
        print('scanning failed')
        return ''
    else:
        for idx, resp in enumerate(response.json()['responses']):
            result = resp['textAnnotations'][0]['description']

    return result


def find_addressee(label_text):
    probability = []
    for name in MEMBERS:
        for line in label_text.upper().split("\n"):
            if line == "":
                continue
            r = difflib.SequenceMatcher(None, name, line).ratio()
            if r == 1.0: # exact match
                return [{'line': line, 'name': name, 'ratio': r}]
            elif r >= 0.5: # ignore line less than 50% match
                probability.append({'line': line, 'name': name, 'ratio': r})
    probability.sort(key=lambda x: x['ratio'])
    probability.reverse()

    if len(probability) > 0:
        return probability[0]
    else:
        return {'name': 'UNKNOWN', 'ratio': 0}


def find_deliverer(label_text):
    probability = []

    for deliverer in DELIVERERS:
        for line in label_text.upper().split("\n"):
            if line == "":
                continue
            r = difflib.SequenceMatcher(None, deliverer, line).ratio()
            if r >= 0.5: # ignore line less than 50% match
                probability.append({'line': line, 'name': deliverer, 'ratio': r})

    probability.sort(key=lambda x: x['ratio'])
    probability.reverse()

    if len(probability) > 0:
        return probability[0]
    else:
        return {'name': 'UNKNOWN', 'ratio': 0}
