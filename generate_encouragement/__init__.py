import openai
import os
import azure.functions as func
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        req_body = req.get_json()
        project_description = req_body.get('description')

        # Construct prompt
        prompt = f"I'm working on this personal project: {project_description}. Please give me some encouraging words to stay motivated and accomplish it."

        # OpenAI API call
        openai.api_key = os.environ["OPENAI_API_KEY"]
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an uplifting and motivational assistant."},
                {"role": "user", "content": prompt}
            ]
        )

        encouragement = response.choices[0].message.content.strip()

        return func.HttpResponse(
            json.dumps({"encouragement": encouragement}),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        return func.HttpResponse(
            json.dumps({"error": str(e)}),
            status_code=500,
            mimetype="application/json"
        )
