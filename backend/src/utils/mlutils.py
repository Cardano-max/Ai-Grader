import requests

ML_API = "https://mlgrader-api-debffbr7ta-uc.a.run.app/"
def process_image(url):
    resp = requests.post(f"{ML_API}api/v1/predict", json={"url" : url})
    if resp.status_code == 200:
        return resp.json()