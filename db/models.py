# coding: utf-8

"""
Модели для уведомлений.
"""


from sqlalchemy import Column, DateTime, Integer, TIMESTAMP, VARCHAR, text
from sqlalchemy.dialects.oracle import NUMBER
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class FcmMessage(Base):
    __tablename__ = 'fcm$message'
    __table_args__ = {'schema': 'apiuser'}

    id = Column(NUMBER(asdecimal=True), primary_key=True)
    type = Column(VARCHAR(128))
    is_important = Column(NUMBER(asdecimal=True))
    for_all = Column(NUMBER(asdecimal=True))
    id_entity = Column(NUMBER(asdecimal=True))
    date_sent = Column(DateTime)
    fio_author = Column(VARCHAR(1024))
    portrait_url = Column(VARCHAR(1024))
    text_ = Column("text", VARCHAR(100))
    tittle = Column(VARCHAR(100))
    short_text = Column(VARCHAR(100))
    main_picture = Column(VARCHAR(1024))
    news_date = Column(DateTime)
    preview_main_picture = Column(VARCHAR(1024))
    date_add = Column(DateTime, nullable=False, server_default=text("sysdate "))
    was_processed = Column(NUMBER(1, 0, False), nullable=False, server_default=text("0 "), comment='Факт обработки сообщения: 1 - успех, 0 - еще не обработано, -1 - ошибка')


class FcmMessagePerson(Base):
    __tablename__ = 'fcm$message_person'
    __table_args__ = {'schema': 'apiuser'}

    id = Column(NUMBER(asdecimal=True), primary_key=True)
    id_fcm_messages = Column(NUMBER(asdecimal=True), nullable=False)
    id_fcm_person = Column('id_fcm$person', NUMBER(asdecimal=True), nullable=False)
    date_add = Column(DateTime, nullable=False, server_default=text("sysdate "))


class FcmPerson(Base):
    __tablename__ = 'fcm$person'
    __table_args__ = {'schema': 'apiuser'}

    id = Column(Integer, primary_key=True)
    nstu_email = Column(VARCHAR(255))
    id_fcm = Column(VARCHAR(327))
    timestamp_added = Column(TIMESTAMP, server_default=text("CURRENT_TIMESTAMP"))
    platform = Column(VARCHAR(256))
