class TraceableUNet(Module):
  __parameters__ = []
  __buffers__ = []
  training : bool
  _is_full_backward_hook : Optional[bool]
  unet : __torch__.diffusers.models.unets.unet_2d_condition.UNet2DConditionModel
  def forward(self: __torch__.TraceableUNet,
    sample: Tensor,
    timestep: Tensor,
    encoder_hidden_states: Tensor) -> Tensor:
    unet = self.unet
    _0 = (unet).forward(sample, timestep, encoder_hidden_states, )
    return _0
