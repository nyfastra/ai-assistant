import os
import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from google import genai

@csrf_exempt
def assistant_view(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_prompt = data.get("prompt", "")

            api_key = os.getenv("GEMINI_API_KEY")
            if not api_key:
                return JsonResponse({"error": "Gemini API key is missing in .env"}, status=500)

            client = genai.Client(api_key=api_key)
            
            try:
                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=user_prompt,
                )
            except Exception:
                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=user_prompt,
                )

            reply_text = ""
            if hasattr(response, 'text') and response.text:
                reply_text = response.text
            elif hasattr(response, 'candidates') and response.candidates:
                parts = response.candidates[0].content.parts
                reply_text = "".join([part.text for part in parts if hasattr(part, 'text') and part.text])

            return JsonResponse({"reply": reply_text})

        except Exception as e:
            return JsonResponse({"error": str(e)}, status=500)

    return render(request, "ai_assistant/assistant.html")