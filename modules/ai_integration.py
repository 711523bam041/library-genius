from openai import OpenAI
from config import OPENAI_API_KEY

class AIBookAssistant:
    def __init__(self):
        if OPENAI_API_KEY and OPENAI_API_KEY != 'your-openai-api-key':
            self.client = OpenAI(api_key=OPENAI_API_KEY)
            self.enabled = True
        else:
            self.enabled = False
            print("Warning: OpenAI API key not configured. AI features disabled.")
    
    def generate_summary(self, title, author, description=""):
        """Generate a concise book summary using OpenAI"""
        if not self.enabled:
            return "AI summary generation is not available. Please configure OPENAI_API_KEY."
        
        try:
            prompt = f"Write a concise 150-word summary of the book '{title}' by {author}."
            if description:
                prompt += f"\n\nAdditional context: {description[:500]}"
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful literary assistant. Provide concise, informative book summaries."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"Error generating summary: {str(e)}"
    
    def suggest_genres(self, title, author, description=""):
        """Suggest 3-5 genre categories for a book"""
        if not self.enabled:
            return "Fiction, Literature"
        
        try:
            prompt = f"Suggest 3-5 genre categories for the book '{title}' by {author}."
            if description:
                prompt += f"\n\nDescription: {description[:300]}"
            prompt += "\n\nReturn only a comma-separated list of genres, nothing else."
            
            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a literary expert. Suggest appropriate book genres."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=50,
                temperature=0.5
            )
            genres = response.choices[0].message.content.strip()
            return genres
        except Exception as e:
            return f"Fiction, Literature"
