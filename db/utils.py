# coding: utf-8
"""
Работа с сессией и прочие методы.
"""

__author__ = "aa.blinov"


from json import load
from os.path import join

from sqlalchemy import create_engine
from sqlalchemy.orm.session import sessionmaker


config_data = None
with open(join("configs", "db.json"), "r") as file:
    config_data = load(file)

engine_oracle = create_engine(
    "{DB}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DB_NAME}".format(**config_data),
    echo=False
)
factory = sessionmaker(bind=engine_oracle, autocommit=False, autoflush=False)
session = factory()
