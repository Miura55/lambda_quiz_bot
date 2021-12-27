# lambda_quiz_bot
LambdaとDynamo DBを使ったクイズを行うLINE bot(ローカルのテスト用のDocker入り)
## ローカルでの実行
`.env`ファイルを用意して以下の設定を用意

```
LINE_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"
```

Dockerコンテナを起動(lambdaのコードを変更したら毎回実行する)

```
docker-compose up -d --build
```

ngrokでローカルポートを払い出す

```
ngrok http 18080
```

Messaging APIのWebhook URLを設定するときには以下のようになる


```
【ngrokのURL】/2015-03-31/functions/function/invocations
```
