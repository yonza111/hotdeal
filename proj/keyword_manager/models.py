from django.db import models
from django.contrib.auth.models import User

class Keyword(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'text'], 
                                    name='unique_user_keyword')
        ]
        # unique=True 하면 user과 관계없이 text 한번 등록되면 끝이라서
        # UniqueConstraint로 user-text 두 필드의 조합이 
        # 데이터베이스 내에서 유일해야 함을 의미
    def __str__(self):
        return self.text