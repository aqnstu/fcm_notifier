# coding: utf-8
"""
Служба-нотфикатор.
"""

__author__ = "aa.blinov"


from json import dumps
from traceback import format_exc
from typing import List, Optional, Tuple

from db.models import FcmMessage, FcmMessagePerson, FcmPerson
from db.utils import session
from log import logger
from push import push_service


def get_all_persons() -> List[Optional[str]]:
    """
    Получить всех пользователей.
    """
    persons = session.query(
        FcmPerson.id_fcm
    ).all()

    if persons:
        return [registration_id for registration_id, in persons]

    return []


def get_raw_news(was_processed: int = 0, only_first: bool = False) -> List[FcmMessage]:
    """
    Получить новости.
    """
    query = session.query(FcmMessage).filter(
        FcmMessage.type == "news",
        FcmMessage.was_processed == was_processed
    )

    return query.first() if only_first else query.all()


def publish_news(new_news: List[FcmMessage], all_persons: List[str]) -> None:
    """
    Опубликовать новости.
    """
    for news in new_news:
        data_msg = {
            "type": str(news.type),
            "isImportant": str(bool(news.is_important)).lower(),
            "entity": dumps(
                {
                    "ID": int(news.id),
                    "MAIN_PICTURE": news.main_picture,
                    "NEWS_DATE": news.news_date.isoformat(sep="T", timespec="seconds"),
                    "PREVIEW_MAIN_PICTURE": news.preview_main_picture,
                    "SHORT_TEXT": news.short_text,
                    "TEXT": news.text_,
                    "TITLE": news.tittle,
                },
                ensure_ascii=False,
            ),
        }

        try:
            push_service.multiple_devices_data_message(
                registration_ids=all_persons,
                data_message=data_msg,
                low_priority=False
            )

            was_processed = 1  # факт обработки
        except Exception:
            was_processed = -1  # факт ошибки
            logger.error(f"id - {int(news.id)}: {format_exc()}")

        session.query(FcmMessage).filter(FcmMessage.id == news.id).update({
            FcmMessage.was_processed: was_processed
        })
        session.commit()


def get_raw_messages(
    was_processed: int = 0, only_first: bool = False
) -> List[Tuple[FcmMessage, FcmPerson]]:
    """
    Получить личные сообщения.
    """
    query = session.query(FcmMessage).filter(
        FcmMessage.type == "messages",
        FcmMessage.was_processed == was_processed,
    )

    return query.first() if only_first else query.all()


def get_persons_for_message(id_msg: int) -> List[FcmPerson]:
    """
    Получить registration_id пользователей для рассылки по сообщению.
    """
    query = (
        session.query(FcmPerson.id_fcm)
        .join(FcmMessagePerson, FcmMessagePerson.id_fcm_person == FcmPerson.id)
        .filter(FcmMessagePerson.id_fcm_messages == id_msg)
        .all()
    )

    if query:
        return [registration_id for registration_id, in query]

    return []


def publish_message(msgs: List[FcmMessage]) -> None:
    """
    Опубликовать сообщение для пользоваетелей.
    TODO: Оптимизировать агрегацию.
    """
    for msg in msgs:
        data_msg = {
            "type": msg.type,
            "isImportant": str(bool(msg.is_important)).lower(),
            "entity": dumps(
                {
                    "ID": int(msg.id),
                    "DATE_SENT": msg.date_sent.isoformat(sep="T", timespec="seconds"),
                    "FIO_AUTHOR": msg.fio_author,
                    "PORTRAIT_URL": msg.portrait_url,
                    "TEXT": msg.text_,
                    "TITTLE": msg.tittle,
                },
                ensure_ascii=False,
            ),
        }

        persons = get_persons_for_message(
            msg.id
        )  # получаем пользоваетлей в разрезе сообщений

        try:
            push_service.multiple_devices_data_message(
                registration_ids=persons,
                data_message=data_msg,
                low_priority=False
            )
            was_processed = 1  # факт обработки
        except Exception:
            was_processed = -1  # факт ошибки
            logger.error(f"id - {int(msg.id)}: {format_exc()}")

        session.query(FcmMessage).filter(FcmMessage.id == msg.id).update({
            FcmMessage.was_processed: was_processed
        })
        session.commit()


def main():
    """
    Главная функция.
    """
    # новости
    new_news = get_raw_news(was_processed=0, only_first=False)  # получаем все "новые" новости
    all_persons = get_all_persons()  # получаем всех пользователей
    publish_news(new_news, all_persons)  # публикуем новости во всех пользователей

    # сообщения
    new_msgs = get_raw_messages(was_processed=0)  # получаем все "новые" сообщения
    publish_message(new_msgs)  # публикуем сообщения в нужных пользователей


if __name__ == "__main__":
    main()
