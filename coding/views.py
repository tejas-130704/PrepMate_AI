from django.shortcuts import render
from .models import DSAQuestions
from django.http import JsonResponse
import subprocess
import json
import os
import tempfile
import subprocess
import json
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404, get_list_or_404
import json

# Create your views here.
@login_required(login_url="login")
def home(request):
    questions = DSAQuestions.objects.all()
    return render(request,"coding_home.html",{"questions":questions})

def question(request,question_id):
    ques = get_object_or_404(DSAQuestions, id=question_id)
    
    return render(request,"coding_question.html",{"question":ques})


def run_code(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            code = data.get("code", "")
            language = data.get("language", "")
            id = data.get("id", "")
            question = get_object_or_404(DSAQuestions,id=id)
            test_case=question.test_cases
            
            structured_input = "5\n10 20 30 40 50\n"
            # Adjust execution commands for Windows/Linux
            if language == "python":
                command = ["python", "-c", code]  # Use 'python' instead of 'python3' on Windows
            elif language == "javascript":
                command = ["node", "-e", code]
            elif language == "c":
                # Save code to a temporary file
                with tempfile.NamedTemporaryFile(delete=False, suffix=".c") as temp_c_file:
                    temp_c_file.write(code.encode())
                    temp_c_file_path = temp_c_file.name
                
                exe_file = temp_c_file_path.replace(".c", ".exe") if os.name == "nt" else "./a.out"

                # Compile the C code
                compile_command = ["gcc", temp_c_file_path, "-o", exe_file]
                compile_result = subprocess.run(compile_command, capture_output=True, text=True, shell=False)

                if compile_result.returncode != 0:
                    return JsonResponse({"output": compile_result.stderr, "success": False})

                # Run the compiled executable
                command = [exe_file]
            else:
                return JsonResponse({"output": "Unsupported language", "success": False})

            # Run the user's code
            result={}
            # print(test_case)

            for case in test_case:
                for key, value in case.items():  # Extract dictionary from list
                    test_input = value['input']
                    expected_output = value['expected_output'].strip()  # Remove extra spaces/newlines
                    
                    # Run the code
                    process = subprocess.run(command, input=test_input, text=True, capture_output=True, shell=False)
                    output = process.stdout.strip()  # Get and clean stdout

                    # Store results in a dictionary
                    result[key] = {
                        "input": test_input,
                        "expected_output": expected_output,
                        "output": output,
                        "status": "✅ Passed" if expected_output == output else "❌ Failed"
                    }
            
            return JsonResponse({"output": result, "success": True})

        except Exception as e:
            return JsonResponse({"output": str(e), "success": False})

    return JsonResponse({"output": "Invalid request", "success": False})
