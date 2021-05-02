from datetime import datetime
import requests

'''

botenv\Scripts\activate  

'''

def sample_responses(input_text):
    user_message = str(input_text).lower()

    if user_message in ("hello","hi","sup"):
        return "Hey there!"


def send_dog_pic(text):
    contents = requests.get('https://random.dog/woof.json').json()
    image_url = contents['url']
    return image_url