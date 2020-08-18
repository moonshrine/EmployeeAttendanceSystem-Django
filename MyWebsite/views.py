from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
#from django.contrib.auth.forms import UserCreationForm
from .models import EmployeeUser
from .forms import EmployeeRegisterForm, EmployeeEntryForm

#own imports
from .services import SMSService, EmailService, PasswordService, EmployeeService

#python imports
import threading, datetime



# Create your views here.
@login_required(login_url='home')
def employee_entry_view(request, *args, **kwargs):

	if request.user.is_authenticated and request.user.is_superuser:
		form = EmployeeEntryForm()

		if request.method == 'POST':
			form = EmployeeEntryForm(request.POST)
			if form.is_valid():
				print('Valid form :',form.cleaned_data)
				empsc = EmployeeService()
				email = form.cleaned_data.get('email')
				date = form.cleaned_data.get('date')
				intime = form.cleaned_data.get('intime')
				outtime = form.cleaned_data.get('outtime')

				datetime1 = datetime.datetime.combine(date, intime)
				datetime2 = datetime.datetime.combine(date, outtime)

				ttime = datetime2 - datetime1
				print('\n\tttime: ',ttime)
				empsc.addEntry(email, date, intime, outtime, ttime)

				form = EmployeeEntryForm()
				messages.success(request, 'Entry added successfully!!')
		
		context = {'form':form}
		return render(request, 'entry.html', context)

	else:
		return redirect('adminhome')


def template_view(request):
	#test view may delete later

	context ={'name': 'Moonshrine', 'location':'Bhayander east'}
	return render(request, 'template_test.html', context)


@login_required(login_url='home')
def register_user_view(request, *args, **kwargs):
	
	if request.user.is_superuser:
		form = EmployeeRegisterForm()
		if request.method == 'POST':
			form = EmployeeRegisterForm(request.POST)
			if form.is_valid():
				print("Valid form submission, Info: ",form.cleaned_data)
				ename = form.cleaned_data.get('ename')
				email = form.cleaned_data.get('email')
				password = form.cleaned_data.get('password')

				mail_subject = 'Digital Bunny Studios'
				mail_content = 'Hello, '+ename+'\nYour Profile successfully added to the system!\nAnd your login password is:'+password

				email = EmailService(email, ename, mail_subject, mail_content)
				threading.Thread(target=email.sendMail).start()

				SMS = SMSService('New Employee Added!\nEmployee Info:'+str(form.cleaned_data))
				threading.Thread(target=SMS.sendMessage).start()
				#form.save()	#form.save() does not save generated password so use create objects
				
				user = EmployeeUser.objects.create(**form.cleaned_data)
				user.set_password(password)
				user.save()

				form = EmployeeRegisterForm()
				messages.success(request,'Employee ' +ename+ ' Added!!')
			else:
				print("Not valid form",form.errors)

		context = {'form':form}
		return render(request, "register_user.html",context)

	else:
		print("[VIEWS] User is not superuser")
		url = 'employee/'+str(request.user.id)
		return redirect(url)


def login_view(request, *args, **kwargs):

	if request.user.is_authenticated:
		return redirect('adminhome')

	else:
		if request.method == 'POST':
			email = request.POST.get('uname')
			password = request.POST.get('pass')
			
			print("Email: ",email)
			print("Password: ",password)

			user = authenticate(request, email=email, password=password)
			print(user)
			if user is not None:
				login(request, user)
				print('Current login user',request.user.ename)
				if request.user.is_superuser:
					return redirect('adminhome2')
				else:
					url = 'employee/'+str(request.user.id)
					return redirect(url)
			else:
				messages.info(request, 'Email OR Password is wrong!')

		context = {'logined':False}
		return render(request, "home.html",context)


@login_required(login_url='home')
def logout_view(request):
	logout(request)
	return redirect('home')

@login_required(login_url='home')
def admin_home_view(request, *args, **kwargs):
	emps = EmployeeUser.objects.all().exclude(is_superuser=True)

	context = {'employees':emps}
	return render(request, "admin_home.html", context)


@login_required(login_url='home')
def admin_home_view2(request, *args, **kwargs):
	
	AllEmployees = EmployeeService().getEmployees()
	print(AllEmployees)
	context = {'Employees':AllEmployees}
	return render(request, "admin_home2.html", context)

@login_required(login_url='home')
def employee_view(request, id):
	if not request.user.is_superuser:
		id = request.user.id
	#emp = EmployeeUser.objects.get(id=id)
	emp = get_object_or_404(EmployeeUser, id=id)

	entries = EmployeeService().retrieveEntries(emp.email)
	#print('entries:----->',entries)
	context = {'emp':emp, 'entries':entries}

	return render(request, "employee.html", context)


@login_required(login_url='home')
def update_profile_view(request,*args,**kwargs):

	info = []
	info.append(request.POST.get('pass1'))
	info.append(request.POST.get('pass2'))
	info.append(request.POST.get('otp'))
	print('Update profile info: ',info)
	return render(request, 'update_profile.html',{})
