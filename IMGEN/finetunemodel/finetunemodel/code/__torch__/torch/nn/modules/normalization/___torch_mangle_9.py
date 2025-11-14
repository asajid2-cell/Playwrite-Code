class GroupNorm(Module):
  __parameters__ = ["weight", "bias", ]
  __buffers__ = []
  weight : Tensor
  bias : Tensor
  training : bool
  _is_full_backward_hook : Optional[bool]
  def forward(self: __torch__.torch.nn.modules.normalization.___torch_mangle_9.GroupNorm,
    input: Tensor) -> Tensor:
    bias = self.bias
    weight = self.weight
    input0 = torch.group_norm(input, 32, weight, bias)
    return input0
