class Attention(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  to_q : __torch__.torch.nn.modules.linear.___torch_mangle_50.Linear
  to_k : __torch__.torch.nn.modules.linear.___torch_mangle_51.Linear
  to_v : __torch__.torch.nn.modules.linear.___torch_mangle_52.Linear
  to_out : __torch__.torch.nn.modules.container.___torch_mangle_55.ModuleList
  def forward(self: __torch__.diffusers.models.attention_processor.___torch_mangle_56.Attention,
    encoder_hidden_states: Tensor,
    argument_2: Tensor) -> Tensor:
    to_out = self.to_out
    _1 = getattr(to_out, "1")
    to_out0 = self.to_out
    _0 = getattr(to_out0, "0")
    to_v = self.to_v
    to_k = self.to_k
    to_q = self.to_q
    _2 = torch.size(encoder_hidden_states, 0)
    batch_size = ops.prim.NumToTensor(_2)
    _3 = int(batch_size)
    _4 = int(batch_size)
    _5 = int(batch_size)
    _6 = int(batch_size)
    _7 = (to_q).forward(argument_2, )
    _8 = (to_k).forward(encoder_hidden_states, )
    _9 = (to_v).forward(encoder_hidden_states, )
    _10 = ops.prim.NumToTensor(torch.size(_8, 2))
    head_dim = torch.floor_divide(_10, CONSTANTS.c4)
    _11 = int(head_dim)
    _12 = int(head_dim)
    _13 = torch.view(_7, [_6, -1, 4, int(head_dim)])
    query = torch.transpose(_13, 1, 2)
    key = torch.transpose(torch.view(_8, [_5, -1, 4, _12]), 1, 2)
    value = torch.transpose(torch.view(_9, [_4, -1, 4, _11]), 1, 2)
    hidden_states = torch.scaled_dot_product_attention(query, key, value)
    _14 = torch.transpose(hidden_states, 1, 2)
    _15 = int(torch.mul(head_dim, CONSTANTS.c4))
    hidden_states0 = torch.reshape(_14, [_3, -1, _15])
    input = torch.to(hidden_states0, 6)
    _16 = (_1).forward((_0).forward(input, ), )
    return torch.div(_16, CONSTANTS.c3)
