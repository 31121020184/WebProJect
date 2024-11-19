from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('Store.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('analysis/', include('analysis.urls', namespace='analysis')),
    path('orders/', include('orders.urls', namespace='orders')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
