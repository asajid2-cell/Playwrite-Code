class Conv2d(Module):
  __parameters__ = ["weight", "bias", ]
  __buffers__ = []
  weight : Tensor
  bias : Tensor
  training : bool
  _is_full_backward_hook : Optional[bool]
  def forward(self: __torch__.torch.nn.modules.conv.Conv2d,
    sample: Tensor) -> Tensor:
    bias = self.bias
    weight = self.weight
    input = torch._convolution(sample, weight, bias, [1, 1], [1, 1], [1, 1], False, [0, 0], 1, False, False, True, True)
    return input
