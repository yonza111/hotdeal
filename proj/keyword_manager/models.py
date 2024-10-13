# keyword_manager/models.py
from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


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




class DiscordMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    keyword = models.ForeignKey(Keyword, on_delete=models.CASCADE)
    discord_uid = models.CharField(max_length=50, null=True, blank=True)
    active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}'s Discord Message"

    @classmethod
    def create_discord_uid(cls, user):
        user_social_account = SocialAccount.objects.filter(user_id=user.id, provider='discord').first()
        if user_social_account:
            return user_social_account.uid
        return None
    
    @classmethod
    def get_user_keywords(cls, user):
        return Keyword.objects.filter(user=user)
    

@receiver(post_save, sender=Keyword)
def create_discord_message(sender, instance, created, **kwargs):
    if created:
        user = instance.user
        discord_uid = DiscordMessage.create_discord_uid(user)
        discord_message = DiscordMessage.objects.create(user=user, keyword=instance, discord_uid=discord_uid)
        
        # 현재 사용자의 DiscordMessage 객체 중 첫 번째 객체의 active 상태를 가져옴
        user_discord_message = DiscordMessage.objects.filter(user=user).first()
        if user_discord_message:
            discord_message.active = user_discord_message.active
            discord_message.save()

@receiver(post_delete, sender=Keyword)
def delete_discord_message(sender, instance, **kwargs):
    DiscordMessage.objects.filter(keyword=instance).delete()