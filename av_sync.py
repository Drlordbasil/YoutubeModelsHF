from moviepy.editor import *
import logging

def sync_audio_video(video_file, audio_file, output_file):
    try:
        logging.info(f"Starting audio-video sync: video={video_file}, audio={audio_file}")
        video = VideoFileClip(video_file)
        audio = AudioFileClip(audio_file)
        
        # Ensure audio duration matches video duration
        if audio.duration > video.duration:
            audio = audio.subclip(0, video.duration)
        else:
            video = video.subclip(0, audio.duration)
        
        final_video = video.set_audio(audio)
        final_video.write_videofile(output_file)
        logging.info(f"Audio-video sync complete: {output_file}")
    except Exception as e:
        logging.exception(f"Error in sync_audio_video: {str(e)}")
        raise