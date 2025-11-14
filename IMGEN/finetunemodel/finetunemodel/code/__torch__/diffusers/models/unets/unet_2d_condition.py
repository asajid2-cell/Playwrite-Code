class UNet2DConditionModel(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  conv_in : __torch__.torch.nn.modules.conv.Conv2d
  time_proj : __torch__.diffusers.models.embeddings.Timesteps
  time_embedding : __torch__.diffusers.models.embeddings.TimestepEmbedding
  down_blocks : __torch__.torch.nn.modules.container.___torch_mangle_167.ModuleList
  up_blocks : __torch__.torch.nn.modules.container.___torch_mangle_434.ModuleList
  mid_block : __torch__.diffusers.models.unets.unet_2d_blocks.UNetMidBlock2DCrossAttn
  conv_norm_out : __torch__.torch.nn.modules.normalization.___torch_mangle_482.GroupNorm
  conv_act : __torch__.torch.nn.modules.activation.___torch_mangle_483.SiLU
  conv_out : __torch__.torch.nn.modules.conv.___torch_mangle_484.Conv2d
  def forward(self: __torch__.diffusers.models.unets.unet_2d_condition.UNet2DConditionModel,
    sample: Tensor,
    timestep: Tensor,
    encoder_hidden_states: Tensor) -> Tensor:
    conv_out = self.conv_out
    conv_act = self.conv_act
    conv_norm_out = self.conv_norm_out
    up_blocks = self.up_blocks
    _2 = getattr(up_blocks, "2")
    up_blocks0 = self.up_blocks
    _1 = getattr(up_blocks0, "1")
    up_blocks1 = self.up_blocks
    _0 = getattr(up_blocks1, "0")
    mid_block = self.mid_block
    down_blocks = self.down_blocks
    _20 = getattr(down_blocks, "2")
    down_blocks0 = self.down_blocks
    _10 = getattr(down_blocks0, "1")
    down_blocks1 = self.down_blocks
    _00 = getattr(down_blocks1, "0")
    conv_in = self.conv_in
    time_embedding = self.time_embedding
    time_proj = self.time_proj
    _3 = ops.prim.NumToTensor(torch.size(sample, 0))
    timesteps = torch.expand(timestep, [int(_3)])
    input = torch.to((time_proj).forward(timesteps, ), 6)
    _4 = (time_embedding).forward(input, )
    _5 = (conv_in).forward(sample, )
    _6, _7, _8, = (_00).forward(_5, _4, )
    _9 = (_10).forward(_6, _4, encoder_hidden_states, )
    _11, _12, _13, = _9
    _14 = (_20).forward(_11, _4, encoder_hidden_states, )
    _15, _16, _17, = _14
    _18 = (mid_block).forward(_15, _4, encoder_hidden_states, )
    _19 = (_0).forward(_18, _15, _4, encoder_hidden_states, _16, _17, )
    _21 = (_1).forward(_19, _12, _4, encoder_hidden_states, _13, _6, )
    _22 = (conv_norm_out).forward((_2).forward(_21, _7, _4, _8, _5, ), )
    _23 = (conv_out).forward((conv_act).forward(_22, ), )
    return _23
