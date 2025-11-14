class GroupNorm(Module):
  __parameters__ = ["weight", "bias", ]
  __buffers__ = []
  weight : Tensor
  bias : Tensor
  training : bool
  _is_full_backward_hook : Optional[bool]
  def forward(self: __torch__.torch.nn.modules.normalization.___torch_mangle_344.GroupNorm,
    argument_1: Tensor) -> Tensor:
    bias = self.bias
    weight = self.weight
    input = torch.group_norm(argument_1, 32, weight, bias, 9.9999999999999995e-07)
    return input
