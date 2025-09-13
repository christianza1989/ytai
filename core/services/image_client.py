import os
from typing import Optional
from pathlib import Path
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation

class ImageClient:
    """Stability AI client for image generation"""

    def __init__(self):
        self.api_key = os.getenv('STABILITY_API_KEY')
        if not self.api_key:
            raise ValueError("STABILITY_API_KEY environment variable is required")

        # Initialize Stability AI client
        self.stability_api = client.StabilityInference(
            key=self.api_key,
            verbose=True,
            engine="stable-diffusion-xl-1024-v1-0",  # Latest SDXL model
        )

    def generate_image(self, prompt: str, save_path: str, filename: str) -> bool:
        """Generate image using Stability AI and save to specified location"""
        try:
            print(f"🎨 Generuojamas paveikslėlis pagal: {prompt[:50]}...")

            # Ensure save_path exists
            Path(save_path).mkdir(parents=True, exist_ok=True)

            # Generate image
            answers = self.stability_api.generate(
                prompt=prompt,
                seed=42,  # For reproducible results
                steps=50,  # Higher quality
                cfg_scale=7.0,  # Good balance
                width=1024,
                height=1024,
                samples=1,  # Generate one image
                sampler=generation.SAMPLER_K_DPMPP_2M  # Good quality sampler
            )

            # Process the first (and only) image
            for resp in answers:
                for artifact in resp.artifacts:
                    if artifact.finish_reason == generation.FILTERING_DISALLOWED:
                        print("❌ Paveikslėlis atmestas dėl turinio politikos")
                        return False
                    elif artifact.finish_reason == generation.FILTERING_DISALLOWED:
                        print("❌ Paveikslėlis atmestas dėl saugumo filtrų")
                        return False

                    if artifact.type == generation.ARTIFACT_IMAGE:
                        # Save the image
                        file_path = Path(save_path) / filename

                        with open(file_path, "wb") as f:
                            f.write(artifact.binary)

                        print(f"✅ Paveikslėlis išsaugotas: {file_path}")
                        return True

            print("❌ Nepavyko gauti paveikslėlio iš API")
            return False

        except Exception as e:
            print(f"❌ Klaida generuojant paveikslėlį: {e}")
            return False

    def generate_image_with_style(self, prompt: str, style: str, save_path: str, filename: str) -> bool:
        """Generate image with specific style parameters"""
        try:
            # Enhance prompt with style
            style_prompts = {
                "neon_city": "neon lights, cyberpunk city, futuristic, glowing signs, urban landscape",
                "dark_mood": "dark atmosphere, moody lighting, mysterious, dramatic shadows",
                "vibrant": "bright colors, energetic, dynamic composition, vivid",
                "minimalist": "clean, simple, geometric shapes, limited color palette",
                "nature": "natural landscape, organic shapes, earthy tones",
                "abstract": "abstract art, geometric patterns, artistic composition"
            }

            style_enhancement = style_prompts.get(style, "")
            enhanced_prompt = f"{prompt}, {style_enhancement}, professional album cover design, high quality"

            return self.generate_image(enhanced_prompt, save_path, filename)

        except Exception as e:
            print(f"❌ Klaida generuojant paveikslėlį su stiliumi: {e}")
            return False
