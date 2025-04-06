from django.shortcuts import render
from django.http import JsonResponse
import base64
import os
import io
from PIL import Image
import pdf2image
import google.generativeai as genai

genai.configure(api_key="") #Add your API key here

# Prompts
input_prompt1 = """
You are an experienced Technical HR Manager with Tech Experience in the field of  Data Science, Full stack web development, Data Anaylst, Big Data Engineering, DEVOPS. Your task is to review the provided resume against the job description for these profiles.
Please share your professional evaluation on whether the candidate's profile aligns with the role.
Highlight the strengths and weaknesses of the applicant in relation to the specified job requirements. 
Please provide Response in Bullent points, and make it interavtive using html and tailwind css.
"""

input_prompt3 = """
You are a skilled ATS (Applicant Tracking System) scanner with a deep understanding of Data Science, Full stack web development, Data Anaylst, Big Data Engineering, DEVOPS  and deep ATS functionality.
Your task is to evaluate the resume against the provided job description. Provide a percentage match first, 
then list missing keywords, and finally, share final thoughts.
Please provide Response in Bullent points, and make it interavtive using html and tailwind css.
"""

def resume_home(request):
    return render(request, "resume_home.html")

def getResume_data(request):
    if request.method == "POST":
        try:
            input_text = request.POST.get("input_text", "")  # Get job description

            pdf_file = request.FILES["pdf"]
            # Convert PDF to image format
            if "pdf" not in request.FILES:
                return JsonResponse({"error": "No PDF file provided"}, status=400)

            pdf_content = input_pdf_setup(pdf_file)

            

            # Get AI-generated responses
            response1 = get_gemini_response(input_prompt1, pdf_content, input_text)
            response2 = get_gemini_response(input_prompt3, pdf_content, input_text)
            response1 = response1.replace("```html","").replace("```","")
            response2 = response2.replace("```html","").replace("```","")

            response = {"response1": response1, "response2": response2}
        
            return JsonResponse({"response": response, "success": True})
        
        except Exception as e:
            return JsonResponse({"error": str(e), "success": False})
    else:
        return JsonResponse({"output": "Invalid request", "success": False})
        
    


def input_pdf_setup(uploaded_file):
    if uploaded_file is not None:
        # Convert PDF to images
        images = pdf2image.convert_from_bytes(uploaded_file.read())

        if not images:
            raise ValueError("No pages found in the uploaded PDF")

        first_page = images[0]


        # Convert to bytes
        img_byte_arr = io.BytesIO()
        first_page.save(img_byte_arr, format="JPEG")
        img_byte_arr = img_byte_arr.getvalue()

        pdf_parts = [
            {
                "mime_type": "image/jpeg",
                "data": base64.b64encode(img_byte_arr).decode()  # Encode to base64
            }
        ]
        return pdf_parts
    else:
        raise FileNotFoundError("No file uploaded")

def get_gemini_response(input_prompt, pdf_content, job_description):

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content([input_prompt, pdf_content[0], job_description])
    return response.text
