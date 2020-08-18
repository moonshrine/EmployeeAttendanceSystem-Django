from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
# Create your models here.

# class Employee(models.Model):
# 	ename = models.CharField(max_length=120, null= False)
# 	age = models.PositiveIntegerField()
# 	email = models.EmailField(max_length=150)
# 	password = models.CharField(max_length=32)
# 	mobileno = models.CharField(max_length=10)
# 	last_login = models.CharField(max_length=150)

class MyEmployeeManager(BaseUserManager):
	def create_user(self, email, employeeid, password=None):
		if not email:
			raise ValueError("User must have an email")
		if not employeeid:
			raise ValueError("User must have an employeeid")

		user = self.model(
				email=self.normalize_email(email),
				employeeid=employeeid,
			)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, email, employeeid, password):
		user = self.create_user(
				email=self.normalize_email(email),
				employeeid=employeeid,
				password=password,
			)

		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True

		user.save(using=self._db)
		return user



class EmployeeUser(AbstractBaseUser):
	email = models.EmailField(name="email", max_length=60,unique=True)
	employeeid = models.CharField(max_length=30, unique=True)
	
	password = models.CharField(max_length=150)
	ename = models.CharField(max_length=30, null=False)
	age = models.PositiveIntegerField(null=True)
	mobileno = models.CharField(max_length=10)
	entry = models.TextField(null=True)

	date_joined = models.DateTimeField(name='date joined', auto_now_add=True)
	last_login = models.DateTimeField(name='last login', auto_now=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['employeeid']

	objects = MyEmployeeManager()

	def has_perm(self, perm, obj=None):
		return self.is_admin

	def has_module_perms(self, app_label):
		return True

	def __str__(self):
		return self.email
	
	def get_absolute_url(self):
		return f"/employee/{self.id}"

class EmployeeEntry(models.Model):
	email = models.EmailField(max_length=50)
	date = models.DateField()
	intime = models.TimeField()
	outtime = models.TimeField()


	def __str__(self):
		return self.email