class ModuleList(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  __annotations__["0"] = __torch__.torch.nn.modules.linear.___torch_mangle_182.Linear
  __annotations__["1"] = __torch__.torch.nn.modules.dropout.___torch_mangle_183.Dropout
