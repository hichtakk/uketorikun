import requests
from slackbot.bot import listen_to

from uketorikun import cvision, sheets
from slackbot_settings import SPREADSHEET_ID


def get_image(token, file):
    if 'thum_1024' in file:
        url = file['thum_1024']
    else:
        url = file['url_private']
    header = {'Authorization': 'Bearer {}'.format(token)}
    response = requests.get(url, headers=header, allow_redirects=True)
    print("Downloading image: " + url)
    if response.status_code != 200:
        e = Exception("HTTP status: " + str(response.status_code))
        raise e
    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("invalid content type: " + content_type)
        raise e

    return response.content


@listen_to('(.*)')
def listen(message, params):
    if 'files' in message.body:
        for file in message.body['files']:
            if file['filetype'] in ('png', 'jpg', 'jpeg'):
                check_image(message._client.token, file, message)


def check_image(token, file, message):
    print('image file found in message')
    image = get_image(token, file)

    print('start scaning image')
    result = cvision.ocr_image(image)
    print('scanning completed')
    print('========')
    print(result)
    print('========')

    print('start finding addressee')
    addressee = cvision.find_addressee(result)
    print(addressee)

    print('start finding addressee')
    deliverer = cvision.find_deliverer(result)
    print(deliverer)

    print('write package information to sheet')
    try:
        sheets.write_package_info(message.body['user_profile']['real_name'], addressee['name'], deliverer['name'], file['url_private'])
    except Exception as e:
        raise e

    msg = """
```
TO: {addressee} ({ratio}% probability)
DELIVERER: {deliverer}
```
Please refer to tracking sheet:
https://docs.google.com/spreadsheets/d/{sheet}
    """
    print('Done. Report message to slack.')
    print(msg.format(addressee=addressee['name'],
                            ratio=addressee['ratio']*100,
                            deliverer=deliverer['name'],
                            sheet=SPREADSHEET_ID))
    message.send(msg.format(addressee=addressee['name'],
                            ratio=addressee['ratio']*100,
                            deliverer=deliverer['name'],
                            sheet=SPREADSHEET_ID))
