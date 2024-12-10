from django import forms

from posts.models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group')
        labels = {
            'text': 'Текст поста',
            'group': "Выберите группу"
        }
        widgets = {
            'text': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'введите текст поста'}),
            'group': forms.Select(attrs={'class': 'form-control'}),
        }
