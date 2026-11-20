"""Prototype CICO: context limited by orientation disagreement.

Candidate, not established novelty. Mathematical sources and differences are in
experiments/procedencia.md. Written from the formulation, using tensor primitives.
No training or pretrained models are imported by the web application.
"""
import math
import torch
from torch import nn


def orbit_d4(x):
    """Eight exact lattice isometries of a square; no interpolation."""
    def rotations(a):
        return [a, a.transpose(-2, -1).flip(-2), a.flip((-2, -1)),
                a.transpose(-2, -1).flip(-1)]
    return rotations(x) + rotations(x.flip(-1))


class ContextoAcotado(nn.Module):
    """Invariant center classifier with a bounded contextual logit correction.

    beta is a fixed correction budget (not learned), penalty controls orientation
    disagreement. Neither is chosen using the historical test partition.
    """
    def __init__(self, width=16, classes=3, beta=0.5, penalty=1.0,
                 use_orbit=True, use_contrast=True, use_dispersion=True,
                 use_context=True):
        super().__init__()
        if width < 2 or classes < 2 or beta < 0 or penalty < 0:
            raise ValueError('Invalid width, classes or nonnegative budgets')
        self.classes, self.beta, self.penalty = classes, float(beta), float(penalty)
        self.use_orbit, self.use_contrast = use_orbit, use_contrast
        self.use_dispersion, self.use_context = use_dispersion, use_context
        # No batch statistics or dropout: each transformed view uses the same map.
        self.encoder = nn.Sequential(
            nn.Conv2d(3, width, 3, padding=1), nn.SiLU(),
            nn.Conv2d(width, width, 3, stride=2, padding=1), nn.SiLU(),
            nn.Conv2d(width, 2*width, 3, stride=2, padding=1), nn.SiLU())
        self.center_head = nn.Linear(2*width, classes)
        self.context_head = nn.Linear(2*width, classes)
        self.gate = nn.Linear(4*width, 1)

    def descriptors(self, x):
        f = self.encoder(x)
        h, w = f.shape[-2:]
        # Square central window and disjoint surround, with the same mask per view.
        y = torch.arange(h, device=f.device, dtype=f.dtype) - (h-1)/2
        z = torch.arange(w, device=f.device, dtype=f.dtype) - (w-1)/2
        mask = ((y[:, None].abs() < h/4) & (z[None, :].abs() < w/4)).to(f.dtype)
        center = (f*mask).sum((-2, -1))/mask.sum()
        surround = (f*(1-mask)).sum((-2, -1))/(1-mask).sum()
        return center, surround

    def components(self, x):
        if not torch.jit.is_tracing():
            if x.ndim != 4 or x.shape[1] != 3 or x.shape[2] != x.shape[3] or x.shape[2] < 16:
                raise ValueError('Expected N×3×H×H, H>=16')
            if not x.is_floating_point() or not torch.isfinite(x).all():
                raise ValueError('Expected finite floating-point images')
        views = orbit_d4(x) if self.use_orbit else [x]
        pairs = [self.descriptors(v) for v in views]
        c = torch.stack([p[0] for p in pairs]); s = torch.stack([p[1] for p in pairs])
        center, surround = c.mean(0), s.mean(0)
        relation = s-c if self.use_contrast else s
        r = relation.mean(0)
        dispersion = ((relation-r)**2).mean((0, 2)).unsqueeze(-1)
        gate = torch.sigmoid(self.gate(torch.cat([center, surround], -1)))
        damping = 1/(1+self.penalty*dispersion) if self.use_dispersion else torch.ones_like(dispersion)
        budget = self.beta*gate*damping
        delta = budget*torch.tanh(self.context_head(r))/math.sqrt(self.classes)
        if not self.use_context:
            delta = torch.zeros_like(delta)
        base = self.center_head(center)
        return dict(logits=base+delta, base=base, delta=delta,
                    budget=budget, dispersion=dispersion)

    def forward(self, x):
        return self.components(x)['logits']
