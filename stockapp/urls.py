from django.urls import path
from . import views

urlpatterns = [
    path('',views.stockPicker,name='stockpicker'),
    path('stoctracker/',views.stockTracker,name='stocktracker'),

]