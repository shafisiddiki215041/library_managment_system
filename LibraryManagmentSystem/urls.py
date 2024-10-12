from django.contrib import admin
from django.urls import path,  include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/',include('user.urls')),
    path('books/',include('books.urls')),
    path('homepage/',views.home, name=
    "homepage"),
    path('category/<slug:category_slug>/', views.home, name='categories_wise_show'),
    path('show_all/', views.home, name='show_all'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)