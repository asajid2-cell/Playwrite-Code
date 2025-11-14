class ModuleList(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  __annotations__["0"] = __torch__.diffusers.models.activations.___torch_mangle_455.GEGLU
  __annotations__["1"] = __torch__.torch.nn.modules.dropout.___torch_mangle_456.Dropout
  __annotations__["2"] = __torch__.torch.nn.modules.linear.___torch_mangle_457.Linear
