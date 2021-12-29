import os
import json
import boto3

from linebot import LineBotApi
from linebot.models import TextSendMessage, FlexSendMessage

from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute, MapAttribute

access_token = os.getenv('LINE_ACCESS_TOKEN')
line_bot = LineBotApi(access_token)

endpoint_url = os.getenv('DYNAMODB_ENDPOINT', None)
dynamodb = boto3.resource('dynamodb', endpoint_url=endpoint_url)
scores = dynamodb.Table('Score')


class ScoreMap(MapAttribute):
    q1 = NumberAttribute(null=True)
    q2 = NumberAttribute(null=True)
    q3 = NumberAttribute(null=True)


class UserScore(Model):
    class Meta:
        table_name = 'UserScore'
        region = 'ap-northeast-1'
        if endpoint_url:
            host = endpoint_url

    line_user_id = UnicodeAttribute(hash_key=True)
    scores = MapAttribute(of=ScoreMap)


# テーブルが存在しない場合は作成する
if not UserScore.exists():
    UserScore.create_table(read_capacity_units=1,
                           write_capacity_units=1, wait=True)


def get_result(question, answer):
    question_info = scores.get_item(Key={"question_id": question})['Item']
    score = 0
    if question_info['answer'] == answer:
        score = int(question_info['score'])
    return score


def get_next_question(inserted_question):
    if inserted_question == 'q1':
        next_question = scores.get_item(
            Key={"question_id": 'q2'}
        )['Item']['question']
    elif inserted_question == 'q2':
        next_question = scores.get_item(
            Key={"question_id": 'q3'}
        )['Item']['question']
    return FlexSendMessage(
        alt_text='Next Question',
        contents=json.loads(next_question)
    )


def update_score(user_score, answer):
    # 各設問に対するスコアを挿入する
    inserted_question = ''
    if user_score.scores['q1'] is None:
        score = get_result('q1', answer)
        inserted_question = 'q1'
    elif user_score.scores['q2'] is None:
        score = get_result('q2', answer)
        inserted_question = 'q2'
    elif user_score.scores['q3'] is None:
        score = get_result('q3', answer)
        inserted_question = 'q3'

    # スコアを更新する
    if inserted_question != '':
        user_score.scores[inserted_question] = score
        user_score.save()
    if score == 0:
        result_msg = TextSendMessage(text='不正解です')
    else:
        result_msg = TextSendMessage(text='正解です')

    # 最終問題であれば結果を返す
    if inserted_question == 'q3':
        result_data = UserScore.get(user_score.line_user_id)
        total_score = result_data.scores['q1'] + \
            result_data.scores['q2'] + result_data.scores['q3']
        next_msg = TextSendMessage(
            text='以上で問題は終了です\n合計得点は{}点です'.format(total_score))
    else:
        next_msg = get_next_question(inserted_question)

    # 次の設問を返す
    return {
        'inserted_question': inserted_question,
        'score': score,
        'msg': [result_msg, next_msg]
    }


def lambda_handler(event, context):
    print("Received event: " + json.dumps(event, indent=2))
    # 接続確認
    if len(event['events']) == 0:
        return {
            'statusCode': 200,
            'body': 'OK'
        }

    # Webhookから必要な値を取得
    user_id = event['events'][0]['source']['userId']
    reply_token = event['events'][0].get('replyToken')
    event_type = event['events'][0]['type']
    message_text = event['events'][0]['message']['text'] if event_type == 'message' else ''

    if event_type == 'follow' or message_text == 'start':
        # 友だち追加時に初期値を設定する
        UserScore(
            line_user_id=user_id,
            scores=ScoreMap(q1=None, q2=None, q3=None)
        ).save()

        first_question = scores.get_item(
            Key={"question_id": 'q1'}
        )['Item']['question']
        greet_msg = TextSendMessage(
            text='このbotでは簡単な3択クイズを用意しました\nそれでは始めていきましょう！'
        )
        question_msg = FlexSendMessage(
            alt_text='First Question',
            contents=json.loads(first_question)
        )
        line_bot.reply_message(
            reply_token,
            [greet_msg, question_msg]
        )
        return {
            'statusCode': 200,
            'body': json.dumps('Init Success!')
        }
    elif event_type == 'unfollow':
        # ブロックされた時にはデータを削除する
        UserScore.get(user_id).delete()
        return {
            'statusCode': 200,
            'body': json.dumps('Delete Success!')
        }
    else:
        user_score = UserScore.get(user_id)
        # 返信メッセージを作成する
        if message_text.isnumeric():
            result = update_score(user_score, message_text)
            print('Question: {}\nScore: {}'.format(
                result['inserted_question'], result['score']))
            msg_obj = result['msg']
        else:
            msg_obj = TextSendMessage(text='数字を入力してください')

        line_bot.reply_message(
            reply_token,
            msg_obj
        )
        return {
            'statusCode': 200,
            'body': json.dumps('OK')
        }
