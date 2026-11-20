from app import app
from pages.modelos import update

def test_routes_and_layout():
 c=app.server.test_client()
 for path in ['/', '/datos', '/modelos', '/_dash-layout', '/_dash-dependencies']:
  assert c.get(path).status_code==200

def test_reference_selection():
 fig, detail=update('resnet50')
 assert len(fig.data[0].x)==13
 assert '0.6669' in detail[1].children
