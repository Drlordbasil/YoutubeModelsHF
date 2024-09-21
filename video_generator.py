from moviepy.editor import *
from PIL import Image, ImageDraw, ImageFont
import numpy as np

def create_background(size, color1, color2):
    img = Image.new('RGB', size)
    draw = ImageDraw.Draw(img)
    for i in range(size[1]):
        r = int(color1[0] + (color2[0] - color1[0]) * i / size[1])
        g = int(color1[1] + (color2[1] - color1[1]) * i / size[1])
        b = int(color1[2] + (color2[2] - color1[2]) * i / size[1])
        draw.line([(0, i), (size[0], i)], fill=(r, g, b))
    return np.array(img)

def create_text_clip(text, size, duration, font_size=40, color='white', bg_color=(0,0,0,128)):
    txt_clip = TextClip(text, fontsize=font_size, color=color, size=size, 
                        method='caption', align='center', font='Arial')
    txt_clip = txt_clip.on_color(size=size, color=bg_color, pos=('center', 'center'))
    return txt_clip.set_duration(duration)

def create_video(sections, images, duration, output_file):
    clips = []
    bg = create_background((1280, 720), (30, 30, 30), (60, 60, 60))
    background = ImageClip(bg).set_duration(duration)
    
    section_duration = duration / len(sections)
    
    for i, (section, image_path) in enumerate(zip(sections, images)):
        # Create text clip
        txt_clip = create_text_clip(section, (1000, 300), section_duration)
        txt_clip = txt_clip.set_position(('center', 'bottom')).set_start(i * section_duration)
        
        # Create image clip
        img_clip = ImageClip(image_path).set_duration(section_duration)
        img_clip = img_clip.resize(height=400).set_position(('center', 'top')).set_start(i * section_duration)
        
        clips.extend([txt_clip, img_clip])
    
    final_video = CompositeVideoClip([background] + clips)
    final_video.write_videofile(output_file, fps=24)