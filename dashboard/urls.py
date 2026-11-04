
from django.urls import path
from . import views

urlpatterns = [
    # Vista principal del dashboard (home general)
    path('', views.dashboard_home, name='dashboard_home'),

    # Vista de inicio con métricas desde Excel
    path('inicio/', views.inicio, name='inicio'),

    # Reporte mensual de ventas
    path('reporte-mensual/', views.reporte_mensual, name='reporte_mensual'),

    # Comparativos de métricas
    path('comparativo/', views.dashboard_comparativo, name='dashboard_comparativo'),

    # Exportar Excel físico (archivo original)
    path('exportar-excel/', views.exportar_excel, name='exportar_excel'),

    # Exportar ventas dinámicas desde Django
    path('exportar-ventas-excel/', views.exportar_ventas_excel, name='exportar_ventas_excel'),

    # Vista de sucursales
    path('sucursales/', views.sucursales, name='sucursales'),

    # Ranking de sucursales (Top Sucursales)
    path('sucursales/top/', views.top_sucursales, name='top_sucursales'),

    # -------------------------
    # Módulo CRM principal
    # -------------------------
    path('crm/modulo/', views.crm_modulo, name='crm_modulo'),

    # CRM Avanzado (herramientas de gestión avanzada)
    path('crm/avanzado/', views.crm_avanzado, name='crm_avanzado'),

    # CRM Ejecutivo (panel ejecutivo)
    path('crm/ejecutivo/', views.crm_ejecutivo, name='crm_ejecutivo'),

    # Submódulos CRM básicos
    path('crm/seguimiento/', views.crm_seguimiento_comercial, name='crm_seguimiento_comercial'),
    path('crm/desempeno/', views.crm_desempeno_vendedor, name='crm_desempeno_vendedor'),
    path('crm/segmentacion/', views.crm_segmentacion_clientes, name='crm_segmentacion_clientes'),

    # --- CRM Avanzado ---
    path('crm/pipeline/', views.crm_pipeline, name='crm_pipeline'),
    path('crm/notas/', views.crm_notas, name='crm_notas'),
    path('crm/recordatorios/', views.crm_recordatorios, name='crm_recordatorios'),
    path('crm/dashboard-gerencial/', views.crm_dashboard_gerencial, name='crm_dashboard_gerencial'),

    # --- CRM Ejecutivo ---
    path('crm/ejecutivo/nuevo-prospecto/', views.crm_nuevo_prospecto, name='crm_nuevo_prospecto'),
    path('crm/ejecutivo/pipeline/', views.crm_ejecutivo_pipeline, name='crm_ejecutivo_pipeline'),
    path('crm/ejecutivo/dashboard/', views.crm_ejecutivo_dashboard, name='crm_ejecutivo_dashboard'),
    path('crm/ejecutivo/score-clientes/', views.crm_score_clientes, name='crm_score_clientes'),
    path('crm/ejecutivo/alertas/', views.crm_alertas_inactividad, name='crm_alertas_inactividad'),
    path('crm/ejecutivo/prediccion/', views.crm_prediccion_ventas, name='crm_prediccion_ventas'),
    path('crm/ejecutivo/panel-rol/', views.crm_panel_por_rol, name='crm_panel_por_rol'),
    path('crm/ejecutivo/analitica-avanzada/', views.analitica_avanzada, name='crm_analitica_avanzada'),
]


