import os
from openai import OpenAI

openai_client = OpenAI()

def translate_chapter_content_to_urdu(chapter_content: str) -> str:
    """
    Translates chapter content from English Markdown to Urdu Markdown using an LLM.
    Preserves Markdown formatting.
    """
    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo", # Or gpt-4 for higher quality
            messages=[
                {"role": "system", "content": "You are a helpful assistant that translates educational content from English to Urdu, preserving Markdown formatting."},
                {"role": "user", "content": f"Translate the following English Markdown content to Urdu, preserving all Markdown formatting, including headings, bold text, lists, and code blocks:\n\n{chapter_content}"}
            ],
            max_tokens=4000, # Adjust as needed
        )
        translated_text = response.choices[0].message.content.strip()
        return translated_text
    except Exception as e:
        print(f"Error translating content with LLM: {e}")
        return "An error occurred during translation."