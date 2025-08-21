from django.urls import path
from . import views

urlpatterns = [
    #GET Req
    path('', views.getPouchData),
    path('inlog/', views.getPouchInData),
    path('outlog/', views.getPouchOutData),
    path('latestlog', views.pouch_out_today_latest),

    #POST Req
    path('pouch/add/', views.addPouch),
    path('in/', views.pouchIn),
    path('out/', views.pouchOut),

    #PUT Req
    path('update/', views.updateOutPouch),
]
