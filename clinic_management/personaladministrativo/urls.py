from django.urls import path
from . import views

urlpatterns = [
    path('home/personal_administrativo/',views.crear_paciente,name='home_personal_administrativo'),
    path('home/personal_administrativo/crear_paciente',views.crear_paciente,name='crear_paciente'),
    path('home/personal_administrativo/buscar_paciente',views.buscar_paciente,name='buscar_paciente'),
    path('home/personal_administrativo/actualizar_paciente/<str:numero_identificacion>/',views.actualizar_paciente,name='actualizar_paciente'),
    path('home/personal_administrativo/buscar_paciente_facturacion/',views.buscar_paciente_facturacion,name='buscar_paciente_facturacion'),
    path('home/personal_administrativo/generar_factura/<str:numero_identificacion>', views.generar_factura, name='generar_factura'),
    path('home/personal_administrativo/generar_factura/generar_pdf/<str:numero_identificacion>/<str:costo_bruto>/', views.generar_pdf_factura, name='generar_pdf_factura' ),
    
]