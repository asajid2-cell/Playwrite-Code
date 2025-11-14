class Upsample2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  conv : __torch__.torch.nn.modules.conv.___torch_mangle_284.Conv2d
  def forward(self: __torch__.diffusers.models.upsampling.Upsample2D,
    argument_1: Tensor) -> Tensor:
    conv = self.conv
    input = torch.upsample_nearest2d(argument_1, None, [2., 2.])
    return (conv).forward(input, )
