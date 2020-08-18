from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms 

from .models import EmployeeUser, EmployeeEntry
from .services import PasswordService, EmployeeService

#python imports
import re


#Manual form
class EmployeeRegisterForm(forms.ModelForm):
	class Meta:
		model = EmployeeUser
		fields = ['email','employeeid','ename', 'age','mobileno']
	ename = forms.CharField(label = 'title', widget=forms.TextInput(attrs={"placeholder":"Employee Name..."}))
	age = forms.IntegerField(label = 'age', widget=forms.NumberInput(attrs={"placeholder":"Age..."}))
	email = forms.EmailField(label = 'email',max_length=150, widget=forms.EmailInput(attrs={"placeholder":"Email..."}))
	password = forms.CharField(label = 'password', required=False, max_length=32, widget=forms.PasswordInput(attrs={"placeholder":"Password..."}))
	mobileno = forms.CharField(label = 'mobile no', widget=forms.TextInput(attrs={"placeholder":"Mobile No..."}))
	employeeid = forms.CharField(label = 'employeeid',required=False)

	def clean_password(self,*args,**kwargs):
		password = PasswordService().generatePass()
		#print("[FORMS] Password:",password)	#debug
		
		return password

	def clean_mobileno(self):
		mobileno = self.cleaned_data.get('mobileno')

		pattern = re.compile("[7-9][0-9]{9}")
		if pattern.match(mobileno):
			return mobileno
		else:
			raise forms.ValidationError("Not a Valid Mobile No")

	def clean_employeeid(self, *args, **kwargs):
		last_emp = EmployeeUser.objects.all().last()
		last_id = last_emp.id
		last_id += 1
		employeeid = 'EMP202000'+str(last_id)
		
		return employeeid


class EmployeeEntryForm(forms.ModelForm):
	class Meta:
		model = EmployeeEntry
		fields = ['email', 'date', 'intime', 'outtime']

	email = forms.EmailField(label='email', max_length=50, widget=forms.EmailInput(attrs={"placeholder":"Employee Email..."}))
	date = forms.DateField(label='date', widget=forms.DateInput(attrs={"placeholder":"Date..."}))
	intime = forms.TimeField(label='intime', widget=forms.TimeInput(attrs={"placeholder":"In Time..."}))
	outtime = forms.TimeField(label='outtime', widget=forms.TimeInput(attrs={"placeholder":"Out Time..."}))

	def clean_date(self):
		email = self.cleaned_data.get('email')
		date = self.cleaned_data.get('date')
		#intime = self.cleaned_data.get()
		print(email, date)

		empsc = EmployeeService()
		if not empsc.entryExistsForDate(email, date):
			return date
		else:
			raise forms.ValidationError("Entry exists for date:"+str(date))



