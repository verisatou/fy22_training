from django import forms
from .models import Memo

class MemoForm(forms.ModelForm):
    class Meta:
        model = Memo
        exclude = ('created_at','updated_at','user_id','status')  #入力項目から作成日時、更新日時を除外