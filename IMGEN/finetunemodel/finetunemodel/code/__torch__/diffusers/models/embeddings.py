class Timesteps(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  def forward(self: __torch__.diffusers.models.embeddings.Timesteps,
    timesteps: Tensor) -> Tensor:
    _0 = torch.arange(0, 64, dtype=6, layout=None, device=torch.device("cpu"), pin_memory=False)
    exponent = torch.mul(_0, CONSTANTS.c0)
    exponent0 = torch.div(exponent, CONSTANTS.c1)
    emb = torch.exp(exponent0)
    _1 = torch.slice(timesteps, 0, 0, 9223372036854775807)
    _2 = torch.to(torch.unsqueeze(_1, 1), 6)
    _3 = torch.slice(torch.unsqueeze(emb, 0), 1, 0, 9223372036854775807)
    emb0 = torch.mul(_2, _3)
    emb1 = torch.mul(emb0, CONSTANTS.c2)
    emb2 = torch.cat([torch.sin(emb1), torch.cos(emb1)], -1)
    _4 = torch.slice(emb2, 0, 0, 9223372036854775807)
    _5 = torch.slice(_4, 1, 64, 9223372036854775807)
    _6 = torch.slice(emb2, 0, 0, 9223372036854775807)
    t_emb = torch.cat([_5, torch.slice(_6, 1, 0, 64)], -1)
    return t_emb
class TimestepEmbedding(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  linear_1 : __torch__.torch.nn.modules.linear.Linear
  act : __torch__.torch.nn.modules.activation.SiLU
  linear_2 : __torch__.torch.nn.modules.linear.___torch_mangle_0.Linear
  def forward(self: __torch__.diffusers.models.embeddings.TimestepEmbedding,
    input: Tensor) -> Tensor:
    linear_2 = self.linear_2
    act = self.act
    linear_1 = self.linear_1
    _7 = (act).forward((linear_1).forward(input, ), )
    return (linear_2).forward(_7, )
