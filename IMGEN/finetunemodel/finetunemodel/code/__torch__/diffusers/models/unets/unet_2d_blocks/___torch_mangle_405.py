class CrossAttnUpBlock2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  attentions : __torch__.torch.nn.modules.container.___torch_mangle_373.ModuleList
  resnets : __torch__.torch.nn.modules.container.___torch_mangle_401.ModuleList
  upsamplers : __torch__.torch.nn.modules.container.___torch_mangle_404.ModuleList
  def forward(self: __torch__.diffusers.models.unets.unet_2d_blocks.___torch_mangle_405.CrossAttnUpBlock2D,
    argument_1: Tensor,
    argument_2: Tensor,
    argument_3: Tensor,
    encoder_hidden_states: Tensor,
    argument_5: Tensor,
    argument_6: Tensor) -> Tensor:
    upsamplers = self.upsamplers
    _0 = getattr(upsamplers, "0")
    attentions = self.attentions
    _2 = getattr(attentions, "2")
    resnets = self.resnets
    _20 = getattr(resnets, "2")
    attentions0 = self.attentions
    _1 = getattr(attentions0, "1")
    resnets0 = self.resnets
    _10 = getattr(resnets0, "1")
    attentions1 = self.attentions
    _00 = getattr(attentions1, "0")
    resnets1 = self.resnets
    _01 = getattr(resnets1, "0")
    input = torch.cat([argument_1, argument_2], 1)
    _3 = (_00).forward((_01).forward(input, argument_3, ), encoder_hidden_states, )
    input0 = torch.cat([_3, argument_5], 1)
    _4 = (_1).forward((_10).forward(input0, argument_3, ), encoder_hidden_states, )
    input1 = torch.cat([_4, argument_6], 1)
    _5 = (_2).forward((_20).forward(input1, argument_3, ), encoder_hidden_states, )
    return (_0).forward(_5, )
