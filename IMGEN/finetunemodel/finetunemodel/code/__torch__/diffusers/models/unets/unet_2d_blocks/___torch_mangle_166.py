class CrossAttnDownBlock2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  attentions : __torch__.torch.nn.modules.container.___torch_mangle_147.ModuleList
  resnets : __torch__.torch.nn.modules.container.___torch_mangle_165.ModuleList
  def forward(self: __torch__.diffusers.models.unets.unet_2d_blocks.___torch_mangle_166.CrossAttnDownBlock2D,
    argument_1: Tensor,
    argument_2: Tensor,
    encoder_hidden_states: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
    attentions = self.attentions
    _1 = getattr(attentions, "1")
    resnets = self.resnets
    _10 = getattr(resnets, "1")
    attentions0 = self.attentions
    _0 = getattr(attentions0, "0")
    resnets0 = self.resnets
    _00 = getattr(resnets0, "0")
    _2 = (_00).forward(argument_1, argument_2, )
    _3, _4, = _2
    _5 = (_0).forward(_3, encoder_hidden_states, )
    _6 = (_1).forward((_10).forward(_5, argument_2, ), encoder_hidden_states, )
    return (_6, _5, _4)
