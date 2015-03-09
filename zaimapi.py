#!/usr/bin/env python
# coding: utf-8

import requests
from requests_oauthlib import OAuth1

# Zaim API ver 2.0.3
API_ROOT = "https://api.zaim.net/v2/"


class Zaim(object):
    def __init__(self, consumer_key, consumer_secret,
                 access_token_key, access_token_secret):
        self.categories = {}
        self.user = {}
        self.accounts = {}
        self.currencies = {}
        self.auth = OAuth1(consumer_key, consumer_secret,
                           access_token_key, access_token_secret)

    def _request(self, method, url, data=None, params=None):
        r = requests.request(method, url, auth=self.auth,
                             data=data, params=params)
        return r.json()

    def get_genres(self, mode=None):
        data = None
        if mode:
            data = {"mode": mode}

        endpoint = API_ROOT + "home/genre"
        r = self._request('get', endpoint, data)
        self.genres = r["genres"]

        return self.genres

    def get_categories(self, mode=None):
        data = None
        if mode:
            data = {"mode": mode}

        endpoint = API_ROOT + "home/category"
        r = self._request('get', endpoint, data)
        return r["categories"]

    def get_user(self):
        if not self.user:
            endpoint = API_ROOT + "home/user/verify"
            r = self._request('get', endpoint)
            return r["me"]

        return self.user

    def get_user_id(self):
        return self.get_user()["id"]

    def get_currencies(self):
        if not self.currencies:
            endpoint = API_ROOT + "currency"
            r = self._request('get', endpoint)
            return r["currencies"]

        return self.currencies

    def get_currency_sign(self, currency_code):
        currencies = self.get_currencies()
        for d in currencies:
            if d["currency_code"] == currency_code:
                return d["unit"]

    def get_accounts(self):
        endpoint = API_ROOT + "home/account"

        if not self.accounts:
            r = self._request('get', endpoint)
            self.accounts =  r["accounts"]

        return self.accounts

    def get_account_by_name(self,name):
        accounts = self.get_accounts()
        for d in accounts:
            if d["name"] == name:
                return d
        raise ValueError("Account not found: " + name)

    def create_pay(self, **params):
        endpoint = API_ROOT + "home/money/payment"

        data = {
            "category_id": params["category_id"],
            "genre_id": params["genre_id"],
            "amount": params['amount'],
            "date": params["date"].strftime("%Y-%m-%d"),
        }

        if 'from_account_id' in params:
            data['from_account_id'] = params['from_account_id']

        if 'name' in params:
            data["name"] = params["name"]

        if 'place' in params:
            data["place"] = params["place"]

        if 'comment' in params:
            data["comment"] = params["comment"]

        return self._request('post', endpoint, data)

    def delete_pay(self, money_id):
        endpoint = API_ROOT + "home/money/payment/" + money_id

        try:
            if self.get_money_record_by_id(money_id):
                return self._request('delete', endpoint)
        except ValueError:
            raise ValueError("Money record not found: " + money_id)

    def create_income(self, **params):
        endpoint = API_ROOT + "home/money/income"

        data = {
            "category_id": params["income_category"],
            "amount": params["amount"],
            "date": params["date"].strftime("%Y-%m-%d") if params["date"] else "",
            "to_account_id": params["to_account_id"],
        }

        if 'comment' in params:
            data["comment"] = params["comment"]

        return self._request('post', endpoint, data=data)

    def get_money_records(self, params=None):
        endpoint = API_ROOT + "home/money"
        r = self._request('get', endpoint, params=params)
        return  r["money"]

    def get_money_record_by_id(self,money_id, params=None):
        records = self.get_money_records(params)
        for d in records:
            if d["id"] == money_id:
                return d
        raise ValueError("Money record not found: " + money_id)

    def get_genre_by_name(self, name):
        genres = self.get_genres()
        for d in genres:
            if d["name"] == name:
                return d
        raise ValueError("Genre not found: " + name)

    def get_category_by_name(self, name):
        categories = self.get_categories()
        for d in categories:
            if d["name"] == name:
                return d
        raise ValueError("Category not found: " + name)

    def get_genre_id_by_name(self, name):
        return self.get_genre_by_name(name)["id"]

    def get_category_id_by_name(self, name):
        return self.get_category_by_name(name)["id"]
