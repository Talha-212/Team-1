import google.generativeai as genai
import random

genai.configure(api_key="AIzaSyBCDa0w8-ESc-p5KPvQwHno3GNJsyCGQ4k")  # Replace with your real API key

def generate_paragraph(difficulty):
    random_word = random.choice(["ocean", "mountain", "laser", "dream", "falcon", "violin", "jungle"])

    prompt_map = {
        "Easy": "Write a single short paragraph suitable for a typing speed test. Use basic vocabulary. Include the word '{}'. Do not return multiple versions.",
        "Medium": "Write one medium-length paragraph for a typing test. Use clear and varied sentences. Include '{}'. Return only one paragraph.",
        "Hard": "Write one complex paragraph for an advanced typing test. Use advanced vocabulary and sentence structure. Include the word '{}'. Only one version should be returned."
    }

    prompt = prompt_map[difficulty].format(random_word)

    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content(prompt, generation_config={"temperature": 0.9})
        return response.text.strip()
    except Exception as e:
        print("Gemini API Error:", e)
        return "Typing practice is essential for improving your keyboard skills."
