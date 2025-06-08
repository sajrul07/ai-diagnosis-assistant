import google.generativeai as genai
import json
import logging
import re
from config import GOOGLE_API_KEY

logger = logging.getLogger(__name__)

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")

async def generate_medical_report_ai(request_data: dict) -> dict:
    prompt = f"""
    You are a medical AI assistant. Generate a structured medical report in **strictly valid JSON format** based on the patient's details.

    Patient Details:
    - Age: {request_data['age']}
    - Gender: {request_data['gender']}
    - Weight: {request_data['weight']} kg
    - Symptoms: {request_data['symptoms']}
    - Medical History: {request_data['medical_history']}

    Format the response as follows:
    {{
        "diagnosis": {{
            "disease": "Possible disease name",
            "summary": "Brief description of the disease",
            "severity": "Severity level"
        }},
        "immediate_actions": {{
            "steps": ["Action 1", "Action 2"],
            "emergency_signs": ["Sign 1", "Sign 2"]
        }},
        "medical_recommendations": {{
            "specialist_to_consult": "Specialist type",
            "recommended_tests": ["Test 1", "Test 2"],
            "treatment_options": ["Treatment 1", "Treatment 2"]
        }},
        "risk_factors": {{
            "causes": ["Cause 1", "Cause 2"],
            "high_risk_groups": ["Group 1", "Group 2"]
        }},
        "preventive_measures": {{
            "prevention_tips": ["Tip 1", "Tip 2"],
            "lifestyle_changes": ["Change 1", "Change 2"]
        }}
    }}
    **Important:** Return **only JSON** without any additional text or explanations.
    """

    try:
        response = model.generate_content(prompt)
        logger.info("AI Response: %s", response.text)
        print("AI Response:", response.text)

        json_match = re.search(r"\{.*\}", response.text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON found in AI response")

        return json.loads(json_match.group(0))

    except json.JSONDecodeError:
        logger.error("Failed to parse AI response as JSON")
        raise

    except Exception as e:
        logger.error("AI processing error: %s", str(e))
        raise
