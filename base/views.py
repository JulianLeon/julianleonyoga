from django.shortcuts import render
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from contact.forms import ContactForm


# Create your views here.
def home(request):

    form_submitted = False
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            ## Daten aus Formular holen
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            betreff = form.cleaned_data['betreff']
            nachricht = form.cleaned_data['nachricht']
            form_submitted = True
            # form = None

            full_message = f"Von: {name}\nE-Mail: {email}\n\nNachricht:\n{nachricht}"

            #Send the Email
            email = EmailMessage(
                subject=f'Kontaktanfrage: {betreff}',
                body=f"Von: {name}\nE-Mail: {email}\n\nNachricht:\n{nachricht}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[settings.ADMIN_EMAIL],
                reply_to=[email], 
            )
            email.send(fail_silently=False)
            
            
    else:
        form = ContactForm()

    context = {
        'form_submitted': form_submitted,
        'form': form
    }

    return render(request, 'base/index.html', context)


def impressum(request):
    return render(request, 'base/impressum.html')    

def datenschutz(request):
    return render(request, 'base/datenschutz.html')