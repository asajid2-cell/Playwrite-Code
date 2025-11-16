from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path
from typing import Optional, Sequence

import torch
from diffusers import DDPMScheduler
from PIL import Image
from torchvision import transforms
from transformers import AutoModel, AutoTokenizer

PROJECT_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TS_MODEL = PROJECT_ROOT / "IMGEN" / "finetunemodel.ts"


@dataclass
class PromptImageResult:
    prompt: str
    seed: int
    image: Image.Image


class PromptImageGenerator:
    """Lightweight text-to-image sampler powered by a traced UNet."""

    def __init__(
        self,
        *,
        model_path: Path | str | None = None,
        device: Optional[str | torch.device] = None,
        image_size: int = 128,
        max_prompt_length: int = 77,
        default_guidance: float = 5.5,
        default_steps: int = 40,
    ) -> None:
        target_path = Path(model_path or DEFAULT_TS_MODEL)
        if not target_path.is_file():
            raise FileNotFoundError(
                f"TorchScript model not found at {target_path}. Ensure IMGEN assets are deployed."
            )

        self.device = torch.device(device) if device is not None else torch.device(
            "cuda" if torch.cuda.is_available() else "cpu"
        )
        # TorchScript weights are float32; keep sampling in fp32 for stability on CPU.
        self.dtype = torch.float16 if self.device.type == "cuda" else torch.float32
        self.model = torch.jit.load(str(target_path), map_location=self.device)
        self.model.eval()
        self.model.to(self.device)
        if self.device.type == "cuda":
            self.model.to(dtype=self.dtype)

        self.tokenizer = AutoTokenizer.from_pretrained("prajjwal1/bert-tiny")
        self.text_encoder = AutoModel.from_pretrained(
            "prajjwal1/bert-tiny",
            use_safetensors=True,
            dtype=self.dtype,
        )
        self.text_encoder.eval()
        self.text_encoder.to(self.device, dtype=self.dtype)

        self.base_scheduler = DDPMScheduler(
            num_train_timesteps=1000,
            beta_schedule="squaredcos_cap_v2",
            prediction_type="epsilon",
        )

        self.image_size = image_size
        self.max_prompt_length = max_prompt_length
        self.default_guidance = default_guidance
        self.default_steps = default_steps
        self.blank_prompt = " "
        self.to_pil = transforms.ToPILImage()

    def _encode_text(self, prompts: Sequence[str]) -> torch.Tensor:
        encoded = self.tokenizer(
            list(prompts),
            max_length=self.max_prompt_length,
            padding="max_length",
            truncation=True,
            return_tensors="pt",
        )
        encoded = {k: v.to(self.device) for k, v in encoded.items()}
        with torch.inference_mode():
            hidden = self.text_encoder(**encoded).last_hidden_state
        return hidden

    def generate(
        self,
        prompt: str,
        *,
        guidance_scale: Optional[float] = None,
        num_inference_steps: Optional[int] = None,
        seed: Optional[int] = None,
    ) -> PromptImageResult:
        clean_prompt = (prompt or "").strip()
        if not clean_prompt:
            raise ValueError("Prompt text is required.")

        steps = int(num_inference_steps or self.default_steps)
        guidance = float(guidance_scale or self.default_guidance)
        if steps <= 0:
            raise ValueError("Number of inference steps must be positive.")
        if guidance <= 0:
            raise ValueError("Guidance scale must be positive.")

        if seed is None:
            seed = random.randint(0, 2**31 - 1)
        generator = torch.Generator(device=self.device)
        generator.manual_seed(int(seed))

        scheduler = DDPMScheduler.from_config(self.base_scheduler.config)
        scheduler.set_timesteps(steps, device=self.device)

        with torch.inference_mode():
            latents = torch.randn(
                (1, 3, self.image_size, self.image_size),
                generator=generator,
                device=self.device,
                dtype=self.dtype,
            )

            text_embeddings = self._encode_text([clean_prompt])
            uncond_embeddings = self._encode_text([self.blank_prompt])

            for t in scheduler.timesteps:
                latent_model_input = torch.cat([latents, latents], dim=0)
                latent_model_input = scheduler.scale_model_input(latent_model_input, t)

                encoder_hidden_states = torch.cat(
                    [uncond_embeddings, text_embeddings], dim=0
                )
                noise_pred = self.model(
                    latent_model_input, t, encoder_hidden_states
                )
                if hasattr(noise_pred, "sample"):
                    model_out = noise_pred.sample
                elif isinstance(noise_pred, (tuple, list)):
                    model_out = noise_pred[0]
                else:
                    model_out = noise_pred

                noise_pred_uncond, noise_pred_text = model_out.chunk(2)
                guided = noise_pred_uncond + guidance * (
                    noise_pred_text - noise_pred_uncond
                )
                latents = scheduler.step(guided, t, latents).prev_sample

            image_tensor = (latents * 0.5 + 0.5).clamp(0, 1)[0].cpu()
            pil_image = self.to_pil(image_tensor)

        return PromptImageResult(prompt=clean_prompt, seed=int(seed), image=pil_image)
