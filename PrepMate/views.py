import json
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render,HttpResponse,redirect
from .models import Company,JobPost
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, get_list_or_404
from .gemini_response import get_gemini_response
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
from .models import Interview
from base.models import IndivisualAnalysis
import re

# Create your views here.
def home(request):
    # obj = Company.objects.filter()  # This retrieves all Company objects.
    companies=get_list_or_404(Company)
    
    print("This is new: ",companies)
    
    context={
        'company':companies,
    }
    return render(request,"PrepMate_index.html",context)

@login_required(login_url="login")
def profile(request):
    data = Interview.objects.filter(user=request.user)  # Returns a queryset of interviews
    gd_data= IndivisualAnalysis.objects.filter(user=request.user)
    return render(request, "profile.html", context={'data': data, 'gd_data':gd_data})


def getGD(request,gd_id):
    gd_data = get_object_or_404(IndivisualAnalysis, id=gd_id)
    return render(request, "getGD.html", context={'gd_data':gd_data})
    
def registration(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        # Check if the username is unique
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists. Please choose a different one.")
            return redirect('registration')  # Redirect back to the registration page

        # Basic validation
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect('registration')  # Redirect back to the registration page

        try:
            # Create a new user
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')  # Redirect to the login page after successful registration
        except Exception as e:
            messages.error(request, "An error occurred during registration: " + str(e))
            return redirect('registration')  # Redirect back to the registration page

    return render(request, "register.html")






def login_view(request):  # Renamed for clarity
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)  # Log the user in
            messages.success(request, "Login successful")  # Message for successful login
            return redirect('home')  # Redirect to the home page after successful login
        else:
            messages.error(request, "Invalid Username or Password")  # Error message for invalid login

    return render(request, "login.html")


from django.contrib import messages  # Import Django messages framework

def byPosition(request):
    jobs = JobPost.objects.values('id', 'title').distinct()
    
    if request.method == "POST":
        query = request.POST.get('search')
        
        if query:  # Check if query is not empty
            jobs = JobPost.objects.filter(title__icontains=query).values('id', 'title').distinct()
            
            if not jobs.exists():  # If no results found
                messages.error(request, "No result found")
        else:
            messages.warning(request, "Please enter a search term")

    return render(request, "PrepMate_byPosition.html", {"jobs": jobs})


def byCompany(request):
    company=get_list_or_404(Company)
    
    if request.method == "POST":
        query = request.POST.get('search')
        
        if query:  # Check if query is not empty
            company = Company.objects.filter(name__icontains=query)
            
            if not company.exists():  # If no results found
                messages.error(request, "No result found")
        else:
            messages.warning(request, "Please enter a search term")
            
    return render(request,"PrepMate_byCompany.html",{"company":company})




@login_required(login_url="login")
def logout_view(request):
    logout(request)  # Clears the session
    messages.success(request, 'You have been logged out.')
    return redirect('home')


def post(request, comp_id):
    # Get the company or return a 404 if it doesn't exist
    comp = get_object_or_404(Company, id=comp_id)
    
    # Fetching job posts related to the company using the company object directly
    obj = JobPost.objects.filter(company=comp)  
    context={
        'company':comp,
        'post':obj,
    }
    print(obj)
    return render(request,"PrepMate_post.html",context)


# @login_required(login_url="login")
# def meet(request):
#     if request.method == 'POST':
#         # Retrieve form data from POST request
#         course_id = request.POST.get('post')
#         # if course_id and course_id.isdigit():  
#         #     course_id = int(course_id)
#         round_selected = request.POST.get('round')
#         difficulty_selected = request.POST.get('difficulty')
#         interviewer_selected = request.POST.get('interviewer')
#         # audio_checked = 'audio' in request.POST  # True if checked, False if not
#         # video_checked = 'video' in request.POST  # True if checked, False if not
#         terms_accepted = request.POST.get('terms')  # None if not checked
#         course_id = int(course_id)
#         print(type(course_id))
        
#         interviewer=interviewer_selected+".mp4"
#         # inter_content ={
#         #     "John.mp4":"M",
#         #     "Jyoti.mp4": "F",
#         #     "Lisa.mp4" : "F",
#         #     "Mike.mp4" : "M",
#         # }
#         # gender = inter_content.get(interviewer) 
#         # Retrieve the JobPost object using get() to avoid indexing
#         obj = get_object_or_404(JobPost, id=course_id)
#         print(obj)

#         # Retrieve the Company object associated with the JobPost
#         # comp = Company.objects.filter(name=obj.company).values()
#         comp = get_object_or_404(Company, name=obj.company)
#         print("Whats new: ",comp)
#         print("Company Name:",comp)

#         # Prepare the question data for the gemini_response
#         question = [round_selected, difficulty_selected, obj, comp.name]
#         # result="'Tell me about a challenging technical project you worked on and how you overcame the obstacles', ' Describe a time you had to learn a new technology quickly', ' How do you stay up-to-date with the latest advancements in software engineering'"
#         # Assuming gemini_response is a function that returns a list-like object
#         try:
#             result = get_gemini_response(question,'Q')  # This should now work as a function
#             # Get the current time
#             current_time = datetime.now()

#             # Check if it's morning or afternoon
#             if current_time.hour < 12:
#                 section = "Good morning"
#             else:
#                 section = "Good afternoon"
                    
#             greeting=f"{section} and thank you for joining us today! I'm looking forward to our conversation and learning more about your background and experiences. Let's get started whenever you're ready.,"
             
#             result=greeting+result

#             lst = result.split(',')
#         except Exception as e:
#             # Handle the error if the Gemini API call fails
#             print(f"Error calling Gemini API: {e}")
#             return HttpResponse(f"Error: {str(e)}")
#         lst=result.split(',')  # Convert the result to a list if necessary
#         print(lst)
#         # Prepare context for rendering the template
#         context = {
#             'data': lst,
#             'company': comp,
#             'post': obj,
#             'interviewer':interviewer,
#         }

#         # Render the response with the context
#         return render(request, "PrepMate_meet.html", context=context)
    
#     else:
#         # Avoid referencing POST data in GET requests, handle it differently
#         return HttpResponse("This page only handles POST requests.")

from django.contrib.sessions.models import Session

@login_required(login_url="login")
def meet(request):
    if request.method == 'POST':
        try:
            # Retrieve and process data
            course_id = int(request.POST.get('post'))
            round_selected = request.POST.get('round')
            difficulty_selected = request.POST.get('difficulty')
            interviewer_selected = request.POST.get('interviewer') + ".mp4"
            
            obj = get_object_or_404(JobPost, id=course_id)
            comp = get_object_or_404(Company, name=obj.company)

            question = [round_selected, difficulty_selected, obj, comp.name]
            result = get_gemini_response(question, 'Q')

            # Greet based on time
            current_time = datetime.now()
            section = "Good morning" if current_time.hour < 12 else "Good afternoon"
            greeting=f"{section} and thank you for joining us today! I'm looking forward to our conversation and learning more about your background and experiences. Let's get started whenever you're ready.,"
             
            result = greeting + result

            lst = result.split(',')

            # Store meeting data in Django session
            request.session['meeting_data'] = {
                'company': comp.name,
                'post': obj.id,
                'interviewer': interviewer_selected,
                'questions': lst
            }

            context = {
                'data': lst,
                'company': comp,
                'post': obj,
                'interviewer': interviewer_selected,
            }

            return render(request, "PrepMate_meet.html", context=context)

        except Exception as e:
            print(f"Error: {e}")
            return HttpResponse(f"Error: {str(e)}")
    
    else:
        # If page reloads, retrieve session data and restore it
        meeting_data = request.session.get('meeting_data')
        if meeting_data:
            obj = get_object_or_404(JobPost, id=meeting_data['post'])
            comp = get_object_or_404(Company, name=meeting_data['company'])

            context = {
                'data': meeting_data['questions'],
                'company': comp,
                'post': obj,
                'interviewer': meeting_data['interviewer'],
            }

            return render(request, "PrepMate_meet.html", context=context)

        return HttpResponse("This page only handles POST requests.")

    
    
@csrf_exempt
def getData(request):
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method. Please use POST.'}, status=400)

    try:
        data = json.loads(request.body)
        # Validate input
        print(f"Title:{data['title']}\nHistory:{data['history']}\nResponse:{data['company']}")
        
        if 'company' not in data or 'title' not in data:
            return JsonResponse({'error': 'Missing parameters.'}, status=400)

        # response="This is response"
        question=[ data['title'], data['company'], data['history']]
        response = get_gemini_response(question,'A')  # Processing the conversation to get the 'response'
        # response ="---------------- Respose Willl come here ---------------------"
        # Store data in session
        print(response)
        response=response.replace("```html", "").replace("```", "")
        request.session['company'] = data['company']
        request.session['response'] = response
        request.session['title'] = data['title']
        request.session['history'] = data['history']
        user=request.user
        company=Company.objects.get(name=data['company'])
        job=JobPost.objects.get(title=data['title'],company=company)
        print()
        Interview.objects.create(
            user=user,
            job=job,
            conversation=data['history'],
            ai_analysis=response,
        )
        
        
        # Delete the member after gathering necessary information
        
        
        print("Session updated with conversation and response.")

        # Now return a success response so that the frontend can handle redirection
        return JsonResponse({'success': True})

    except json.JSONDecodeError:
        return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
    
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    

def getAnalysis(request):
    company = request.session.get('company')
    response = request.session.get('response')
    title = request.session.get('title')
    history = request.session.get('history')
    

    # Extract content between <body> and </body> tags
    if not company or not response or not history or not title:
        return HttpResponseBadRequest("Required session data is missing.")

    print(f"Company: {company}, Response: {response}, History: {history}, Title:{title}")
    # print("***************************************************************")
   
    response = response.replace("```html", "").replace("```", "")
    
    context = {
        'company': company,
        'response': response,
        'title':title,
        'history': history
    }

    return render(request, 'PrepMate_analysis.html', context=context)

def everyAnalysis(request,interview_id):
    data = get_object_or_404(Interview, id=interview_id)
    company = data.job.company.name
    history = data.conversation
    response = data.ai_analysis
    title = data.job.title
    response = response.replace("```html", "").replace("```", "")
    context = {
        'company': company,
        'response': response,
        'title':title,
        'history': history
    }

    return render(request, 'PrepMate_analysis.html', context=context)


def about(request):
    return render(request, "about.html")
    