
from google import genai
import json
import re
from config import GEMINI_API_KEY
client = genai.Client(api_key=GEMINI_API_KEY)

def parse_resume_with_gemini(resume_text: str) -> dict:
    prompt = f"""
You are an expert resume parser. Extract ONLY the following fields in JSON format:
- name (full candidate name)
- email (email address)
- phone (phone number)
- skills (list of professional skills)
- qualifications (list of degrees or certifications)
- experience_years (total years of work experience as a number)

Return ONLY the JSON object, without any additional text or markdown formatting.

Resume:
{resume_text}
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        
        # Extract the text from the response
        if hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                response_text = candidate.content.parts[0].text
            else:
                response_text = str(response)
        else:
            response_text = str(response)
        
        # Clean the response to extract just the JSON
        response_text = response_text.strip()
        
        # Remove markdown code blocks if present
        response_text = re.sub(r'^```json|```$', '', response_text, flags=re.MULTILINE).strip()
        
        # Parse the JSON
        parsed_data = json.loads(response_text)
        
        # Ensure all required fields are present
        required_fields = ['name', 'email', 'phone', 'skills', 'qualifications', 'experience_years']
        for field in required_fields:
            if field not in parsed_data:
                parsed_data[field] = "" if field != 'experience_years' else 0
                
        return parsed_data
        
    except json.JSONDecodeError as e:
        print(f"Failed to parse JSON: {e}")
        print("Raw response:", response_text)
        return {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "qualifications": [],
            "experience_years": 0
        }
    except Exception as e:
        print(f"Error calling Gemini API: {e}")
        return {
            "name": "",
            "email": "",
            "phone": "",
            "skills": [],
            "qualifications": [],
            "experience_years": 0
        }