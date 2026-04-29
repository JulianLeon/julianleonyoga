import re

from django import forms


SPAM_ERROR_MESSAGE = (
    "Deine Nachricht konnte nicht gesendet werden. Bitte formuliere sie etwas "
    "persönlicher oder kontaktiere mich direkt per E-Mail."
)


SPAM_KEYWORDS = (
    "bitcoin",
    "casino",
    "crypto",
    "forex",
    "free money",
    "loan",
    "make money",
    "marketing agency",
    "nft",
    "online casino",
    "rank higher",
    "seo",
    "viagra",
    "weight loss",
)


URL_PATTERN = re.compile(r"(https?://|www\.|[a-z0-9-]+\.(?:com|net|org|info|biz|ru|cn|xyz)\b)", re.IGNORECASE)
REPEATED_CHAR_PATTERN = re.compile(r"(.)\1{5,}")
EMAIL_PATTERN = re.compile(r"[\w.+-]+@[\w-]+\.[\w.-]+")


def _normalize(value):
    return " ".join((value or "").lower().split())


def _contains_spam_keyword(text):
    return any(keyword in text for keyword in SPAM_KEYWORDS)


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

    def clean(self):
        cleaned_data = super().clean()
        name = _normalize(cleaned_data.get('name'))
        betreff = _normalize(cleaned_data.get('betreff'))
        nachricht = _normalize(cleaned_data.get('nachricht'))
        combined_text = f"{name} {betreff} {nachricht}"

        spam_score = 0

        if URL_PATTERN.search(combined_text):
            spam_score += 2

        if len(URL_PATTERN.findall(combined_text)) > 1:
            spam_score += 2

        if _contains_spam_keyword(combined_text):
            spam_score += 2

        if REPEATED_CHAR_PATTERN.search(combined_text):
            spam_score += 1

        if nachricht and len(nachricht) < 20:
            spam_score += 1

        if len(EMAIL_PATTERN.findall(nachricht)) > 1:
            spam_score += 2

        if name and any(char.isdigit() for char in name):
            spam_score += 1

        if spam_score >= 3:
            raise forms.ValidationError(SPAM_ERROR_MESSAGE)

        return cleaned_data
