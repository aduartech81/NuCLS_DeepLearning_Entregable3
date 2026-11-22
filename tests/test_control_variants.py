import pytest,torch
from src.original_model import orbit_d4
from src.control_variants import build_control,CONFIGS

def test_controls_preserve_stored_capacity_and_initial_weights():
 torch.manual_seed(20261122);reference=build_control('cico_completo',width=4)
 original={k:v.clone() for k,v in reference.state_dict().items()}
 for name in CONFIGS:
  model=build_control(name,reference,width=4)
  assert sum(p.numel() for p in model.parameters())==sum(p.numel() for p in reference.parameters())
  for k,v in model.state_dict().items():torch.testing.assert_close(v,original[k])
 for k,v in reference.state_dict().items():torch.testing.assert_close(v,original[k])

def test_central_controls_remove_context_exactly():
 x=torch.randn(2,3,16,16)
 for name in ('base_central','solo_orbita'):
  c=build_control(name,width=4).components(x)
  assert torch.count_nonzero(c['delta'])==0
  torch.testing.assert_close(c['logits'],c['base'],atol=0,rtol=0)

def test_dispersion_needs_multiple_views():
 x=torch.randn(2,3,16,16)
 for name in ('solo_contexto','contexto_contraste'):
  m=build_control(name,width=4);c=m.components(x)
  assert torch.count_nonzero(c['dispersion'])==0

@pytest.mark.parametrize('name',['solo_orbita','orbita_contexto','orbita_contexto_contraste','cico_completo'])
def test_orbit_controls_are_invariant(name):
 torch.manual_seed(33);m=build_control(name,width=4).double().eval();x=torch.randn(2,3,16,16,dtype=torch.double)
 for transformed in orbit_d4(x):torch.testing.assert_close(m(x),m(transformed),atol=1e-12,rtol=1e-10)

def test_context_gate_has_effect_and_gradients():
 torch.manual_seed(44);reference=build_control('cico_completo',width=4);x=torch.randn(2,3,16,16)
 for name in ('solo_contexto','contexto_contraste','orbita_contexto','orbita_contexto_contraste','cico_completo'):
  m=build_control(name,reference,width=4);c=m.components(x)
  assert torch.count_nonzero(c['delta'])>0
  c['logits'].square().sum().backward()
  assert m.context_head.weight.grad.abs().sum()>0
  assert torch.linalg.vector_norm(c['delta'],dim=-1).max()<=m.beta
