from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from .models import Post, Category
##Für Markdown
import os
import json
import cloudinary.uploader
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.views import View
from django.core.files.uploadedfile import InMemoryUploadedFile
import io

# Pillow imports - KORRIGIERT
try:
    from PIL import Image, ImageFile
    ImageFile.LOAD_TRUNCATED_IMAGES = True  # Für beschädigte Bilder
    PILLOW_AVAILABLE = True
except ImportError:
    print("⚠️ Pillow not installed. Install with: pip install Pillow")
    PILLOW_AVAILABLE = False


# Create your views here.
@method_decorator(csrf_exempt, name='dispatch')
class CloudinaryImageUploadView(View):
    """Upload View mit automatischer Bildverkleinerung"""
    
    def post(self, request, *args, **kwargs):
        print("=== CLOUDINARY UPLOAD DEBUG ===")
        print(f"User authenticated: {request.user.is_authenticated}")
        print(f"Files received: {list(request.FILES.keys())}")
        
        if not request.user.is_authenticated:
            return JsonResponse({'error': 'Authentication required'}, status=403)
        
        image_file = request.FILES.get('markdownx-image-file')
        
        if not image_file:
            return JsonResponse({'error': 'No image file found'}, status=400)
        
        print(f"Original image: {image_file.name}, Size: {image_file.size} bytes")
        
        try:
            # Verkleinere das Bild automatisch
            compressed_image = self.compress_image(image_file)
            print(f"Compressed image size: {compressed_image.size} bytes")
            
            # Upload zu Cloudinary
            upload_result = cloudinary.uploader.upload(
                compressed_image,
                folder="blog_images",
                # Zusätzliche Cloudinary-Transformationen
                transformation=[
                    {'quality': 'auto:good'},  # Automatische Qualitäts-Optimierung
                    {'format': 'auto'},        # Bestes Format wählen (WebP, etc.)
                    {'width': 1200, 'crop': 'limit'},  # Max. Breite 1200px
                ],
                resource_type="auto"
            )
            
            print(f"✓ Upload successful: {upload_result['secure_url']}")
            
            return JsonResponse({
                'image_url': upload_result['secure_url'],
            })
            
        except Exception as e:
            print(f"✗ Upload failed: {str(e)}")
            return JsonResponse({
                'error': f'Upload failed: {str(e)}'
            }, status=500)
    
    def compress_image(self, image_file, max_size_mb=8, quality=85, max_width=1920):
        """
        Verkleinere Bild auf unter max_size_mb MB
        """
        # Öffne das Bild
        img = Image.open(image_file)
        
        # Konvertiere RGBA zu RGB falls nötig (für JPEG)
        if img.mode in ('RGBA', 'LA', 'P'):
            background = Image.new('RGB', img.size, (255, 255, 255))
            if img.mode == 'P':
                img = img.convert('RGBA')
            background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
            img = background
        
        # Verkleinere die Abmessungen falls nötig
        if img.width > max_width:
            ratio = max_width / img.width
            new_height = int(img.height * ratio)
            img = img.resize((max_width, new_height), Image.Resampling.LANCZOS)
            print(f"Resized to: {img.width}x{img.height}")
        
        # Speichere in verschiedenen Qualitätsstufen bis Dateigröße passt
        for quality_level in [quality, 75, 60, 45, 30]:
            output = io.BytesIO()
            
            # Format bestimmen
            format_type = 'JPEG'  # Standardmäßig JPEG für kleinere Dateien
            if image_file.name.lower().endswith('.png') and quality_level >= 75:
                format_type = 'PNG'
            
            img.save(output, format=format_type, quality=quality_level, optimize=True)
            
            output_size = output.tell()
            max_size_bytes = max_size_mb * 1024 * 1024
            
            print(f"Quality {quality_level}, Format {format_type}: {output_size} bytes")
            
            if output_size <= max_size_bytes:
                output.seek(0)
                
                # Erstelle eine neue InMemoryUploadedFile
                compressed_file = InMemoryUploadedFile(
                    output,
                    'ImageField',
                    f"{os.path.splitext(image_file.name)[0]}.{format_type.lower()}",
                    f'image/{format_type.lower()}',
                    output_size,
                    None
                )
                
                return compressed_file
        
        # Falls auch mit niedrigster Qualität zu groß, verwende die letzte Version
        output.seek(0)
        return InMemoryUploadedFile(
            output,
            'ImageField',
            f"{os.path.splitext(image_file.name)[0]}.jpg",
            'image/jpeg',
            output.tell(),
            None
        )



def blog(request):
    posts = Post.objects.all()[:3]
    categories = Category.objects.all()

    return render(request, 'blog/index.html', {
        "posts": posts,
        "categories": categories
    })

def post_detail(request, slug):
    categories = Category.objects.all()
    post = Post.objects.get(slug=slug)

    return render(request, 'blog/post_detail.html', {
        "post": post,
        "categories": categories
    })

def category(request, category_slug):
    category = Category.objects.get(slug=category_slug)
    categories = Category.objects.all().exclude(slug=category_slug)
    posts = category.posts.all()
    if posts.exists():
        return render(request, 'blog/category.html', {
            "posts": posts,
            "category": category,
            "categories": categories
        })
    else:
        return render(request, 'blog/category.html', {
            "message": f'Keine Beiträge in {category}.',
            "category": category,
            "categories": categories
        })

    


def search(request):
    categories = Category.objects.all()
    query = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(title__icontains=query) |
        Q(body__icontains=query)
    )
    if posts.exists():
        return render(request, 'blog/search.html', {
            "posts": posts,
            "categories": categories
        })
    else: 
        return render(request, 'blog/search.html', {
            "message": f"Keine Ergebnisse gefunden für {query}.",
            "categories": categories
        })
                            
    

