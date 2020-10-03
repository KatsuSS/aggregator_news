import pytest
from flask import url_for


def test_get_home_page(client):
    res = client.get(url_for("main.index"))
    assert res.status_code == 200


def test_get_new_with_id(client):
    res = client.get(url_for("api.get_new", id=1))
    assert res.status_code == 200
    assert res.json == {
        '_links': {
            'resource': '/api/news/resource/1',
            'self': 'https://daily.afisha.ru/news/40588-stiven-fray-podderzhal-protestuyuschih-v-belarusi/'},
        'header': 'Стивен Фрай поддержал протестующих в Беларуси',
        'time': '2020-08-20T12:20:30.025249Z'}
