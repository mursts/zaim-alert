# Zaim-Alert

Zaimにランチ代の登録忘れがあればPushbulletに通知します

## 環境

- Python3
- Heroku

## 使い方

```sh
$ heroku login

$ heroku config:set PUSHBULLET_TARGET_DEVICE=yourpushbulett device
$ heroku config:set PUSHBULLET_TOKEN=your pushbullet token
$ heroku config:set TZ=Asia/Tokyo # your timezone
$ heroku config:set ZAIM_ACCESS_TOKEN_KEY= your zaim access token key
$ heroku config:set ZAIM_ACCESS_TOKEN_SECRET=your zaim access token secret
$ heroku config:set ZAIM_CONSUMER_KEY=your zaim consumer key
$ heroku config:set ZAIM_CONSUMER_SECRET=your zaim consumer secret

$ git push heroku master

```