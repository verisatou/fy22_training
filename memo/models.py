from django.db import models
from login.models import CustomUser

CHOICES = (
    ("未達成", "未達成"),
    ("達成", "達成"),
)

class Memo(models.Model): 
    problem = models.CharField('課題点', max_length=50, blank=False)
    solution = models.CharField('改善案', max_length=500, blank=False )
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    status = models.CharField("ステータス", max_length=10, choices=CHOICES, blank=False)
    created_at = models.DateTimeField('作成日時', auto_now_add=True)
    updated_at = models.DateTimeField('更新日時',auto_now=True)

    def __str__(self):
        return self.problem