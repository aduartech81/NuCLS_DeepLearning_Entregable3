from pathlib import Path
import dash
from dash import html,dcc,Input,Output,callback
import pandas as pd
import plotly.express as px

dash.register_page(__name__,path="/modelos",name="Modelos")
df=pd.read_csv(Path(__file__).resolve().parents[1]/"data/heredado_e2/resumen_reserva.csv")
layout=html.Div([html.Span("03 / MODELOS Y EVIDENCIA",className="eyebrow"),html.H1("Un candidato. Un contraste explícito."),html.Div([html.H2("CICO · contexto acotado por desacuerdo"),html.P("z(x) = Wc · c̄ + b + β · σ(a) / (1 + λV) · tanh(Wr · r̄ + br) / √K"),html.P("c̄: centro medio · r̄: contraste entorno−centro · V: dispersión entre vistas · K: clases"),html.P("La norma de la corrección contextual no supera β. Esto no garantiza robustez global frente a cambios del tejido ni superioridad sobre las redes existentes."),html.Strong("Estado: cinco semillas piloto completas y verificadas; curvas y resultados en la página Piloto.")],className="panel"),html.H2("Referencia histórica · cierre E2"),html.P("Selección de referencia visual; no determina ajustes del candidato sobre reserva."),dcc.Dropdown(id="modelo",options=[{"label":x,"value":x} for x in df.modelo],value="resnet50",clearable=False),dcc.Graph(id="ranking"),html.Div(id="detalle",className="panel"),html.Div([html.H2("Inferencia del candidato"),html.P("Modelo piloto exportado y comprobado localmente en CPU. Recibe recortes RGB de 128 × 128; uso exploratorio, sin validación clínica."),html.A("Analizar un recorte",href="/prediccion",className="button")],className="panel")])
@callback(Output("ranking","figure"),Output("detalle","children"),Input("modelo","value"))
def update(model):
 d=df.sort_values("macro_f1_media"); colors=["#13aa95" if x==model else "#b8ccd4" for x in d.modelo]
 fig=px.bar(d,x="macro_f1_media",y="modelo",orientation="h",error_x="macro_f1_sd",template="plotly_white",labels={"macro_f1_media":"Macro-F1 ± DE entre semillas","modelo":""})
 fig.update_traces(marker_color=colors);fig.update_layout(height=520,margin=dict(t=20,l=20,r=20,b=30),xaxis_range=[0,1])
 r=df[df.modelo==model].iloc[0]
 return fig,[html.H3(model),html.P(f"Media: {r.macro_f1_media:.4f} · DE: {r.macro_f1_sd:.4f} · R: {int(r.R)}"),html.P(f"IC95 por paciente: [{r.IC95_paciente_inf:.4f}, {r.IC95_paciente_sup:.4f}]. La barra anterior representa DE entre semillas, no este intervalo.")]
