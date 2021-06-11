from django.urls import path, re_path
from django.conf.urls.static import static
from app import views
from core import settings

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('authors', views.authors, name='authors'),
    path('demo', views.authors, name='demo'),
    path('git', views.git, name='git'),
    path('start', views.start, name='start'),
    path('uploadcsv', views.uploadcsv, name='uploadcsv'),
    path('preprocess', views.preprocessing, name='preprocessing'),
    path('showPreprocess', views.showPreprocess, name='showpreprocess'),
    path('classify', views.classify, name='classify'),
    path('download/<int:idx>/', views.download, name='download'),
    re_path(r'^.*\.html', views.pages, name='pages'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
