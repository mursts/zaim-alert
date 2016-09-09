# Zaim-Alert

Zaimにランチ代の登録忘れがあればslackに通知します。平日の12:45に実行

## 環境

- Python 2.7
- Google App Engine

## 使い方

```sh
$ pip install -r requirements.txt -t lib
$ mv config.py.org config.py
$ vi config.py
$ vi app.yaml # add application id
$ appcfg.py update -A <YOUR_PROJECT_ID> ./
```