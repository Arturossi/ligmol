from django.urls import path

from . import views

app_name = 'complexTable'

# Patterns which leads to a page
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('complexTable', views.ComplexView.as_view(), name='complexTable'),
    path('detailedInfo', views.DetailedView.as_view(), name='detailedInfo'),
]

# Patterns which leads to download
downloadpatterns = [
    path('download', views.download, name='download'),
    path('downloadFiles', views.downloadFiles, name='downloadFiles'),
]

# Patterns to work with ajax
ajaxpatterns =[
    path('hist_post', views.hist_post, name='hist_post'),
]

# Pattern to be used with 2dmap (generate figures on the fly)
twodmappatterns = [
    path('simple.png', views.simplePlot, name='simple2Dmap'),
    path('runningAvg.png', views.runningAvg, name='runningAvg2Dmap'),
    path('heatMap.png', views.heatMap, name='heatMap2Dmap'),
    path('distribStrip.png', views.distribStrip, name='distribStrip2Dmap'),
    path('distribBox.png', views.distribBox, name='distribBox2Dmap'),
    path('distribViolin.png', views.distribViolin, name='distribViolin2Dmap'),
    path('facetGrids.png', views.facetGrids, name='facetGrids2Dmap'),
]

# Concatenate all lists
urlpatterns += downloadpatterns
urlpatterns += ajaxpatterns
urlpatterns += twodmappatterns