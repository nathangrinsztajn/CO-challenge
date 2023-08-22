import requests

URL = "https://llm4co.fly.dev/"
# URL = "http://llm4co.cxuf9445.odns.fr/"
# URL = "http://127.0.0.1:5000/"


def post_data_to_backend(name, time, performance, function_code):
    backend_url = URL + "register"
    payload = {
        'name': name,
        'time': time,
        'performance': performance,
        'function': function_code,
    }
    response = requests.post(backend_url, json=payload)
    if response.status_code != 200:
        print(f"Failed to post data to backend. Status code: {response.status_code}, Message: {response.text}")
    else:
        print(f"Successfully posted data to backend!")
