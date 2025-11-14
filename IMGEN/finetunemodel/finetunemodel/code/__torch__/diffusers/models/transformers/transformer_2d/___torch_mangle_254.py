class Transformer2DModel(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  norm : __torch__.torch.nn.modules.normalization.___torch_mangle_226.GroupNorm
  proj_in : __torch__.torch.nn.modules.conv.___torch_mangle_227.Conv2d
  transformer_blocks : __torch__.torch.nn.modules.container.___torch_mangle_252.ModuleList
  proj_out : __torch__.torch.nn.modules.conv.___torch_mangle_253.Conv2d
  def forward(self: __torch__.diffusers.models.transformers.transformer_2d.___torch_mangle_254.Transformer2DModel,
    argument_1: Tensor,
    encoder_hidden_states: Tensor) -> Tensor:
    proj_out = self.proj_out
    transformer_blocks = self.transformer_blocks
    _0 = getattr(transformer_blocks, "0")
    proj_in = self.proj_in
    norm = self.norm
    batch_size = ops.prim.NumToTensor(torch.size(argument_1, 0))
    _1 = int(batch_size)
    height = ops.prim.NumToTensor(torch.size(argument_1, 2))
    _2 = int(height)
    width = ops.prim.NumToTensor(torch.size(argument_1, 3))
    _3 = int(width)
    batch = ops.prim.NumToTensor(torch.size(argument_1, 0))
    _4 = int(batch)
    height0 = ops.prim.NumToTensor(torch.size(argument_1, 2))
    width0 = ops.prim.NumToTensor(torch.size(argument_1, 3))
    _5 = (proj_in).forward((norm).forward(argument_1, ), )
    inner_dim = ops.prim.NumToTensor(torch.size(_5, 1))
    _6 = int(inner_dim)
    _7 = int(inner_dim)
    _8 = torch.permute(_5, [0, 2, 3, 1])
    _9 = [_4, int(torch.mul(height0, width0)), _7]
    hidden_states = torch.reshape(_8, _9)
    _10 = (_0).forward(hidden_states, encoder_hidden_states, )
    _11 = torch.reshape(_10, [_1, _2, _3, _6])
    input = torch.contiguous(torch.permute(_11, [0, 3, 1, 2]))
    hidden_states0 = torch.add((proj_out).forward(input, ), argument_1)
    return hidden_states0
