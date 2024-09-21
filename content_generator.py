from transformers import pipeline

def generate_content(prompt, max_length=1000):
    generator = pipeline('text-generation', model='EleutherAI/gpt-neo-1.3B')
    generated_text = generator(prompt, max_length=max_length, do_sample=True)[0]['generated_text']
    
    # Split the content into sections
    sections = generated_text.split('\n\n')
    
    # Keep only the first 5 sections or less if there are fewer
    sections = sections[:min(5, len(sections))]
    
    return sections