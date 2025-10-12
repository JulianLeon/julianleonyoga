import mistune
from django.utils.safestring import mark_safe
import re
from mistune.plugins.formatting import strikethrough
from mistune.plugins.table import table
from mistune.plugins.footnotes import footnotes
from mistune.plugins.task_lists import task_lists





class CloudinaryRenderer(mistune.HTMLRenderer):
    def image(self, alt, url, title=None):  # <-- ANGEPASSTE SIGNATUR
        # Wir nennen die Variable intern 'src', weil der Rest des Codes das erwartet
        src = url 
        
        # Prüfen, ob Cloudinary-URL, Transformationen hinzufügen
        if 'cloudinary.com' in src and '/upload/' in src:
            src = src.replace('/upload/', '/upload/f_auto,q_auto/')

        if title:
            return f'''<figure class="markdown-image">
                <img src="{src}" alt="{alt}" loading="lazy">
                <figcaption>{title}</figcaption>
            </figure>'''
        else:
            return f'<img src="{src}" alt="{alt}" loading="lazy">'
    
    def block_code(self, code, info=None):
        """Syntax Highlighting für Code Blöcke"""
        if info:
            return f'<pre><code class="language-{info}">{mistune.escape(code)}</code></pre>'
        return f'<pre><code>{mistune.escape(code)}</code></pre>'


def markdownify(text):
    """
    Konvertiert Markdown zu HTML mit Mistune
    Diese Funktion wird von django-markdownx aufgerufen
    """
    if not text:
        return ''
    
    renderer = CloudinaryRenderer()
    markdown_parser = mistune.Markdown(
        renderer=renderer,
        plugins=[
            table,
            strikethrough,
            footnotes,
            task_lists,
        ]
    )
    
    html = markdown_parser(text)
    return mark_safe(html)
