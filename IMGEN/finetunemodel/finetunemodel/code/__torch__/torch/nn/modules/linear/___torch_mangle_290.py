class Linear(Module):
  __parameters__ = ["weight", ]
  __buffers__ = []
  weight : Tensor
  training : bool
  _is_full_backward_hook : Optional[bool]
  def forward(self: __torch__.torch.nn.modules.linear.___torch_mangle_290.Linear,
    argument_1: Tensor) -> Tensor:
    weight = self.weight
    return torch.linear(argument_1, weight)
