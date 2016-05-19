import requests


if __name__ == '__main__':
    resp = requests.get("http://192.168.2.1:8000/picture/")
    if resp.status_code == 200:
        with open("test2.jpg", "w+b") as pic:
            pic.write(resp.content)
