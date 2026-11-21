from pathlib import Path
import dash
from dash import Dash, html
import plotly.express as px
px.defaults.color_discrete_sequence=["#087f8c","#b36b45","#72518f","#54677a","#81965b"]
import dash_bootstrap_components as dbc
app = Dash(__name__, use_pages=True, title="NuCLS · Proyecto final", suppress_callback_exceptions=True, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server
server.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
app.layout = html.Div([
    html.Header([html.A("NuCLS / RESEARCH", href="/", className="brand"),
        html.Nav([html.A("Proyecto",href="/"),html.A("Histología",href="/histologia"),html.A("Resultados E1–E2",href="/proyecto"),html.A("Datos y EDA",href="/datos"),html.A("CICO",href="/modelos"),html.A("Diagnósticos",href="/diagnosticos"),html.A("Ejemplos",href="/ejemplos"),html.A("Literatura",href="/investigacion"),html.A("Evidencia",href="/reproducibilidad"),html.A("Cierre CPU",href="/cierre"),html.A("Piloto",href="/piloto"),html.A("Ablaciones",href="/ablaciones"),html.A("Analizar imagen",href="/prediccion"),html.A("Libro",href="/libro/")])]),
    html.Main(dash.page_container),
    html.Footer([html.P("NuCLS · Proyecto final · E1 + E2 + E3 · Revisión CPU: 21 noviembre 2026 · Resultados identificados por etapa"),html.A("Contexto y ficha del modelo",href="/documentacion"),html.Span(" · "),html.A("Privacidad",href="/documentacion#privacidad"),html.P("Demostración experimental: no diagnóstico. Las imágenes cargadas se procesan en memoria y no se usan para entrenar.")])])

from flask import send_from_directory, jsonify, abort
BOOK_HTML = Path(__file__).resolve().parent / 'book/_build/html'
@server.get('/healthz')
def healthz():
    from src.inference import engine
    try:
        _, meta = engine()
        return jsonify(status='ok', project='NuCLS-E3', trained_model_available=True, seed=meta['seed'])
    except Exception:
        return jsonify(status='ok', project='NuCLS-E3', trained_model_available=False)
@server.get('/libro/')
def book_home():
    if not (BOOK_HTML/'intro.html').is_file():
        abort(503, description='El libro aún no se ha compilado en este entorno.')
    return send_from_directory(BOOK_HTML, 'intro.html')
@server.get('/libro/<path:filename>')
def book_file(filename):
    return send_from_directory(BOOK_HTML, filename)

if __name__ == "__main__":
    import os
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT",8053)), debug=False)

@server.get('/histologia-imagen/<case>/<mode>')
def histology_image(case,mode):
    import re
    from flask import Response
    if case not in [f'{i:02d}' for i in range(1,37)] or mode not in ('limpia','anotada'):abort(404)
    svg=(Path(__file__).resolve().parent/'data/histologia'/f'{case}.svg').read_text()
    if mode=='limpia':svg=re.sub(r'<polygon[^>]*/>','',svg)
    return Response(svg,mimetype='image/svg+xml',headers={'Cache-Control':'public, max-age=86400'})
@server.get('/histologia-evidencia/casos.json')
def histology_provenance():
    return send_from_directory(Path(__file__).resolve().parent/'data/histologia','casos.json',as_attachment=True)


@server.get('/model-card')
def model_card_download():
 return send_from_directory(Path(__file__).resolve().parent,'MODEL_CARD.md',as_attachment=True)

@server.get('/ejemplo-png/<case>')
def example_png(case):
 import base64,json
 from flask import Response
 rows=json.loads((Path(__file__).resolve().parent/'data/ejemplos.json').read_text())
 r=next((r for r in rows if r['caso']==case),None)
 if r is None:abort(404)
 return Response(base64.b64decode((Path(__file__).resolve().parent/r['png_file']).read_text()),mimetype='image/png',headers={'Content-Disposition':'attachment; filename="'+r['archivo_ejemplo']+'"'})
