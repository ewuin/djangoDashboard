# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
import bcrypt
from .models import *
# Create your views here.

def index(request):
    r="test"
    return render(request,'dashboardApp/index.html')

def signin(request):
    return render (request, 'dashboardApp/signin.html')

def process_signin(request):

    emailTC=request.POST['emailTC'].strip().lower()
    passwordTC=request.POST['passwordTC'].strip()

    if len(emailTC)<1:
        print "missing email entry"
        messages.add_message(request,messages.ERROR,"invalid username or password")
        return redirect ('/signin')

    user_found=User.objects.filter(email=emailTC)
    print user_found
    if len(user_found)==1:
        user_found=user_found[0]
        verified_user=True
    elif len(user_found)==0:
        verified_user=False
        messages.add_message(request,messages.ERROR,"Email not found. Would you like to register?")
        return redirect ('/signin')
    elif len(user_found)>1:
        verified_user=False
        print "database error"
        messages.add_message(request, messages.ERROR,"database error, contact site admin")
        return redirect('/')
    else:
        print "programming error in verifying user"
        messages.add_message(request, messages.ERROR,"programming error, contact site admin")
        return redirect('/')

    if verified_user:
        password_in_db=user_found.password.encode()
        password_good=bcrypt.checkpw(passwordTC.encode(), password_in_db)

    if verified_user and password_good:
        request.session['id']=user_found.id
        request.session['userLevel']=user_found.userLevel
        context = {'User':User.objects.all().values('id','firstName','lastName','email','created_at','userLevel','description')}

        if user_found.userLevel=="admin":
            return render(request,'dashboardApp/dashboard-admin.html',context)
        elif user_found.userLevel=="normal":
            return render(request,'dashboardApp/dashboard.html',context)
    elif not password_good:
        messages.add_message(request,messages.ERROR,"invalid username or password")
        return redirect('/signin')
    else:
        print "programming error in verifying password"
        messages.add_message(request, messages.ERROR,"programming error, contact site admin")
        return redirect('/')

def register(request):
    return render(request, 'dashboardApp/register.html')

def process_addbyadmin(request):
    fnameTA=request.POST['fnameTA'].strip()
    lnameTA=request.POST['lnameTA'].strip()
    emailTA=request.POST['emailTA'].strip().lower()
    passwordTA=request.POST['passwordTA'].strip()
    confirm_passwordTA=request.POST['confirm_passwordTA'].strip()
    userLevelTA=request.POST['userLevelTA']
    if not fnameTA or not lnameTA or not emailTA or not passwordTA or not confirm_passwordTA:
        messages.add_message(request,messages.ERROR,"all data fields are required")
        messages.add_message(request,messages.ERROR,"User NOT added!! TRY AGAIN.")
        context = {'User':User.objects.all().values('id','firstName','lastName','email','created_at','userLevel','description')}
        return render(request,'dashboardApp/dashboard-admin.html',context)
    status=attempt_add(request,fnameTA,lnameTA,emailTA,passwordTA,confirm_passwordTA,userLevelTA)

    if status=="success":
        password_hashed = bcrypt.hashpw(passwordTA.encode(), bcrypt.gensalt())
        User.objects.create(firstName=fnameTA.title(),lastName=lnameTA.title(),email=emailTA,password=password_hashed,userLevel=userLevelTA)
        context = {'User':User.objects.all().values('id','firstName','lastName','email','created_at','userLevel','description')}
        messages.add_message(request,messages.ERROR,"Successfully added")
        return render(request,'dashboardApp/dashboard-admin.html',context)
    else:
        messages.add_message(request,messages.ERROR,"User NOT added!! TRY AGAIN.")
        context = {'User':User.objects.all().values('id','firstName','lastName','email','created_at','userLevel','description')}
        return render(request,'dashboardApp/dashboard-admin.html',context)


def attempt_add(request,fnameTA,lnameTA,emailTA,passwordTA,confirm_passwordTA,userLevelTA):
#check if email already registered
    email_exists=User.objects.filter(email=emailTA)
    if len(email_exists)>0:
        print "email already has registered account"
        messages.add_message(request,messages.ERROR,"this email is already regiestered")
        return "Email already registered"
    #check that passwords match
    if passwordTA == confirm_passwordTA:
        pw_match=True
    else:
        pw_match=False
        print "passwords must match"
        return "passwords dont match"
    #perform all validations
    if pw_match:
        pw_error=User.objects.pw_validator(passwordTA)

    email_error=User.objects.email_validator(emailTA)
    fname_error=User.objects.name_validator(fnameTA)
    lname_error=User.objects.name_validator(lnameTA)
    reg_errors=[pw_error,email_error,fname_error,lname_error]
    print email_error,fname_error,lname_error
    for error in reg_errors:
        messages.add_message(request,messages.ERROR,error)
    if len(pw_error)+len(email_error)+len(fname_error)+len(lname_error)==0:
        return "success"
    else:
        return "validation errors"



def process_registraion(request):
#gather post data
    fnameTA=request.POST['fnameTA'].strip()
    lnameTA=request.POST['lnameTA'].strip()
    emailTA=request.POST['emailTA'].strip().lower()
    passwordTA=request.POST['passwordTA'].strip()
    confirm_passwordTA=request.POST['confirm_passwordTA'].strip()
    if not fnameTA or not lnameTA or not emailTA or not passwordTA or not confirm_passwordTA:
        messages.add_message(request,messages.ERROR,"all data fields are required")
        return redirect('/register')

#check if email already registered
    email_exists=User.objects.filter(email=emailTA)
    if len(email_exists)>0:
        print "email already has registered account"
        messages.add_message(request,messages.ERROR,"this email is already regiestered")
        return redirect('/register')
    #check that passwords match
    if passwordTA == confirm_passwordTA:
        pw_match=True
    else:
        pw_match=False
        print "passwords must match"
        return redirect('/')
    #perform all validations
    if pw_match:
        pw_error=User.objects.pw_validator(passwordTA)

    email_error=User.objects.email_validator(emailTA)
    fname_error=User.objects.name_validator(fnameTA)
    lname_error=User.objects.name_validator(lnameTA)
    reg_errors=[pw_error,email_error,fname_error,lname_error]
    print email_error,fname_error,lname_error
    for error in reg_errors:
        messages.add_message(request,messages.ERROR,error)

    if User.objects.count()==0:
        userLevelTA="admin"
    else:
        userLevelTA="normal"

    #commit to database if all is well, encrypt password
    if len(pw_error)+len(email_error)+len(fname_error)+len(lname_error)==0:
        password_hashed = bcrypt.hashpw(passwordTA.encode(), bcrypt.gensalt())
        User.objects.create(firstName=fnameTA.title(),lastName=lnameTA.title(),email=emailTA,password=password_hashed,userLevel=userLevelTA)
        context = {'User':User.objects.all().values('id','firstName','lastName','email','created_at','userLevel','description')}
        new_user=User.objects.get(email=emailTA)
        request.session['id']=new_user.id
        request.session['userLevel']=new_user.userLevel
        if userLevelTA=="admin":
            return render(request,'dashboardApp/dashboard-admin.html',context)
        elif userLevelTA=="normal":
            return render(request,'dashboardApp/dashboard.html',context)
    else:
        return redirect('/register')


def add_by_admin(request):
    return render(request,'dashboardApp/add-by-admin.html')

def edit_user(request, user_id):
    context={'user':User.objects.get(id=user_id)}
    if request.session['userLevel']=="admin":
        return render(request,'dashboardApp/edit-user-admin.html',context)
    elif request.session['userLevel']=="normal":
        return render(request,'dashboardApp/edit_user.html',context)
    else:
        messages.add_message(request,messages.ERROR,"There has been an error. You have been logged out.")
        request.session.clear()
        return redirect('/')

def process_edit(request,user_id):
    userTE=User.objects.get(id=user_id)
    #print userTE.first_name
    #get and clean form data
    f_nameTE=request.POST['fnameTE'].strip()
    l_nameTE=request.POST['lnameTE'].strip()
    emailTE=request.POST['emailTE'].lower().strip()
    pw_TE1=request.POST['passwordTE'].strip()
    pw_TE2=request.POST['confirm_passwordTE'].strip()
    descTE=request.POST['descriptionTE']

    if request.session['userLevel']=="admin":
        userLevelTE=request.POST['userLevelTE']
        if userLevelTE != "NoChange":
            userTE.userLevel=userLevelTE

    if len(descTE)>0:
        userTE.description=descTE

    if f_nameTE:
        fname_error=User.objects.name_validator(f_nameTE)
        if fname_error:
            print fname_error
            messages.add_message(request,messages.ERROR,"Your first name has NOT been changed")
        elif not fname_error:
            userTE.firstName=f_nameTE.title()
            messages.add_message(request,messages.ERROR,"Your first name has been changed")
    if l_nameTE:
        lname_error=User.objects.name_validator(l_nameTE)
        if lname_error:
            print lname_error
            messages.add_message(request,messages.ERROR,"Your last name has not been changed")
        elif not lname_error:
            userTE.lastName=l_nameTE.title()
            messages.add_message(request,messages.ERROR,"Your last name has been changed")

    if emailTE:
        #if attempting to change email, check if not already taken
        email_exists=User.objects.filter(email=emailTE)
        if len(email_exists)>0:
            print "email already has registered account"
            messages.add_message(request,messages.ERROR,"this email is already regiestered")

        elif len(email_exists)==0:
            email_error=User.objects.email_validator(emailTE)
        if email_error:
            print email_error
            messages.add_message(request,messages.ERROR,"Your email has NOT been changed")
        elif not email_error and email_exists==0:
            userTE.email=emailTE
            messages.add_message(request,messages.ERROR,"Your email has been changed")


    #if form had new pw
    if pw_TE1:
        if pw_TE1 != pw_TE2:  #check that they match
            print "Your password has not been changed. They must match!"
            messages.add_message(request,messages.ERROR,"Your password has NOT been changed")

        elif pw_TE1 == pw_TE2:
            pass_error=User.objects.pw_validator(pw_TE1)
            if pass_error:
                print pass_error
                messages.add_message(request,messages.ERROR,"Your password has NOT been changed")

            elif not pass_error:
                password_hashed = bcrypt.hashpw(passwordTA.encode(), bcrypt.gensalt())
                userTE.password= password_hashed
                messages.add_message(request,messages.ERROR,"Your password has been changed!!")
        else:
            messages.add_message(request,messages.ERROR,"Your password has NOT been changed")
    userTE.save()
    context = {'User':User.objects.all().values('id','firstName','lastName','email','created_at','userLevel','description')}
    if request.session['userLevel']=="admin":
        return render(request,'dashboardApp/dashboard-admin.html',context)
    elif request.session['userLevel']=="normal":
        return render(request,'dashboardApp/dashboard.html',context)
    else:
        messages.add_message(request,messages.ERROR,"There has been an error. You have been logged out.")
        request.session.clear()
        return redirect('/')


def see_dashboard(request, user_id):
    context = {'User':User.objects.all().values('id','firstName','lastName','email','created_at','userLevel','description')}
    if request.session['userLevel']=="admin":
        return render(request,'dashboardApp/dashboard-admin.html',context)
    elif request.session['userLevel']=="normal":
        return render(request,'dashboardApp/dashboard.html',context)
    else:
        messages.add_message(request,messages.ERROR,"There has been an error. You have been logged out.")
        request.session.clear()
        return redirect('/')
