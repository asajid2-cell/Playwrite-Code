class ResnetBlock2D(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  norm1 : __torch__.torch.nn.modules.normalization.___torch_mangle_148.GroupNorm
  conv1 : __torch__.torch.nn.modules.conv.___torch_mangle_149.Conv2d
  time_emb_proj : __torch__.torch.nn.modules.linear.___torch_mangle_150.Linear
  norm2 : __torch__.torch.nn.modules.normalization.___torch_mangle_151.GroupNorm
  dropout : __torch__.torch.nn.modules.dropout.___torch_mangle_152.Dropout
  conv2 : __torch__.torch.nn.modules.conv.___torch_mangle_153.Conv2d
  nonlinearity : __torch__.torch.nn.modules.activation.___torch_mangle_154.SiLU
  conv_shortcut : __torch__.torch.nn.modules.conv.___torch_mangle_155.Conv2d
  def forward(self: __torch__.diffusers.models.resnet.___torch_mangle_156.ResnetBlock2D,
    argument_1: Tensor,
    argument_2: Tensor) -> Tuple[Tensor, Tensor]:
    conv_shortcut = self.conv_shortcut
    conv2 = self.conv2
    dropout = self.dropout
    norm2 = self.norm2
    time_emb_proj = self.time_emb_proj
    conv1 = self.conv1
    nonlinearity = self.nonlinearity
    norm1 = self.norm1
    _0 = (nonlinearity).forward((norm1).forward(argument_1, ), )
    _1 = (conv1).forward(_0, )
    _2 = (nonlinearity).forward1(argument_2, )
    _3 = torch.slice((time_emb_proj).forward(_2, ), 0, 0, 9223372036854775807)
    _4 = torch.slice(_3, 1, 0, 9223372036854775807)
    temb = torch.unsqueeze(torch.unsqueeze(_4, 2), 3)
    input = torch.add(_1, temb)
    _5 = (nonlinearity).forward2((norm2).forward(input, ), )
    _6 = (conv2).forward((dropout).forward(_5, ), )
    input0 = torch.contiguous(argument_1)
    _7 = torch.add((conv_shortcut).forward(input0, ), _6)
    hidden_states = torch.div(_7, CONSTANTS.c3)
    return (hidden_states, input0)
