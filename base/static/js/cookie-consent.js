        // Cookie Helper Functions
        function setCookie(name, value, days) {
            const d = new Date();
            d.setTime(d.getTime() + (days * 24 * 60 * 60 * 1000));
            document.cookie = name + "=" + value + ";expires=" + d.toUTCString() + ";path=/;SameSite=Lax";
        }

        function getCookie(name) {
            const nameEQ = name + "=";
            const ca = document.cookie.split(';');
            for(let i = 0; i < ca.length; i++) {
                let c = ca[i];
                while (c.charAt(0) === ' ') c = c.substring(1, c.length);
                if (c.indexOf(nameEQ) === 0) return c.substring(nameEQ.length, c.length);
            }
            return null;
        }

        // Load Google Analytics only if consent given
        function loadGoogleAnalytics() {
            if (window.gtag) return; // Already loaded
            
            const script1 = document.createElement('script');
            script1.async = true;
            script1.src = 'https://www.googletagmanager.com/gtag/js?id=G-BYLS2Y2N5T';
            document.head.appendChild(script1);

            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            window.gtag = gtag;
            gtag('js', new Date());
            gtag('config', 'G-BYLS2Y2N5T', {
                'anonymize_ip': true
            });
            
            console.log('Google Analytics geladen');
        }

        // Save consent to backend
        function saveConsentToBackend(analyticsConsent) {

            const csrftoken = getCookie('csrftoken');

            fetch('/api/cookie-consent/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': csrftoken
                },
                body: JSON.stringify({
                    analytics: analyticsConsent
                })
            })
            .then(response => response.json())
            .then(data => console.log('Consent gespeichert:', data))
            .catch(error => console.error('Fehler beim Speichern:', error));
        }

        // Accept all cookies
        function acceptAllCookies() {
            setCookie('cookie_consent', 'all', 365);
            setCookie('analytics_consent', 'true', 365);
            loadGoogleAnalytics();
            saveConsentToBackend(true);
            hideBanner();
        }

        // Reject all (only necessary)
        function rejectAllCookies() {
            setCookie('cookie_consent', 'necessary', 365);
            setCookie('analytics_consent', 'false', 365);
            saveConsentToBackend(false);
            hideBanner();
        }

        // Open settings modal
        function openCookieSettings() {
            document.getElementById('cookie-settings-modal').classList.add('show');
            const analyticsConsent = getCookie('analytics_consent') === 'true';
            document.getElementById('analytics-toggle').checked = analyticsConsent;
        }

        // Close settings modal
        function closeCookieSettings() {
            document.getElementById('cookie-settings-modal').classList.remove('show');
        }

        // Save custom settings
        function saveCustomSettings() {
            const analyticsEnabled = document.getElementById('analytics-toggle').checked;
            
            setCookie('cookie_consent', 'custom', 365);
            setCookie('analytics_consent', analyticsEnabled.toString(), 365);
            
            if (analyticsEnabled) {
                loadGoogleAnalytics();
            }
            
            saveConsentToBackend(analyticsEnabled);
            closeCookieSettings();
            hideBanner();
        }

        // Hide banner
        function hideBanner() {
            document.getElementById('cookie-banner').classList.remove('show');
        }

        // Check consent on page load
        function checkCookieConsent() {
            const consent = getCookie('cookie_consent');
            
            if (!consent) {
                // Show banner if no consent yet
                document.getElementById('cookie-banner').classList.add('show');
            } else {
                // Load analytics if previously consented
                const analyticsConsent = getCookie('analytics_consent') === 'true';
                if (analyticsConsent) {
                    loadGoogleAnalytics();
                }
            }
        }

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', checkCookieConsent);
