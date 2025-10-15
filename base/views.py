from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.conf import settings
from contact.forms import ContactForm
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import CookieConsent

from anymail.exceptions import AnymailAPIError




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
                to=[settings.DEFAULT_FROM_EMAIL],
                reply_to=[email], 
            )
            email.send(fail_silently=False)
            
            return redirect('/?sent=true')
            
    else:
        form = ContactForm()

    form_submitted = request.GET.get('sent') == 'true'

    context = {
        'form_submitted': form_submitted,
        'form': form
    }

    return render(request, 'base/index.html', context)


def impressum(request):
    return render(request, 'base/impressum.html')    

def datenschutz(request):
    return render(request, 'base/datenschutz.html')





@require_http_methods(["POST"])
@csrf_exempt
def save_cookie_consent(request):
    try:
        # Versuch, den JSON-Body zu parsen
        data = json.loads(request.body)
        analytics_consent = data.get('analytics', False)
        
        # ... Rest deiner Logik zum Speichern in der DB und Session ...
        session_key = request.session.session_key
        if not session_key:
            request.session.create()
            session_key = request.session.session_key
        
        consent, created = CookieConsent.objects.update_or_create(
            session_key=session_key,
            defaults={'analytics_consent': analytics_consent}
        )
        
        return JsonResponse({
            'status': 'success',
            'analytics': consent.analytics_consent
        }, status=200) # <- Gib explizit 200 zurück
    
    except json.JSONDecodeError:
        # Fängt den Fall ab, dass der Body LEER ist oder kein gültiges JSON
        # Dies ist der Grund für deinen 400er.
        # Wir geben eine spezifische Fehlermeldung, behalten aber den 400er, da der Client-Body fehlerhaft ist.
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid or empty JSON body received.'
        }, status=400)
        
    except Exception as e:
        # Fängt alle ANDEREN internen Fehler (Datenbank, Session-Probleme etc.) ab
        # Wir geben einen 500er zurück, da der Fehler auf der Serverseite liegt.
        print(f"Internal Server Error in cookie consent: {e}") # Logge den Fehler für Debugging
        return JsonResponse({
            'status': 'error',
            'message': 'Internal Server Error during consent processing.'
        }, status=500)