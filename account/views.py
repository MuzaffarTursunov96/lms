from django.shortcuts import render,redirect
from .models import User
from django.contrib import auth
from .decorators import unauthenticated_user
from django.contrib.auth.decorators import login_required
from lms.models import UserCourses
from django.core.paginator import Paginator




@unauthenticated_user
def login(request):
  if request.method =='POST':
    email =request.POST.get('email',None)
    password =request.POST.get('password',None)
    remember = request.POST.get('remember_me', None)

    user = auth.authenticate(email=email,password=password)
    if user is not None:
      auth.login(request,user)
      if remember:
          request.session.set_expiry(1209600)  
      else:
          request.session.set_expiry(0)
      return redirect('index')
    else:
      request.session['login_failed'] = True
      return redirect('login')
  return render(request,'account/login.html')

def logout(request):
  auth.logout(request)
  return redirect('login')



@unauthenticated_user
def registerUser(request):
  if request.method =='POST':
    username = request.POST.get('username')
    firstname = request.POST.get('firstname')
    lastname = request.POST.get('lastname')
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User()
    user.first_name = firstname
    user.last_name = lastname
    user.username = username
    user.email =email
    user.set_password(password)
    user.save()
    return redirect('login')
  else:
    return render(request,'account/register.html')
  
@login_required(login_url='login')  
def my_courses(request):
    query = request.GET.get('q', '')
    if query:
        courses = UserCourses.objects.filter(user = request.user,course__title__icontains=query)
    else:
        courses = UserCourses.objects.filter(user = request.user)

    paginator = Paginator(courses, 12)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'courses': page_obj,
    }
    return render(request,'course/my-courses.html',context)