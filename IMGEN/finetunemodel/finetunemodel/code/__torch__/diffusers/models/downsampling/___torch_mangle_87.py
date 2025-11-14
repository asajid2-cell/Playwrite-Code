class Downsample2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  conv : __torch__.torch.nn.modules.conv.___torch_mangle_86.Conv2d
  def forward(self: __torch__.diffusers.models.downsampling.___torch_mangle_87.Downsample2D,
    argument_1: Tensor) -> Tensor:
    conv = self.conv
    return (conv).forward(argument_1, )
