# coding: utf-8
"""
Инициализация push-сервиса.
"""

__author__ = "aa.blinov"


from json import load
from os.path import join

from pyfcm import FCMNotification


def get_api_key(file_path: str) -> str:
    """
    Получить API ключ.
    """
    fcm_config = None
    with open(file_path, "r") as file:
        fcm_config = load(file)

    return fcm_config.get("api-key")


push_service = FCMNotification(
    api_key=get_api_key(join("configs", "yourneti-firebase-adminsdk.json"))
)
