from django import forms
from .models import Feedback
from .models import Reply

class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        #入力項目から作成日時、更新日時,senderを除外
        exclude = ('created_at','updated_at')

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
         #入力項目から作成日時、更新日時,senderを除外
        # exclude = ('created',)
        exclude = ('created','feedback_id','replyer')

