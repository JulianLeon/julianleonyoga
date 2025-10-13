const accordionHeaders = document.querySelectorAll('.accordion-header');
const accordionBodies = document.querySelectorAll('.accordion-body'); // Behalten wir für die Iteration

accordionHeaders.forEach(header => {
   
    header.addEventListener("click", () => {
        // Finde den übergeordneten Container, der den Body und den Header umschließt
        const accordionItem = header.closest('.accordion');
        if (!accordionItem) return; // Sicherheits-Check
        
        // Finde den Body innerhalb dieses Containers
        const bodyToToggle = accordionItem.querySelector('.accordion-body');
        
        // 1. Schließe alle anderen offenen Bodies
        accordionBodies.forEach(body => {
            if (body !== bodyToToggle && body.classList.contains('open')) {
                body.classList.remove('open');
                // Optional: Füge hier Logik hinzu, um das Icon zu drehen/ändern, falls nötig
            }
        });

        // 2. Toggle den Body, auf den geklickt wurde
        if (bodyToToggle) {
            bodyToToggle.classList.toggle('open');
        }
    });
});
