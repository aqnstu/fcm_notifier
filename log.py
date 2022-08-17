# coding=utf-8
"""
Логгирование.
"""

__author__ = "aa.blinov"


from os.path import join

from loguru import logger

logger.remove()  # убираем вывод в консоль

logger.add(
    join("logs", "fcm.log"),
    mode="a+",
    backtrace=True,
    diagnose=True,
    level="INFO",
    encoding="utf-8",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
)