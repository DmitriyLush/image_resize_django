from django import forms
from pill.models import Images

class Images(forms.ModelForm):
    class Meta:
        model = Images
        fields = "__all__"
