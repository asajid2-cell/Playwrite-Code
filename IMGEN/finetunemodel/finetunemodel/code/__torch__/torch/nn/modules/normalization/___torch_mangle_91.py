class LayerNorm(Module):
  __parameters__ = ["weight", "bias", ]
  __buffers__ = []
  weight : Tensor
  bias : Tensor
  training : bool
  _is_full_backward_hook : Optional[bool]
  def forward(self: __torch__.torch.nn.modules.normalization.___torch_mangle_91.LayerNorm,
    hidden_states: Tensor) -> Tensor:
    bias = self.bias
    weight = self.weight
    hidden_states0 = torch.layer_norm(hidden_states, [192], weight, bias)
    return hidden_states0
