# Zaim-Alert

Zaimにランチ代の登録忘れがあればslackに通知します。  
月末にはレポートをSlackに送信する

## 環境

- Python 3.7
- Google App Engine

## 使い方

```sh
$ pip install -r requirements.txt
$ mv config.py.org config.py
$ vi config.py
$ appcfg.py update -A <YOUR_PROJECT_ID> ./
```
