import io
import pytest
import torch
from src.original_model import ContextoAcotado, orbit_d4

torch.set_num_threads(2)

def model():
    torch.manual_seed(19)
    return ContextoAcotado(width=4).double().eval()

def test_all_eight_isometries():
    m=model(); x=torch.randn(2,3,16,16,dtype=torch.double)
    for transformed in orbit_d4(x):
        torch.testing.assert_close(m(x),m(transformed),atol=1e-12,rtol=1e-10)

def test_context_budget():
    m=model()
    for scale in [0.,1.,10.]:
        d=m.components(torch.randn(4,3,16,16,dtype=torch.double)*scale)
        assert (torch.linalg.vector_norm(d['delta'],dim=-1)<=m.beta+1e-12).all()
        assert (torch.linalg.vector_norm(d['delta'],dim=-1)<=d['budget'].squeeze(-1)+1e-12).all()

def test_gradients_and_gradcheck():
    m=model();x=torch.randn(1,3,16,16,dtype=torch.double,requires_grad=True)
    assert torch.autograd.gradcheck(m,(x,),fast_mode=True)
    m(x).square().sum().backward()
    for name,p in m.named_parameters():
        assert p.grad is not None and torch.isfinite(p.grad).all(),name
        assert p.grad.abs().sum()>0,name

def test_invalid_input():
    m=model()
    for x in [torch.zeros(1,1,16,16),torch.zeros(1,3,16,20),torch.full((1,3,16,16),float('nan'))]:
        with pytest.raises(ValueError):m(x)

def test_same_seed_and_serialization():
    a=model();b=model();x=torch.randn(1,3,16,16,dtype=torch.double)
    torch.testing.assert_close(a(x),b(x))
    buf=io.BytesIO();torch.save(a.state_dict(),buf);buf.seek(0)
    b.load_state_dict(torch.load(buf,weights_only=True));torch.testing.assert_close(a(x),b(x))

def test_tiny_synthetic_learning():
    torch.manual_seed(8);m=ContextoAcotado(width=4)
    x=torch.zeros(6,3,16,16);y=torch.arange(6)%3
    for i in range(6):x[i,y[i]]=1
    opt=torch.optim.Adam(m.parameters(),lr=.02)
    for _ in range(100):
        opt.zero_grad();loss=torch.nn.functional.cross_entropy(m(x),y);loss.backward();opt.step()
    assert loss.item()<.1
    assert (m(x).argmax(1)==y).all()
