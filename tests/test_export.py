import torch
import pytest
from training.export_onnx import export
from src.original_model import ContextoAcotado

def test_export_rejects_untrained(tmp_path):
 p=tmp_path/'untrained.pt';torch.save({'trained':False},p)
 with pytest.raises(ValueError): export(p,tmp_path/'model.onnx')

def test_export_roundtrip(tmp_path):
 # Synthetic fixture, never published as a trained scientific artifact.
 torch.manual_seed(1); m=ContextoAcotado(width=4)
 p=tmp_path/'fixture.pt'
 torch.save(dict(trained=True,protocol_sha256='synthetic-test-only',model_config={'width':4},model=m.state_dict(),verification_inputs=torch.randn(2,3,16,16),preprocessing={'test_only':True}),p)
 assert export(p,tmp_path/'fixture.onnx')<1e-4
