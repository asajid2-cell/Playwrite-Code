class BasicTransformerBlock(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  norm1 : __torch__.torch.nn.modules.normalization.LayerNorm
  attn1 : __torch__.diffusers.models.attention_processor.Attention
  norm2 : __torch__.torch.nn.modules.normalization.___torch_mangle_24.LayerNorm
  attn2 : __torch__.diffusers.models.attention_processor.___torch_mangle_31.Attention
  norm3 : __torch__.torch.nn.modules.normalization.___torch_mangle_32.LayerNorm
  ff : __torch__.diffusers.models.attention.FeedForward
  def forward(self: __torch__.diffusers.models.attention.BasicTransformerBlock,
    hidden_states: Tensor,
    encoder_hidden_states: Tensor) -> Tensor:
    ff = self.ff
    norm3 = self.norm3
    attn2 = self.attn2
    norm2 = self.norm2
    attn1 = self.attn1
    norm1 = self.norm1
    _0 = (attn1).forward((norm1).forward(hidden_states, ), )
    input = torch.add(_0, hidden_states)
    _1 = (attn2).forward(encoder_hidden_states, (norm2).forward(input, ), )
    input0 = torch.add(_1, input)
    _2 = (ff).forward((norm3).forward(input0, ), )
    return torch.add(_2, input0)
class FeedForward(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  net : __torch__.torch.nn.modules.container.___torch_mangle_36.ModuleList
  def forward(self: __torch__.diffusers.models.attention.FeedForward,
    argument_1: Tensor) -> Tensor:
    net = self.net
    _2 = getattr(net, "2")
    net0 = self.net
    _1 = getattr(net0, "1")
    net1 = self.net
    _0 = getattr(net1, "0")
    _3 = (_1).forward((_0).forward(argument_1, ), )
    return (_2).forward(_3, )
