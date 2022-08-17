# coding: utf-8
"""
Служба-нотфикатор.
TODO: логгер, cron, try-except, группировка при рассылки сообщений
"""

__author__ = "aa.blinov"


from json import dumps
from typing import List, Tuple

from db.models import FcmMessage, FcmMessagePerson, FcmPerson
from db.utils import session
from log import logger
from push import push_service


def get_all_persons() -> List[str]:
    """
    Получить всех пользователей.
    """
    return session.query(FcmPerson.id_fcm).all()


def get_raw_news(was_processed: int = 0, only_first: bool = False) -> List[FcmMessage]:
    """
    Получить новости.
    """
    query = session.query(FcmMessage) \
        .filter(
            FcmMessage.type == "news",
            FcmMessage.was_processed == was_processed
        )

    return query.first() if only_first else query.all()


def publish_news(new_news: List[FcmMessage], all_persons: List[str]) -> bool:
    """
    Опубликовать новости.
    """
    # new_news = get_raw_news(was_processed=0, only_first=False)
    # all_persons = get_all_persons()

    for news in new_news:
        data_msg = {
            "type": news.type,
            "isImportant": str(bool(news.is_important)).lower(),
            "entity": dumps({
                "ID": news.id,
                "MAIN_PICTURE": news.main_picture,
                "NEWS_DATE": news.news_date.isoformat(sep='T', timespec="seconds"),
                "PREVIEW_MAIN_PICTURE": news.preview_main_picture,
                "SHORT_TEXT": news.short_text,
                "TEXT": news.text_,
                "TITLE": news.tittle,
            }, ensure_ascii=False),
        }

        push_service.multiple_devices_data_message(
            registration_ids=all_persons,
            data_message=data_msg,
            low_priority=False
        )

    return True


def get_raw_messages(was_processed: int = 0, only_first: bool = False) -> List[Tuple[FcmMessage, FcmPerson]]:
    """
    Получить личные сообщения.
    """
    query = session.query(
        FcmMessage, FcmPerson
    ).join(
        FcmMessagePerson, FcmMessage.id == FcmMessagePerson.id_fcm_messages
    ).join(
        FcmPerson, FcmMessagePerson.id_fcm_person == FcmPerson.id
    ).filter(
        FcmMessage.type == "messages",
        FcmMessage.was_processed == was_processed
    )

    return query.first() if only_first else query.all()


def publish_message(msgs: List[Tuple[FcmMessage, FcmPerson]]) -> bool:
    """
    Опубликовать сообщение для пользоваетелей.
    """
    # msgs = get_raw_messages(was_processed=0, only_first=False)

    for msg in msgs:
        data_msg = {
            "type": msg[0].type,
            "isImportant": str(bool(msg[0].type.is_important)).lower(),
            "entity": dumps({
                "ID": msg[0].id,
                "DATE_SENT": msg[0].date_sent.isoformat(sep='T', timespec="seconds"),
                "FIO_AUTHOR": msg[0].fio_author,
                "PORTRAIT_URL": msg[0].fio_author,
                "TEXT": msg[0].text_,
                "TITTLE": msg[0].title(),
            }, ensure_ascii=False),
        }

        push_service.multiple_devices_data_message(
            registration_id=msg[1].id_fcm,
            data_message=data_msg,
            low_priority=False
        )

    return True


def main():
    """
    Главная функция.
    """
    # новости
    new_news = get_raw_news(was_processed=0, only_first=False)  # получаем все "новые" новости\
    all_persons = get_all_persons()  # получаем всех пользователей
    result = publish_news(new_news, all_persons)  # публикуем новости во всех пользователей
    if result:
        pass
    else:
        pass


if __name__ == "__main__":
    main()
