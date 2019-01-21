from django.urls import path

from . import views

app_name = 'complexTable'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('complexTable/', views.ComplexView.as_view(), name='complexTable'),
    path('detailedInfo', views.DetailedView.as_view(), name='detailedInfo'),
    path('download', views.download, name='download'),
    #path('<int:pk>/results/', views.ResultsView.as_view(), name='results'),
    #path('<int:question_id>/vote/', views.vote, name='vote'),
]