class DownBlock2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  resnets : __torch__.torch.nn.modules.container.ModuleList
  downsamplers : __torch__.torch.nn.modules.container.___torch_mangle_15.ModuleList
  def forward(self: __torch__.diffusers.models.unets.unet_2d_blocks.DownBlock2D,
    argument_1: Tensor,
    argument_2: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
    downsamplers = self.downsamplers
    _0 = getattr(downsamplers, "0")
    resnets = self.resnets
    _1 = getattr(resnets, "1")
    resnets0 = self.resnets
    _00 = getattr(resnets0, "0")
    _2 = (_00).forward(argument_1, argument_2, )
    _3 = (_1).forward(_2, argument_2, )
    return ((_0).forward(_3, ), _3, _2)
class CrossAttnDownBlock2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  attentions : __torch__.torch.nn.modules.container.___torch_mangle_68.ModuleList
  resnets : __torch__.torch.nn.modules.container.___torch_mangle_85.ModuleList
  downsamplers : __torch__.torch.nn.modules.container.___torch_mangle_88.ModuleList
  def forward(self: __torch__.diffusers.models.unets.unet_2d_blocks.CrossAttnDownBlock2D,
    argument_1: Tensor,
    argument_2: Tensor,
    encoder_hidden_states: Tensor) -> Tuple[Tensor, Tensor, Tensor]:
    downsamplers = self.downsamplers
    _0 = getattr(downsamplers, "0")
    attentions = self.attentions
    _1 = getattr(attentions, "1")
    resnets = self.resnets
    _13 = getattr(resnets, "1")
    attentions0 = self.attentions
    _04 = getattr(attentions0, "0")
    resnets1 = self.resnets
    _05 = getattr(resnets1, "0")
    _2 = (_05).forward(argument_1, argument_2, )
    _3 = (_04).forward(_2, encoder_hidden_states, )
    _4 = (_1).forward((_13).forward(_3, argument_2, ), encoder_hidden_states, )
    return ((_0).forward(_4, ), _4, _3)
class CrossAttnUpBlock2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  attentions : __torch__.torch.nn.modules.container.___torch_mangle_255.ModuleList
  resnets : __torch__.torch.nn.modules.container.___torch_mangle_283.ModuleList
  upsamplers : __torch__.torch.nn.modules.container.___torch_mangle_285.ModuleList
  def forward(self: __torch__.diffusers.models.unets.unet_2d_blocks.CrossAttnUpBlock2D,
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
    _21 = getattr(resnets, "2")
    attentions1 = self.attentions
    _1 = getattr(attentions1, "1")
    resnets2 = self.resnets
    _14 = getattr(resnets2, "1")
    attentions2 = self.attentions
    _06 = getattr(attentions2, "0")
    resnets3 = self.resnets
    _07 = getattr(resnets3, "0")
    input = torch.cat([argument_1, argument_2], 1)
    _5 = (_06).forward((_07).forward(input, argument_3, ), encoder_hidden_states, )
    input0 = torch.cat([_5, argument_5], 1)
    _6 = (_1).forward((_14).forward(input0, argument_3, ), encoder_hidden_states, )
    input1 = torch.cat([_6, argument_6], 1)
    _7 = (_2).forward((_21).forward(input1, argument_3, ), encoder_hidden_states, )
    return (_0).forward(_7, )
class UpBlock2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  resnets : __torch__.torch.nn.modules.container.___torch_mangle_433.ModuleList
  def forward(self: __torch__.diffusers.models.unets.unet_2d_blocks.UpBlock2D,
    argument_1: Tensor,
    argument_2: Tensor,
    argument_3: Tensor,
    argument_4: Tensor,
    argument_5: Tensor) -> Tensor:
    resnets = self.resnets
    _2 = getattr(resnets, "2")
    resnets4 = self.resnets
    _1 = getattr(resnets4, "1")
    resnets5 = self.resnets
    _0 = getattr(resnets5, "0")
    input = torch.cat([argument_1, argument_2], 1)
    _8 = [(_0).forward(input, argument_3, ), argument_4]
    input2 = torch.cat(_8, 1)
    _9 = [(_1).forward(input2, argument_3, ), argument_5]
    input3 = torch.cat(_9, 1)
    return (_2).forward(input3, argument_3, )
class UNetMidBlock2DCrossAttn(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  attentions : __torch__.torch.nn.modules.container.___torch_mangle_464.ModuleList
  resnets : __torch__.torch.nn.modules.container.___torch_mangle_481.ModuleList
  def forward(self: __torch__.diffusers.models.unets.unet_2d_blocks.UNetMidBlock2DCrossAttn,
    argument_1: Tensor,
    argument_2: Tensor,
    encoder_hidden_states: Tensor) -> Tensor:
    resnets = self.resnets
    _1 = getattr(resnets, "1")
    attentions = self.attentions
    _0 = getattr(attentions, "0")
    resnets6 = self.resnets
    _08 = getattr(resnets6, "0")
    _10 = (_08).forward(argument_1, argument_2, )
    _11 = (_0).forward(_10, encoder_hidden_states, )
    return (_1).forward(_11, argument_2, )
