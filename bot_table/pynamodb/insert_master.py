from QuizModel import Score

if not Score.exists():
    Score.create_table(read_capacity_units=1,
                       write_capacity_units=1, wait=True)

# スコア情報を挿入する
Score(question_id='q1', answer='3', score=10).save()
Score(question_id='q2', answer='1', score=20).save()
Score(question_id='q3', answer='2', score=20).save()
print('Done!')
