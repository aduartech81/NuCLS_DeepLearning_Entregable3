from pathlib import Path
import dash
from dash import Dash, html
app = Dash(__name__, use_pages=True, title="NuCLS · Proyecto final", suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div([
    html.Header([html.A("NuCLS / RESEARCH", href="/", className="brand"),
        html.Nav([html.A("Proyecto",href="/"),html.A("Resultados E1–E2",href="/proyecto"),html.A("Datos y EDA",href="/datos"),html.A("CICO",href="/modelos"),html.A("Literatura",href="/investigacion"),html.A("Evidencia",href="/reproducibilidad"),html.A("Piloto",href="/piloto"),html.A("Libro",href="/libro/")])]),
    html.Main(dash.page_container),
    html.Footer("NuCLS · Proyecto final · E1 + E2 + E3 · Corte: 20 noviembre 2026 · Resultados identificados por etapa")])

from flask import send_from_directory, jsonify, abort
BOOK_HTML = Path(__file__).resolve().parent / 'book/_build/html'
@server.get('/healthz')
def healthz():
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
