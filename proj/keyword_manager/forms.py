from django import forms
from .models import Keyword
import re

class KeywordForm(forms.ModelForm):
    class Meta:
        model = Keyword
        fields = ['text']
        labels = {'text': 'Keyword'}

    def clean_text(self):
        text = self.cleaned_data['text']
        if len(text) < 2:
            raise forms.ValidationError("최소 2글자 이상 입력하세요.")
        elif len(text) > 50:
            raise forms.ValidationError("최대 50글자 이하로 입력하세요.")
        elif not re.match(r'^[A-Za-z0-9\s]+$', text):
            raise forms.ValidationError("특수문자는 입력할 수 없습니다.")
        return text