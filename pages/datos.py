import dash
from dash import html, dcc
import pandas as pd
import plotly.express as px
from pathlib import Path

dash.register_page(__name__,path="/datos",name="Datos")
p=Path(__file__).resolve().parents[1]/"data/heredado_e2"
df=pd.read_csv(p/"resumen_reserva.csv")
fig=px.scatter(df,x="macro_f1_media",y="macro_f1_sd",hover_name="modelo",color="modelo",labels={"macro_f1_media":"Macro-F1 medio en reserva histórica","macro_f1_sd":"Desviación entre semillas"},template="plotly_white")
fig.update_layout(showlegend=False,margin=dict(t=20,l=25,r=20,b=30))
layout=html.Div([html.Span("02 / DATOS Y PROCEDENCIA",className="eyebrow"),html.H1("Medir antes de generalizar."),html.P("Diagnóstico heredado de E2. Este panel no representa un EDA nuevo ni resultados del candidato CICO.",className="lead"),html.Div([html.Div([html.H2("969"),html.P("recortes de reserva")],className="card"),html.Div([html.H2("6"),html.P("pacientes; no 969 observaciones independientes")],className="card"),html.Div([html.H2("13 × 5"),html.P("arquitecturas × semillas en el cierre heredado")],className="card")],className="grid"),html.Div([html.H2("Rendimiento y variabilidad"),dcc.Graph(figure=fig)],className="panel"),html.Div([html.H2("Condiciones de una evaluación válida"),html.P("Los intervalos por paciente y la variabilidad por semillas responden a preguntas diferentes. Los datos adicionales de E3 requieren auditoría de pacientes, sitios, duplicados y compatibilidad de etiquetas antes de agregarse."),html.A("Abrir galería y EDA publicados de E2 ↗",href="https://nucls-entregable2.onrender.com/dashboard/index.html",target="_blank")],className="panel")])
