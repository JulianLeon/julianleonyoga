from django import forms

class ContactForm(forms.Form):

    honeypot = forms.CharField(required=False, widget=forms.HiddenInput)

    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dein Name'
        })
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'Deine E-Mail'
        })
    )
    betreff = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Dein Betreff'
        })
    )
    nachricht = forms.CharField(
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'Deine Nachricht',
            'rows': 5
        })
    )

    def clean_honeypot(self):
        data = self.cleaned_data['honeypot']
        if data:  # wenn ein Bot das Feld ausfüllt
            raise forms.ValidationError("Bot erkannt.")
        return data