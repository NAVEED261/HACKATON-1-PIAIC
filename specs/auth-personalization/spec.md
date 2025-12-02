# 🔐 4.4 Auth & Personalization Specification

## Purpose
Define WHAT authentication + personalization must do.

## Functional Requirements

### Signup:
Collect:
- Software background
- Hardware background
- GPU access
- Learning style

### Personalization:
- Modify chapter difficulty based on user profile
- Use OpenAI LLM to rewrite the chapter content

### Urdu Translation:
- Convert Markdown → Urdu
- Preserve headings, lists, formatting

### Data Storage:
- Neon Postgres MUST store:
  - Profiles
  - Preferences
  - Learning metadata
