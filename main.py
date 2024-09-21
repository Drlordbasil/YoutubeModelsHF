import os
import logging
import warnings
from idea_generator import generate_video_idea, generate_topics
from content_generator import generate_content
from tts_generator import generate_speech
from video_generator import create_video
from av_sync import sync_audio_video
from youtube_upload import upload_video, add_to_playlist
from image_generator import generate_images
from video_enhancer import enhance_video

# Suppress the OpenMP warning
warnings.filterwarnings("ignore", category=RuntimeWarning, module="threadpoolctl")

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    try:
        # Generate video idea
        title, description = generate_video_idea()
        logging.info(f"Generated video idea: {title}")
        
        # Generate topics based on the title
        topics = generate_topics(title)
        logging.info(f"Generated topics: {topics}")
        
        all_sections = []
        images = []
        for topic in topics:
            prompt = f"Create a detailed guide about {topic} related to {title}:"
            sections = generate_content(prompt)
            all_sections.extend(sections)
            logging.info(f"Generated content for topic: {topic}")
            
            # Generate an image for each topic
            image_prompt = f"A visual representation of {topic} related to {title}"
            image = generate_images(image_prompt)
            images.append(image)
            logging.info(f"Generated image for topic: {topic}")
        
        content = "\n\n".join(all_sections)
        
        audio_file = "output.wav"
        audio_file = generate_speech(content, audio_file)
        logging.info(f"Generated speech audio: {audio_file}")
        
        temp_video_file = "temp_video.mp4"
        create_video(all_sections, images, 600, temp_video_file)  # 10 minutes video
        logging.info(f"Created temporary video: {temp_video_file}")
        
        final_video_file = "final_output.mp4"
        sync_audio_video(temp_video_file, audio_file, final_video_file)
        logging.info(f"Synced audio and video: {final_video_file}")
        
        if not os.path.exists(final_video_file):
            raise FileNotFoundError(f"Final video file not created: {final_video_file}")
        
        # Enhance the video using AI
        enhanced_video_file = "enhanced_output.mp4"
        enhance_video(final_video_file, enhanced_video_file)
        logging.info(f"Enhanced video: {enhanced_video_file}")
        
        # Check if the enhanced video file exists
        if os.path.exists(enhanced_video_file):
            upload_file = enhanced_video_file
        elif os.path.exists(final_video_file):
            upload_file = final_video_file
            logging.warning("Enhanced video not found. Uploading original video.")
        else:
            raise FileNotFoundError("No video file found. Upload aborted.")

        video_id = upload_video(
            file_path=upload_file,
            title=title,
            description=description,
            tags=['Financial Automation', 'Online Finance', 'Budgeting', 'Investing', 'Saving', 'Personal Finance', 'Money Management'],
            privacy_status='private'
        )
        
        if video_id:
            logging.info(f"Video uploaded successfully. Video ID: {video_id}")
            # Add to a playlist (replace with your actual playlist ID)
            add_to_playlist(video_id, "YOUR_PLAYLIST_ID")
        else:
            logging.error("Video upload failed.")
        
        # Clean up files
        for file in [audio_file, temp_video_file, final_video_file, enhanced_video_file]:
            if os.path.exists(file):
                os.remove(file)
                logging.info(f"Removed temporary file: {file}")

    except Exception as e:
        logging.exception(f"An error occurred: {str(e)}")

if __name__ == "__main__":
    main()