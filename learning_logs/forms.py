from django import forms

from .models import Topic, Entry


class TopicForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ["topic_text"]
        labels = {"topic_text": "主题"}
        widgets = {
            "topic_text": forms.TextInput(attrs={
                "class": "form-control",
            })
        }


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
        fields = ["entry_text"]
        labels = {"entry_text": "条目内容"}
        widgets = {
            "entry_text": forms.Textarea(attrs={
                "class": "form-control",
                "rows": 5
            })
        }
