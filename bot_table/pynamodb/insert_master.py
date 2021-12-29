import json
from QuizModel import Score

if not Score.exists():
    Score.create_table(read_capacity_units=1,
                       write_capacity_units=1, wait=True)

with open('flex_messages.json', 'r') as f:
    flex_messages = json.load(f)

# スコア情報を挿入する
Score(question_id='q1', question=json.dumps(flex_messages['q1']),
      answer='3', score=10).save()
Score(question_id='q2', question=json.dumps(flex_messages['q2']),
      answer='1', score=20).save()
Score(question_id='q3', question=json.dumps(flex_messages['q3']),
      answer='2', score=20).save()
print('Done!')
