import requests
import json
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

def get_book_summary(title, author, description, category_name=""):
    """
    Fetches an AI-generated book summary from Google Gemini API.
    If the API Key is missing or the request fails, it falls back to a 
    highly engaging, custom-designed mock summary based on the book's data.
    """
    api_key = getattr(settings, 'GEMINI_API_KEY', '')
    
    if api_key:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key={api_key}"
        headers = {'Content-Type': 'application/json'}
        prompt = (
            f"Provide an engaging, professional book summary and overview for the book '{title}' by '{author}'. "
            f"Here is a brief description of the book to guide your writing: '{description}'. "
            f"Structure your response nicely with markdown. Include three clear sections: "
            f"1. A narrative 'Synopsis' (about 100 words), "
            f"2. 'Key Takeaways' (bullet points), and "
            f"3. 'Who Should Read This' (bullet points). "
            f"Do not write excessive headers. Make the tone warm, intellectual, and exciting."
        )
        
        payload = {
            "contents": [
                {
                    "parts": [
                        {"text": prompt}
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(url, headers=headers, json=payload, timeout=8)
            if response.status_code == 200:
                response_data = response.json()
                # Parse the response text out of the standard Gemini JSON structure
                text = response_data['candidates'][0]['content']['parts'][0]['text']
                if text:
                    return text
            else:
                logger.warning(f"Gemini API returned error code {response.status_code}: {response.text}")
        except Exception as e:
            logger.error(f"Error calling Gemini API: {str(e)}")

    # Fallback smart Mock AI Summary Generator
    return generate_mock_summary(title, author, description, category_name)


def generate_mock_summary(title, author, description, category_name):
    """Generates an extremely detailed and professional-looking summary when Gemini is offline."""
    category_lower = str(category_name).lower()
    
    # Customise mock summary highlights based on the category of the book
    if 'tech' in category_lower or 'programming' in category_lower or 'education' in category_lower:
        takeaways = [
            "Gain practical, real-world strategies that can be implemented immediately.",
            "Deconstruct highly complex structural concepts into clean, digestible mental models.",
            "Acquire the baseline architectures required to build, test, and scale modern systems."
        ]
        audience = [
            "Students, professionals, and lifelong learners looking to sharpen their analytical skills.",
            "Engineers, designers, and practitioners aiming to master advanced technical methodologies."
        ]
        hook = "essential companion guide for modern mastery."
    elif 'fiction' in category_lower or 'novel' in category_lower or 'mystery' in category_lower:
        takeaways = [
            "Explore highly multi-dimensional character dynamics and profound psychological struggles.",
            "Deconstruct thematic explorations of memory, identity, society, and human vulnerability.",
            "Experience an intricate, expertly-paced plot full of emotional resonance and atmospheric prose."
        ]
        audience = [
            "Lovers of deeply emotional, lyrical storytelling and high-stakes character conflicts.",
            "Readers who appreciate masterfully built tension, poetic symbolism, and philosophical depth."
        ]
        hook = "stunning and unforgettable masterpiece of literary imagination."
    else:
        # Default fallback
        takeaways = [
            "Understand the fundamental core principles guiding the main subject matter.",
            "Discover historical contexts and future-facing perspectives from the expert author.",
            "Adopt new viewpoints that challenge conventional wisdom and traditional practices."
        ]
        audience = [
            "General non-fiction enthusiasts seeking a thought-provoking, well-researched read.",
            "Curious minds wanting to expand their intellectual horizons with clear, structured wisdom."
        ]
        hook = "magnificent addition to your personal library."

    synopsis = (
        f"**_{title}_** by **{author}** is a {hook} "
        f"Built upon the core themes of the book, this work explores the deep concepts "
        f"and ideas surrounding: *\"{description[:160]}...\"* "
        f"The author writes with a distinctive, highly persuasive style, balancing thorough analysis "
        f"with captivating storytelling. By synthesizing complex theories into direct, actionable "
        f"realizations, the book bridges theoretical paradigms and actual life experiences in a way "
        f"that is both engaging and deeply impactful."
    )

    markdown_summary = f"""### AI-Generated Summary (Mock Mode)

#### Synopsis
{synopsis}

#### Key Takeaways
{"".join([f"* {t}\n" for t in takeaways])}
#### Who Should Read This
{"".join([f"* {a}\n" for a in audience])}
"""
    return markdown_summary
