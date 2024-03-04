import json
import requests

def find_url_for_word(sentence, gloss_data):
    sentence = sentence.lower()

    for word in sentence.split():
        for entry in gloss_data:
            if entry["gloss"].lower() == word:
                for instance in entry["instances"]:
                    url = instance["url"]
                    if url.endswith(".mp4") and test_url(url):
                        return url

def test_url(url):
    try:
        response = requests.head(url)
        return response.status_code == 200
    except requests.ConnectionError:
        return False

json_path = '/Users/angelacao/S2S/data/WLASL_v0.3 .json'
with open(json_path, "r") as file:
    gloss_data = json.load(file)

user_input = input("Enter a sentence: ")

for word in user_input.split():
    url = find_url_for_word(word, gloss_data)
    if url:
        print(f"URL for '{word}': {url}")
    else:
        print(f"No working URL found for '{word}'")
