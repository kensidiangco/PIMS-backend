from django.urls import path
from . import views

urlpatterns = [
    #GET Req
    path('', views.getPouchesData),
    path('pouch/<int:id>/', views.getPouchData),
    path('pouch/inbounded/', views.getPouchInData),
    path('pouch/outbounded/', views.getPouchOutData),
    path('pouch/recent/outbounded/', views.pouch_out_today_latest),
    path('pouch/inbounded/<int:id>/', views.getInboundedPouchData),

    path('pouch/add/', views.addPouch),
    path('in/', views.pouchIn),
    path('out/', views.pouchOut),
    path('bulk/', views.bulk_create_pouches),

    path('pouch/paid/<int:id>/', views.markPouchAsPaid),
    path('update/<int:id>/', views.updateOutPouch),
    path('delete/<int:id>/', views.deleteOutPouch),
]
