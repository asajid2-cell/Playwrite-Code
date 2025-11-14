class Attention(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  to_q : __torch__.torch.nn.modules.linear.___torch_mangle_289.Linear
  to_k : __torch__.torch.nn.modules.linear.___torch_mangle_290.Linear
  to_v : __torch__.torch.nn.modules.linear.___torch_mangle_291.Linear
  to_out : __torch__.torch.nn.modules.container.___torch_mangle_294.ModuleList
  def forward(self: __torch__.diffusers.models.attention_processor.___torch_mangle_295.Attention,
    argument_1: Tensor) -> Tensor:
    to_out = self.to_out
    _1 = getattr(to_out, "1")
    to_out0 = self.to_out
    _0 = getattr(to_out0, "0")
    to_v = self.to_v
    to_k = self.to_k
    to_q = self.to_q
    batch_size = ops.prim.NumToTensor(torch.size(argument_1, 0))
    _2 = int(batch_size)
    _3 = int(batch_size)
    _4 = int(batch_size)
    _5 = int(batch_size)
    _6 = (to_q).forward(argument_1, )
    _7 = (to_k).forward(argument_1, )
    _8 = (to_v).forward(argument_1, )
    _9 = ops.prim.NumToTensor(torch.size(_7, 2))
    head_dim = torch.floor_divide(_9, CONSTANTS.c4)
    _10 = int(head_dim)
    _11 = int(head_dim)
    _12 = torch.view(_6, [_5, -1, 4, int(head_dim)])
    query = torch.transpose(_12, 1, 2)
    key = torch.transpose(torch.view(_7, [_4, -1, 4, _11]), 1, 2)
    value = torch.transpose(torch.view(_8, [_3, -1, 4, _10]), 1, 2)
    hidden_states = torch.scaled_dot_product_attention(query, key, value)
    _13 = torch.transpose(hidden_states, 1, 2)
    _14 = int(torch.mul(head_dim, CONSTANTS.c4))
    hidden_states0 = torch.reshape(_13, [_2, -1, _14])
    input = torch.to(hidden_states0, 6)
    _15 = (_1).forward((_0).forward(input, ), )
    return torch.div(_15, CONSTANTS.c3)
