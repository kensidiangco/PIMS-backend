from django.urls import path
from . import views

urlpatterns = [
    #GET Req
    path('', views.getPouchesData),
    path('pouch/<int:id>/', views.getPouchData),
    path('inlog/', views.getPouchInData),
    path('outlog/', views.getPouchOutData),
    path('latestlog/', views.pouch_out_today_latest),

    path('pouch/add/', views.addPouch),
    path('in/', views.pouchIn),
    path('out/', views.pouchOut),
    path('bulk/', views.bulk_create_pouches),

    path('update/<int:id>/', views.updateOutPouch),
    path('delete/<int:id>/', views.deleteOutPouch),
]
