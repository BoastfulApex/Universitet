from io import BytesIO
import os
import struct
from typing import Sequence, Union
import zipfile
import requests
from telegram import ReplyKeyboardMarkup as _ReplyKeyboardMarkup, File
from telegram._keyboardbutton import KeyboardButton
from telegram._utils.types import JSONDict


class ReplyKeyboardMarkup(_ReplyKeyboardMarkup):
    def __init__(
        self,
        keyboard: Sequence[Sequence[str | KeyboardButton]],
        # home=True,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = None,
        selective: bool = None,
        input_field_placeholder: str = None,
        is_persistent: bool = None,
        *,
        api_kwargs: JSONDict = None,
    ):
        # if home:
        #     keyboard += [["🏠 Bosh menu"]]
        super().__init__(
            keyboard,
            True,
            one_time_keyboard,
            selective,
            input_field_placeholder,
            is_persistent,
            api_kwargs=api_kwargs,
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


def norm(number):
    number = str(number)
    number.replace(" ", "")
    if len(number) == 9:
        number = f"+998{number}"
    elif len(number) == 12:
        if not number.startswith("+"):
            number = f"+{number}"
    return number


def send_sms(phone, text):
    username = "onlineqabul"
    password = "p7LnIrh+-Vw"
    sms_data = {
        "messages": [
            {
                "recipient": norm(phone),
                "message-id": "abc000000003",
                "sms": {"originator": "3700", "content": {"text": text}},
            }
        ]
    }
    url = "http://91.204.239.44/broker-api/send"
    requests.post(url=url, headers={}, auth=(username, password), json=sms_data)
