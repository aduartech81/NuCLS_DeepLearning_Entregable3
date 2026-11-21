import numpy as np
from app import app
from pages.prediccion import upload_status
from tests.test_inference import upload

def test_upload_requires_consent_and_valid_pixels():
 image=upload(np.zeros((128,128,3),dtype='uint8'))
 assert upload_status(image,'test.png',[])[1:]==(True,True,True)
 assert upload_status(None,None,['yes'])[1:]==(True,True,False)
 assert upload_status(image,'test.png',['yes'])[1:]==(False,False,False)
 assert upload_status(upload(np.zeros((64,64,3),dtype='uint8')),'small.png',['yes'])[1:]==(True,True,False)
 assert upload_status('data:image/png;base64,!!!','bad.png',['yes'])[1:]==(True,True,False)

def test_browser_feedback_asset_served():
 r=app.server.test_client().get('/assets/upload_feedback.js')
 assert r.status_code==200 and b'reader.onerror' in r.data and b'event.stopImmediatePropagation' in r.data
