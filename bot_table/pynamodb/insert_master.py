from QuizModel import Score

if not Score.exists():
    Score.create_table(read_capacity_units=1,
                       write_capacity_units=1, wait=True)

# スコア情報を挿入する
Score(question_id='q1', question='1問目：日本の首都は？\n1:名古屋\n2:大阪\n3:東京',
      answer='3', score=10).save()
Score(question_id='q2', question='2問目：AWSのサーバーレス実行環境、正しいのはどれ？\n1:lambda\n2:lamda\n3:lamdba',
      answer='1', score=20).save()
Score(question_id='q3', question='3問目：新しい1万円札の顔は？\n1:新渡戸稲造\n2:渋沢栄一\n3:福沢諭吉',
      answer='2', score=20).save()
print('Done!')
