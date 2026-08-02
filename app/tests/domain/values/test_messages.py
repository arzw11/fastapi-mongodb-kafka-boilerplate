from datetime import datetime
from uuid import uuid4

import pytest

from domain.entities.messages import (
    Chat,
    Message,
)
from domain.events.messages import NewMessageReceivedEvent
from domain.exceptions.messages import TitleTooLongException
from domain.values.messages import (
    Text,
    Title,
)


def test_create_message_success_short_text():
    text = Text('hello')
    message = Message(text=text, chat_oid=str(uuid4()))

    assert message.text == text, f'{message=}'
    assert message.created_at.date() == datetime.today().date(), f'{message=}'


def test_create_message_success_long_text():
    text = Text('hello' * 400)
    message = Message(text=text, chat_oid=str(uuid4()))

    assert message.text == text, f'{message=}'
    assert message.created_at.date() == datetime.today().date(), f'{message=}'


def test_create_chat_success():
    title = Title('title')
    chat = Chat(title=title)

    assert chat.title == title, f'{chat=}'
    assert not chat.messages, f'{chat=}'
    assert chat.created_at.date() == datetime.today().date(), f'{chat=}'


def test_create_chat_title_too_long():
    with pytest.raises(TitleTooLongException):
        Title('hello' * 400)


def test_add_chat_to_message():
    text = Text('hello')
    message = Message(text=text, chat_oid=str(uuid4()))

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message=message)

    assert message in chat.messages, f'{chat=}'


def test_new_message_events():
    text = Text('hello world')
    message = Message(text=text, chat_oid=str(uuid4()))

    title = Title('title')
    chat = Chat(title=title)

    chat.add_message(message=message)
    events = chat.pull_events()
    pulled_events = chat.pull_events()

    assert not pulled_events, f'{pulled_events=}'
    assert len(events) == 1, f'{events=}'

    new_event = events[0]

    assert isinstance(new_event, NewMessageReceivedEvent), f'{new_event=}'
    assert new_event.message_oid == message.oid, f'{new_event=}'
    assert new_event.message_text == message.text.as_generic_type(), f'{new_event=}'
    assert new_event.chat_oid == chat.oid, f'{new_event=}'
