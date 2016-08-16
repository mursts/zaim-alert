# Zaim-Alert

Zaimにランチ代の登録忘れがあればslackに通知します

## 環境

- Python3
- Heroku

## 使い方

```sh
$ heroku login

$ heroku config:set TZ=Asia/Tokyo # your timezone
$ heroku config:set ZAIM_ACCESS_TOKEN_KEY= your zaim access token key
$ heroku config:set ZAIM_ACCESS_TOKEN_SECRET=your zaim access token secret
$ heroku config:set ZAIM_CONSUMER_KEY=your zaim consumer key
$ heroku config:set ZAIM_CONSUMER_SECRET=your zaim consumer secret
$ heroku config:set SLACK_WEBHOOK_URL=webhook url


$ git push heroku master

```