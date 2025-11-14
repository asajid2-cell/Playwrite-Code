class FeedForward(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  net : __torch__.torch.nn.modules.container.___torch_mangle_220.ModuleList
  def forward(self: __torch__.diffusers.models.attention.___torch_mangle_221.FeedForward,
    argument_1: Tensor) -> Tensor:
    net = self.net
    _2 = getattr(net, "2")
    net0 = self.net
    _1 = getattr(net0, "1")
    net1 = self.net
    _0 = getattr(net1, "0")
    _3 = (_1).forward((_0).forward(argument_1, ), )
    return (_2).forward(_3, )
