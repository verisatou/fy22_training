from django.db import models
from login.models import CustomUser

class Feedback(models.Model):
    # プルダウンの選択肢
    CHOICES = (
        ("0", "GOOD"),
        ("1", "MORE"),
        ("2", "その他"),
    )

    title = models.CharField('題名', max_length=50, blank=False)
    user_id = models.ForeignKey(CustomUser,verbose_name='宛名',on_delete=models.CASCADE)
    content = models.TextField('内容', max_length=500, blank=False)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)
    sender = models.CharField('送信者', max_length=50, blank=False)
    anonymous = models.BooleanField('匿名投稿',default=False)
    category = models.CharField("カテゴリ", max_length=20, choices=CHOICES, blank=False)

    def __str__(self):
        return self.title

class Reply(models.Model):
    reply_content = models.TextField('内容', max_length=300,blank=False)
    feedback_id = models.ForeignKey(Feedback, on_delete=models.CASCADE)
    created = models.DateTimeField('送信日時', auto_now_add=True)
    replyer = models.CharField('返信者', max_length=50, blank=False)
    # user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)

    def __str__(self):
        return self.reply_content
