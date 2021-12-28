from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute, NumberAttribute

endpoint_url = 'http://localhost:18000'


class Score(Model):
    class Meta:
        table_name = 'Score'
        region = 'ap-northeast-1'
        aws_access_key_id = 'ACCESS_ID'
        aws_secret_access_key = 'ACCESS_KEY'
        host = endpoint_url

    question_id = UnicodeAttribute(hash_key=True)
    answer = UnicodeAttribute()
    score = NumberAttribute()
