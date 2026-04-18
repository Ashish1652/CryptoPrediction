from django.urls import path,include
from . import views
urlpatterns = [

    path('',views.index),
    path('about', views.about, name='about'),
    path('create',views.displayform, name='create'),
    path('AddGuestPost',views.addGuestPost, name='AddGuestPost'),
    path('add_blog',views.add_blog, name='add_blog'),
    path('display_blog', views.display_blog, name = 'display_blog'),
    path('/prediction/', views.prediction, name='prediction'),
    path('bitcoin/', views.bitcoin, name='bitcoin'),
    path('dogecoin/', views.dogecoin, name = 'dogecoin'),
    path('binance/',views.binance, name = 'binance'),
    path('polkadot/',views.polkadot, name='polkadot'),
    path('tether/',views.tether,name = 'tether'),
    path('ethereum/',views.ethereum,name='ethereum')


]
