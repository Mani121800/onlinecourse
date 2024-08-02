from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import UserProfile
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import EmailLoginForm
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from .models import UserProfile

@csrf_exempt
def SignupPage(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        email = request.POST.get('email')
        pass1 = request.POST.get('password1')
        pass2 = request.POST.get('password2')

        # Validate password match
        if pass1 != pass2:
            return render(request, 'signup.html', {'error_message': "Your password and confirm password are not the same!"})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error_message': "Email already exists. Please use a different email address."})
   
    #  # Check if the email is in the Record_Landingpage model
        # if not Record_Landingpage.objects.filter(email=email).exists():
        #     return redirect('add_record_landingpage') 
    #    # Validate unique username
        try:
            user = User.objects.create_user(username=uname, email=email, password=pass1)
            user.save()
            UserProfile.objects.create(user=user, flag=0)  # Adjust this according to your UserProfile model
            return redirect('login')  # Replace 'login' with the name of your login URL pattern
        except IntegrityError as e:
            if 'UNIQUE constraint failed: auth_user.username' in str(e):
                return render(request, 'signup.html', {'error_message': "Username already exists. Please choose a different username."})
            else:
                return render(request, 'signup.html', {'error_message': "An error occurred. Please try again."})

        except Exception as e:
            return render(request, 'signup.html', {'error_message': "An unexpected error occurred. Please try again."})

    return render(request, 'signup.html')      




@login_required(login_url='login')
def HomePage(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Fetch the course link based on the batch number
    # course_links = CourseLinks.objects.filter(batch_number=user_profile.batch_number).first()

    context = {
        'user_profile': user_profile,
        'flag': user_profile.flag,
        # 'Course_Links': course_links,
        'batch_number': user_profile.batch_number,
       
    }
    
    # Check if course_links exists before passing it to the template
    # if course_links:
    #     context['course_detail_url'] = reverse('course_detail', args=[course_links.id])
    
    return render(request, 'home2.html', context)

@login_required(login_url='login')
def req_view(request):
    return render(request, 'req.html')
def LoginPage(request):
    if request.method == 'POST':
        form = EmailLoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.flag == 0:
                        return redirect('req')
                    else:
                        return redirect('home2')
                except UserProfile.DoesNotExist:
                    return render(request, 'login.html', {'form': form, 'error': 'User profile not found.'})
            else:
                return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password.'})
    else:
        form = EmailLoginForm()

    return render(request, 'login.html', {'form': form})



def LogoutPage(request):
    logout(request)
    return redirect('login')

from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def course_view(request, course_id):
    # Fetch the course and videos based on the course_id
    course = get_object_or_404(Course, id=course_id)
    videos = Video.objects.filter(course=course)

    context = {
        'course': course,
        'videos': videos,
        'user': request.user,  # Pass the user object to the template
    }

    return render(request, 'course.html', context)





from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse,reverse_lazy
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from django.views.generic.edit import FormView

class CustomPasswordResetView(FormView):
    template_name = 'password_reset_form.html'
    success_url = reverse_lazy('password_reset_done')  # Use named URL here
    form_class = PasswordResetForm

    def form_valid(self, form):
        email = form.cleaned_data['email']
        users = User.objects.filter(email=email)
        if users.exists():
            for user in users:
                current_site = get_current_site(self.request)
                subject = 'Password Reset Requested'
                message = render_to_string('password_reset_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user),
                    'protocol': 'https' if self.request.is_secure() else 'http',
                })
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
        return super().form_valid(form)
    

from django.views.generic.edit import FormView
from .forms import FileFieldForm


class FileFieldFormView(FormView):
    form_class = FileFieldForm
    template_name = "upload.html"  # Replace with your template.
    success_url = "..."  # Replace with your URL or reverse().

    def form_valid(self, form):
        files = form.cleaned_data["file_field"]
        for f in files:
            ...  # Do something with each file.
        return super().form_valid(form)
    
    
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Course, Video, UserProfile

@login_required(login_url='login')
def course_detail(request):
    user_profile = request.user.userprofile
    # Filter courses based on the user's batch number
    courses = Course.objects.filter(batch_number=user_profile.batch_number)

    if courses.exists():
        course = courses.first()
        videos = Video.objects.filter(course=course).order_by('order')
    else:
        return HttpResponseForbidden("You do not have access to this course.") 

    context = {
        'course': course,
        'videos': videos,
        'batch_number': course.batch_number  # Add batch number to context
    }
    return render(request, 'vid.html', context)
