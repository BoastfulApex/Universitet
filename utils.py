import requests


def send_sms(phone: str, otp: int):
    username = "onlineqabul"
    password = "p7LnIrh+-Vw"

    url = "http://91.204.239.44/broker-api/send"
    requests.post(
        url=url,
        headers={},
        auth=(username, password),
        json={
            "messages": [
                {
                    "recipient": phone,
                    "message-id": "1",
                    "sms": {
                        "originator": "3700",
                        "content": {"text": f"Sizning tasdiqlash ko'dingiz: {otp}"},
                    },
                }
            ]
        },
    )


def distribute(items, number) -> list:
    res = []
    start = 0
    end = number
    for item in items:
        if items[start:end] == []:
            return res
        res.append(items[start:end])
        start += number
        end += number
    return res
