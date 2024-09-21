from transformers import pipeline

def generate_video_idea():
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
    prompt = "Generate a YouTube video idea about financial automation:"
    
    idea = generator(prompt, max_length=100, do_sample=True)[0]['generated_text']
    
    # Extract the title and description from the generated idea
    lines = idea.split('\n')
    title = lines[0].strip()
    description = '\n'.join(lines[1:]).strip()
    
    return title, description

def generate_topics(title, num_topics=5):
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
    prompt = f"Generate {num_topics} subtopics for a YouTube video titled '{title}':"
    
    topics_text = generator(prompt, max_length=200, do_sample=True)[0]['generated_text']
    
    # Extract the topics from the generated text
    topics = [topic.strip() for topic in topics_text.split('\n') if topic.strip()][:num_topics]
    
    return topics