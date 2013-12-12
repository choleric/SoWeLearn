
from django import forms



class UserQuoteForm(forms.Form):
    user_quote= forms.CharField(max_length=20)

    def clean_user_quote(self):
        user_quote = self.cleaned_data['user_quote']
        if len(user_quote) > 20:
            raise forms.ValidationError('too long quote')
        return user_quote

