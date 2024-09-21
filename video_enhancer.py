from diffusers import StableVideoDiffusionPipeline
import torch
import cv2
import numpy as np
from PIL import Image  # Add this import

def enhance_video(input_file, output_file):
    # Load the video
    cap = cv2.VideoCapture(input_file)
    fps = cap.get(cv2.CAP_PROP_FPS)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    # Initialize the StableVideoDiffusionPipeline
    pipe = StableVideoDiffusionPipeline.from_pretrained(
        "stabilityai/stable-video-diffusion-img2vid-xt", torch_dtype=torch.float16, variant="fp16"
    )
    pipe = pipe.to("cuda")

    # Prepare the output video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert frame to PIL Image
        pil_image = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        # Generate enhanced frame
        enhanced_frames = pipe(pil_image, num_frames=1).frames[0]

        # Convert back to OpenCV format and write to output
        enhanced_frame = cv2.cvtColor(np.array(enhanced_frames), cv2.COLOR_RGB2BGR)
        out.write(enhanced_frame)

    cap.release()
    out.release()