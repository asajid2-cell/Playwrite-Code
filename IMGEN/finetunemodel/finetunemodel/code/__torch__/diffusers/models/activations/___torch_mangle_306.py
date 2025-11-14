class GEGLU(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  proj : __torch__.torch.nn.modules.linear.___torch_mangle_305.Linear
  def forward(self: __torch__.diffusers.models.activations.___torch_mangle_306.GEGLU,
    argument_1: Tensor) -> Tensor:
    proj = self.proj
    _0 = torch.chunk((proj).forward(argument_1, ), 2, -1)
    hidden_states, gate, = _0
    input = torch.mul(hidden_states, torch.gelu(gate))
    return input
