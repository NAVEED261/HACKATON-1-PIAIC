import os
from openai import OpenAI
from sqlalchemy.orm import Session
from apps.backend.database import User # Assuming User model

openai_client = OpenAI()

def get_personalization_prompt(user_profile: User, chapter_content: str) -> str:
    """
    Generates a prompt for the LLM to personalize chapter content based on user profile.
    """
    preferences = user_profile.learning_preferences or "none specified"
    background = user_profile.hardware_software_background or "none specified"

    prompt = f"""You are an AI assistant tasked with personalizing textbook content.
Based on the user's learning preferences and hardware/software background, rewrite the provided chapter content to adjust its difficulty and focus. The goal is to make the content more relevant and understandable for this specific user.

User Learning Preferences: {preferences}
User Hardware/Software Background: {background}

Original Chapter Content:
{chapter_content}

Rewritten Chapter Content (personalized for the user):"""
    return prompt

def personalize_chapter_content(user_profile: User, chapter_content: str) -> str:
    """
    Rewrites chapter content using an LLM based on user's profile for personalization.
    """
    prompt = get_personalization_prompt(user_profile, chapter_content)

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo", # Can be gpt-4 for better quality
            messages=[
                {"role": "system", "content": "You are a helpful assistant that personalizes educational content."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error personalizing content with LLM: {e}")
        return "An error occurred while personalizing the chapter."


def get_difficulty_level(user_profile: User) -> str:
    """
    Placeholder for logic to determine difficulty level based on user profile.
    This would be more sophisticated in a real application.
    """
    # Example: Simple logic based on background keywords
    background_lower = (user_profile.hardware_software_background or "").lower()
    if "beginner" in background_lower or "basic" in background_lower:
        return "beginner"
    elif "advanced" in background_lower or "expert" in background_lower:
        return "advanced"
    return "intermediate"
