class Linear(Module):
  __parameters__ = ["weight", ]
  __buffers__ = []
  weight : Tensor
  training : bool
  _is_full_backward_hook : Optional[bool]
  def forward(self: __torch__.torch.nn.modules.linear.___torch_mangle_27.Linear,
    encoder_hidden_states: Tensor) -> Tensor:
    weight = self.weight
    value = torch.linear(encoder_hidden_states, weight)
    return value
