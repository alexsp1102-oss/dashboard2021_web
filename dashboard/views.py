from pathlib import Path
import json
import pandas as pd
from django.http import HttpResponse, FileResponse
from django.shortcuts import render
from openpyxl import Workbook

# Ruta del archivo Excel
EXCEL_PATH = r"C:\Users\a1exs\Downloads\Dashboard2021_50000_registros (1).xlsx"

# -------------------------
# Vistas principales
# -------------------------

def dashboard_home(request):
    return render(request, 'dashboard/home.html')

def inicio(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    total_ventas = df['Ventas'].sum()
    total_documentos = len(df)
    ticket_promedio = total_ventas / total_documentos if total_documentos > 0 else 0
    venta_maxima = df['Ventas'].max()
    productos_vendidos = df['Cantidad'].sum()
    metodos_usados = df['Forma de pago'].nunique()

    ventas_por_metodo = (
        df.groupby('Forma de pago')['Ventas']
        .sum().reset_index().sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )
    ventas_por_vendedor = (
        df.groupby('Vendedor')['Ventas']
        .sum().reset_index().sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )
    productos_mas_vendidos = (
        df.groupby('Producto')['Cantidad']
        .sum().reset_index().sort_values(by='Cantidad', ascending=False)
        .head(10).to_dict(orient='records')
    )
    ventas_por_categoria = (
        df.groupby('Categoría')['Ventas']
        .sum().reset_index().sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    contexto = {
        'total_ventas': total_ventas,
        'total_documentos': total_documentos,
        'ticket_promedio': ticket_promedio,
        'venta_maxima': venta_maxima,
        'productos_vendidos': productos_vendidos,
        'metodos_usados': metodos_usados,
        'ventas_por_metodo_json': json.dumps(ventas_por_metodo, default=str),
        'ventas_por_vendedor_json': json.dumps(ventas_por_vendedor, default=str),
        'productos_mas_vendidos_json': json.dumps(productos_mas_vendidos, default=str),
        'ventas_por_categoria_json': json.dumps(ventas_por_categoria, default=str),
    }
    return render(request, 'dashboard/inicio.html', contexto)

def ventas_listado(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    ventas = df.to_dict(orient='records')
    return render(request, 'dashboard/ventas_listado.html', {'ventas': ventas})

def reporte_mensual(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip().str.lower()

    df['ventas'] = pd.to_numeric(df['ventas'], errors='coerce').fillna(0)
    df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')
    df['mes'] = df['fecha'].dt.strftime('%B %Y')

    datos = (
        df.groupby('mes')
        .agg(
            total_ventas=('ventas', 'sum'),
            total_documentos=('documento', 'count')
        )
        .reset_index()
        .sort_values(by='mes')
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/reporte_mensual.html', {'datos': datos})

def dashboard_comparativo(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip().str.lower()
    df['ventas'] = pd.to_numeric(df['ventas'], errors='coerce').fillna(0)

    comparativo_categorias = (
        df.groupby('categoría')['ventas']
        .sum().reset_index().sort_values(by='ventas', ascending=False)
        .rename(columns={'categoría': 'categoria', 'ventas': 'total'})
        .to_dict(orient='records')
    )
    comparativo_ciudades = (
        df.groupby('ciudad')['ventas']
        .sum().reset_index().sort_values(by='ventas', ascending=False)
        .rename(columns={'ciudad': 'ciudad', 'ventas': 'total'})
        .to_dict(orient='records')
    )
    comparativo_metodos = (
        df.groupby('forma de pago')['ventas']
        .sum().reset_index().sort_values(by='ventas', ascending=False)
        .rename(columns={'forma de pago': 'metodo_pago', 'ventas': 'total'})
        .to_dict(orient='records')
    )

    contexto = {
        'comparativo_categorias': comparativo_categorias,
        'comparativo_ciudades': comparativo_ciudades,
        'comparativo_metodos': comparativo_metodos,
    }
    return render(request, 'dashboard/comparativo.html', contexto)

def exportar_excel(request):
    archivo = Path(EXCEL_PATH)
    return FileResponse(open(archivo, 'rb'), as_attachment=True,
                        filename='Dashboard2021_50000_registros.xlsx')

def exportar_ventas_excel(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip().str.lower()
    df['ventas'] = pd.to_numeric(df['ventas'], errors='coerce').fillna(0)

    wb = Workbook()
    ws = wb.active
    ws.title = 'Ventas'
    ws.append(['documento', 'fecha', 'cliente', 'ciudad', 'vendedor',
               'forma de pago', 'producto', 'categoría', 'precio',
               'cantidad', 'ventas', 'moneda'])

    for _, row in df.iterrows():
        ws.append([
            row['documento'], str(row['fecha']), row['cliente'], row['ciudad'],
            row['vendedor'], row['forma de pago'], row['producto'],
            row['categoría'], float(row['precio']), int(row['cantidad']),
            float(row['ventas']), row['moneda']
        ])

    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=ventas_exportadas.xlsx'
    wb.save(response)
    return response

def sucursales(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    sucursales = (
        df.groupby(['Ciudad', 'Provincia'])['Ventas']
        .sum().reset_index().sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/sucursales.html', {'sucursales': sucursales})

# -------------------------
# Nuevas vistas CRM
# -------------------------

def crm_modulo(request):
    return render(request, 'dashboard/crm/crm_modulo.html')

def crm_avanzado(request):
    return render(request, 'dashboard/crm/crm_avanzado.html')

def crm_ejecutivo(request):
    return render(request, 'dashboard/crm/crm_ejecutivo.html')







  # --- Submódulos del Módulo CRM ---
def crm_seguimiento_comercial(request):
    # Leer el Excel
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir la columna Ventas a número
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Agrupar ventas por vendedor
    ventas_por_vendedor = (
        df.groupby('Vendedor')['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    # Renderizar el template con los datos
    return render(request, 'dashboard/crm/crm_seguimiento_comercial.html', {
        'ventas_por_vendedor': ventas_por_vendedor
    })


def crm_desempeno_vendedor(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    desempeño = (
        df.groupby(['Vendedor', 'Ciudad'])['Ventas']
        .sum().reset_index().sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/crm_desempeno_vendedor.html', {
        'desempeno': desempeño
    })


def crm_segmentacion_clientes(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    clientes_segmentados = (
        df.groupby('Cliente')['Ventas']
        .sum().reset_index().sort_values(by='Ventas', ascending=False)
        .head(20).to_dict(orient='records')
    )

    return render(request, 'dashboard/crm_segmentacion_clientes.html', {
        'clientes_segmentados': clientes_segmentados
    })
  
def crm_desempeno_vendedor(request):
    # Leer el Excel
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir la columna Ventas a número
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Agrupar ventas por vendedor y ciudad
    desempeno = (
        df.groupby(['Vendedor', 'Ciudad'])['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    # Renderizar el template con los datos
    return render(request, 'dashboard/crm/crm_desempeno_vendedor.html', {
        'desempeno': desempeno
    })

def crm_segmentacion_clientes(request):
    # Leer el Excel
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir la columna Ventas a número
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Agrupar ventas por cliente
    clientes_segmentados = (
        df.groupby('Cliente')['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    # Top 10 clientes con mayor volumen de ventas
    top_clientes = clientes_segmentados[:10]

    return render(request, 'dashboard/crm/crm_segmentacion_clientes.html', {
        'clientes_segmentados': clientes_segmentados,
        'top_clientes': top_clientes
    })

def crm_avanzado(request):
    return render(request, 'dashboard/crm/crm_avanzado.html')

# --- Pipeline de prospectos ---
def crm_pipeline(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Filtrar prospectos activos
    prospectos = df[df['Estado'] == 'Prospecto'][['Cliente', 'Vendedor', 'Ciudad', 'Ventas']].to_dict(orient='records')

    return render(request, 'dashboard/crm/crm_pipeline.html', {'prospectos': prospectos})


# --- Notas CRM ---
def crm_notas(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Simulación de notas comerciales agrupadas por vendedor
    notas = (
        df.groupby('Vendedor')['Notas']
        .apply(lambda x: ', '.join(x.dropna().unique()))
        .reset_index()
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/crm/crm_notas.html', {'notas': notas})


# --- Recordatorios CRM ---
def crm_recordatorios(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Filtrar recordatorios próximos
    recordatorios = df[df['Tipo'] == 'Recordatorio'][['Cliente', 'Fecha', 'Comentario']].to_dict(orient='records')

    return render(request, 'dashboard/crm/crm_recordatorios.html', {'recordatorios': recordatorios})


# --- Dashboard gerencial ---
def crm_dashboard_gerencial(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    resumen = {
        'total_ventas': df['Ventas'].sum(),
        'promedio_ventas': df['Ventas'].mean(),
        'total_clientes': df['Cliente'].nunique(),
        'total_vendedores': df['Vendedor'].nunique(),
    }

    return render(request, 'dashboard/crm/crm_dashboard_gerencial.html', {'resumen': resumen})


def crm_pipeline(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Pipeline: todos los clientes con sus ventas
    pipeline = (
        df[['Cliente', 'Vendedor', 'Ciudad', 'Ventas']]
        .sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    resumen = {
        'total_clientes': df['Cliente'].nunique(),
        'ventas_totales': df['Ventas'].sum(),
    }

    return render(request, 'dashboard/crm/crm_pipeline.html', {
        'pipeline': pipeline,
        'resumen': resumen
    })


def crm_notas(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Agrupar productos vendidos por cada vendedor como "notas"
    notas = (
        df.groupby('Vendedor')['Producto']
        .apply(lambda x: ', '.join(x.dropna().unique()))
        .reset_index()
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/crm/crm_notas.html', {
        'notas': notas
    })

def crm_recordatorios(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir la columna Fecha a tipo datetime
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    # Seleccionar columnas relevantes como recordatorios
    recordatorios = (
        df[['Fecha', 'Cliente', 'Vendedor', 'Producto', 'Ventas']]
        .sort_values(by='Fecha', ascending=True)
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/crm/crm_recordatorios.html', {
        'recordatorios': recordatorios
    })

def crm_dashboard_gerencial(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    resumen = {
        'total_ventas': df['Ventas'].sum(),
        'promedio_ventas': df['Ventas'].mean(),
        'total_clientes': df['Cliente'].nunique(),
        'total_vendedores': df['Vendedor'].nunique(),
        'total_documentos': df['Documento'].nunique(),
    }

    return render(request, 'dashboard/crm/crm_dashboard_gerencial.html', {
        'resumen': resumen
    })
#puede que no sirva esto 
def crm_ejecutivo(request):
    return render(request, 'dashboard/crm/crm_ejecutivo.html')


# --- CRM Ejecutivo ---
def crm_nuevo_prospecto(request):
    return render(request, 'dashboard/crm/crm_nuevo_prospecto.html')

def crm_ejecutivo_pipeline(request):
    return render(request, 'dashboard/crm/crm_ejecutivo_pipeline.html')

def crm_ejecutivo_dashboard(request):
    return render(request, 'dashboard/crm/crm_ejecutivo_dashboard.html')

def crm_score_clientes(request):
    return render(request, 'dashboard/crm/crm_score_clientes.html')

def crm_alertas_inactividad(request):
    return render(request, 'dashboard/crm/crm_alertas_inactividad.html')

def crm_prediccion_ventas(request):
    return render(request, 'dashboard/crm/crm_prediccion_ventas.html')

def crm_panel_por_rol(request):
    return render(request, 'dashboard/crm/crm_panel_por_rol.html')


#funciones de  los botones de crm ejecutivo 
def crm_nuevo_prospecto(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir ventas a número
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Tomar los últimos 10 registros como prospectos nuevos
    prospectos = df.tail(10).to_dict(orient='records')

    return render(request, 'dashboard/crm/crm_nuevo_prospecto.html', {
        'prospectos': prospectos
    })
def crm_ejecutivo_pipeline(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir ventas a número
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Pipeline: clientes con ventas ordenadas
    pipeline = (
        df[['Cliente', 'Vendedor', 'Ciudad', 'Ventas']]
        .sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    # Resumen general
    resumen = {
        'total_clientes': df['Cliente'].nunique(),
        'total_vendedores': df['Vendedor'].nunique(),
        'ventas_totales': df['Ventas'].sum(),
    }

    return render(request, 'dashboard/crm/crm_ejecutivo_pipeline.html', {
        'pipeline': pipeline,
        'resumen': resumen
    })
def crm_ejecutivo_dashboard(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    resumen = {
        'total_ventas': df['Ventas'].sum(),
        'promedio_ventas': df['Ventas'].mean(),
        'total_clientes': df['Cliente'].nunique(),
        'total_vendedores': df['Vendedor'].nunique(),
        'total_documentos': df['Documento'].nunique(),
    }

    return render(request, 'dashboard/crm/crm_ejecutivo_dashboard.html', {
        'resumen': resumen
    })

def crm_score_clientes(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir ventas a número
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Calcular score: total de ventas por cliente
    score = (
        df.groupby('Cliente')['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    # Top 10 clientes
    top_clientes = score[:10]

    return render(request, 'dashboard/crm/crm_score_clientes.html', {
        'score': score,
        'top_clientes': top_clientes
    })
def crm_alertas_inactividad(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')

    limite = pd.Timestamp.today() - pd.Timedelta(days=90)

    inactivos = (
        df[df['Fecha'] < limite][['Cliente', 'Vendedor', 'Fecha']]
        .drop_duplicates(subset=['Cliente'])
        .sort_values(by='Fecha', ascending=True)
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/crm/crm_alertas_inactividad.html', {
        'inactivos': inactivos,
        'limite': limite
    })


def crm_prediccion_ventas(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir columnas
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)
 
    # Agrupar ventas por mes
    tendencia = (
        df.groupby(df['Fecha'].dt.to_period('M'))['Ventas']
        .sum()
        .reset_index()
    )
    tendencia['Fecha'] = tendencia['Fecha'].astype(str)

    # Calcular promedio mensual como "predicción simple"
    promedio_mensual = tendencia['Ventas'].mean()

    return render(request, 'dashboard/crm/crm_prediccion_ventas.html', {
        'tendencia': tendencia.to_dict(orient='records'),
        'promedio_mensual': promedio_mensual
    })
def crm_panel_por_rol(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()

    # Convertir ventas a número
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Agrupar ventas por vendedor (rol comercial)
    panel = (
        df.groupby('Vendedor')['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
        .to_dict(orient='records')
    )

    return render(request, 'dashboard/crm/crm_panel_por_rol.html', {
        'panel': panel
    }
    )

def analitica_avanzada(request):
    df = pd.read_excel(EXCEL_PATH)
    df.columns = df.columns.str.strip()
    df.columns = df.columns.str.replace(' ', '_')

    # Conversión de tipos
    df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
    df['Ventas'] = pd.to_numeric(df['Ventas'], errors='coerce').fillna(0)

    # Filtros desde GET
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    moneda = request.GET.get('moneda', 'MXN')
    cliente = request.GET.getlist('cliente')
    vendedor = request.GET.getlist('vendedor')
    categoria = request.GET.getlist('categoria')
    metodo = request.GET.getlist('metodo')

    if fecha_inicio:
        df = df[df['Fecha'] >= pd.to_datetime(fecha_inicio, dayfirst=True)]
    if fecha_fin:
        df = df[df['Fecha'] <= pd.to_datetime(fecha_fin, dayfirst=True)]
    if cliente:
        df = df[df['Cliente'].isin(cliente)]
    if vendedor:
        df = df[df['Vendedor'].isin(vendedor)]
    if categoria:
        df = df[df['Categoría'].isin(categoria)]
    if metodo:
        df = df[df['Forma_de_pago'].isin(metodo)]

    # Conversión de moneda (ejemplo con tasas fijas, puedes ajustarlas)
    tasas = {'MXN': 1, 'USD': 0.056, 'EUR': 0.052, 'ARS': 50, 'CAD': 0.075}
    tasa = tasas.get(moneda, 1)

    # Métricas globales
    total_registros = len(df)
    monto_total = (df['Ventas'].sum()) * tasa
    promedio = (df['Ventas'].mean()) * tasa
    maximo = (df['Ventas'].max()) * tasa

    # Tendencia mensual
    tendencia = (
        df.groupby(df['Fecha'].dt.to_period('M'))['Ventas']
        .sum()
        .reset_index()
    )
    tendencia['Fecha'] = tendencia['Fecha'].astype(str)
    tendencia['Ventas'] = tendencia['Ventas'] * tasa

    # Estacionalidad promedio
    estacionalidad = (
        df.groupby(df['Fecha'].dt.month)['Ventas']
        .mean()
        .reset_index()
    )
    estacionalidad['Ventas'] = estacionalidad['Ventas'] * tasa

    # Top vendedores
    top_vendedores = (
        df.groupby('Vendedor')['Ventas']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .head(5)
    )

    # Top sucursales
    top_sucursales = (
        df.groupby('Ciudad')['Ventas']
        .sum()
        .sort_values(ascending=False)
        .reset_index()
        .head(5)
    )

    # Proyección por categoría
    proyeccion_categoria = (
        df.groupby('Categoría')['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
    )

    # Proyección por método de pago
    proyeccion_metodos = (
        df.groupby('Forma_de_pago')['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
    )

    # Hallazgos automáticos
    cliente_top = df.groupby('Cliente')['Ventas'].sum().idxmax()
    cliente_top_valor = df.groupby('Cliente')['Ventas'].sum().max()

    vendedor_min = df.groupby('Vendedor')['Ventas'].sum().idxmin()
    vendedor_min_valor = df.groupby('Vendedor')['Ventas'].sum().min()

    categoria_top = proyeccion_categoria.iloc[0]['Categoría']
    categoria_top_valor = proyeccion_categoria.iloc[0]['Ventas']

    metodo_top = proyeccion_metodos.iloc[0]['Forma_de_pago']
    metodo_top_valor = proyeccion_metodos.iloc[0]['Ventas']

    mes_min = df.groupby(df['Fecha'].dt.month)['Ventas'].mean().idxmin()
    mes_min_valor = df.groupby(df['Fecha'].dt.month)['Ventas'].mean().min()

    contexto = {
        'total_registros': total_registros,
        'monto_total': monto_total,
        'promedio': promedio,
        'maximo': maximo,
        'tendencia': tendencia.to_dict(orient='records'),
        'estacionalidad': estacionalidad.to_dict(orient='records'),
        'moneda': moneda,
        'clientes': df['Cliente'].unique(),
        'vendedores': df['Vendedor'].unique(),
        'categorias': df['Categoría'].unique(),
        'metodos': df['Forma_de_pago'].unique(),
        'top_vendedores': top_vendedores.to_dict(orient='records'),
        'top_sucursales': top_sucursales.to_dict(orient='records'),
        'proyeccion_categoria': proyeccion_categoria.to_dict(orient='records'),
        'proyeccion_metodos': proyeccion_metodos.to_dict(orient='records'),
        'cliente_top': cliente_top,
        'cliente_top_valor': cliente_top_valor,
        'vendedor_min': vendedor_min,
        'vendedor_min_valor': vendedor_min_valor,
        'categoria_top': categoria_top,
        'categoria_top_valor': categoria_top_valor,
        'metodo_top': metodo_top,
        'metodo_top_valor': metodo_top_valor,
        'mes_min': mes_min,
        'mes_min_valor': mes_min_valor,
    }

    return render(request, 'dashboard/crm/crm_analitica_avanzada.html', contexto)

#este codigo puede que no funcione 


def top_sucursales(request):
    # Leer el archivo Excel
    df = pd.read_excel('Dashboard2021_50000_registros (1).xlsx')

    # Agrupar por sucursal y sumar ventas
    ranking = (
        df.groupby('Sucursal')['Ventas']
        .sum()
        .reset_index()
        .sort_values(by='Ventas', ascending=False)
        .head(10)  # Top 10
    )

    contexto = {
        'ranking': ranking.to_dict(orient='records')
    }
    return render(request, 'crm/top_sucursales.html', contexto)

