from diffusers import StableDiffusionPipeline
import torch

def generate_images(prompt):
    model_id = "stabilityai/stable-diffusion-2-1"
    pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
    pipe = pipe.to("cuda")

    image = pipe(prompt).images[0]
    
    # Save the image and return the file path
    image_path = f"generated_image_{prompt[:10]}.png"
    image.save(image_path)
    return image_path