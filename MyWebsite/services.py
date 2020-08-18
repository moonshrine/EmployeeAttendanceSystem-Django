from .models import EmployeeUser

from twilio.rest import Client #sms api import
#email service imports
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import random, ast


#!!!All the print statement are for debug only, 
#!!!may delete them in final project until and unless stated expicitly

class SMSService():
	def __init__(self, message_content):
		self.msg_content = message_content
		self.account_sid = '*******************************'
		self.auth_token = '*******************************'
		self.client = Client(self.account_sid,self.auth_token)

	def sendMessage(self):
		try:
			message = self.client.messages \
								.create(
									body="Hello Moonshrine,\n"+self.msg_content,
									from_='+1347789****',
									to='+91*********'
								)
			print("SMS Sent, ID:",message.sid)
		except:
			print("[ERROR] can't send message to this Number")


class EmailService():
	def __init__(self, recv_address, recv_name, subject, content):
		self.recv_address = recv_address
		self.recv_name = recv_name
		self.subject = subject
		self.content = content	

		self.sender_address = 'noreply*******@gmail.com'
		self.sender_pass = '**********'

	def sendMail(self):
		try:
			#setup the MIME
			message = MIMEMultipart()
			message['From'] = self.sender_address
			message['To'] = self.recv_address
			message['Subject'] = self.subject
			#The mail body and attachments
			message.attach(MIMEText(self.content, 'plain'))
			#Create SMTP session for sending mail
			session = smtplib.SMTP('smtp.gmail.com', 587)	#using gamil with port 5887
			#Enable security
			session.starttls()
			#Login with email and pass
			session.login(self.sender_address, self.sender_pass)
			text = message.as_string()
			session.sendmail(self.sender_address, self.recv_address, text)
			session.quit()
			print('Mail Sent To||',self.recv_address,'|| Successfully!')
		except:
			print("ERROR: Could not send Mail")

class PasswordService():

	def __init__(self):
		self.digits = '0123456789'
		self.chars = 'abcdefghijklmnopqrstuvwxyz'
		self.password = ''
	
	def generatePass(self):
		for i in range(4):
			self.password += self.chars[random.randint(0,25)]
			self.password += self.digits[random.randint(0,9)]

		#print("[SERVICES]Generated Password",self.password)	#debug
		return self.password

class EmployeeService():
	def __init__(self):
		self.emp_col = 3		#no of employees to display in single row //Or no of emps in card-deck 
		#querying all Employees except superuser or admin
		self.QS = EmployeeUser.objects.all()
		#print(self.QS)

	def getEmployees(self):
		Employee_list = []
		temp_list = []
		# debug
		# print('----------------******------------------')
		# print('Emp list:', Employee_list)
		# print('temp list:', temp_list)
		# print('----------------******------------------')
	
		for i in range(1, len(self.QS)):
			if i%self.emp_col == 0 :
				temp_list.append(self.QS[i])
				Employee_list.append(temp_list)

				temp_list = []
			else:
				temp_list.append(self.QS[i])
			
			#debug
			#print('iteration:',i,'->',temp_list)
			#print('\n')
		Employee_list.append(temp_list)
		
		return Employee_list

	def entryExistsForDate(self, email, date):
		emp = EmployeeUser.objects.get(email=email)
		print('<----------entryExistsForDate check---------->')
		print(emp)
		
		data = emp.entry

		if data != None:
			entry_list = data.split(';')

			for entry in entry_list:
				entry = entry.split('/')
				print('Compare:------> entry[0]:{x}, date:{y}'.format(x= entry[0], y= date))
				if entry[0] == str(date):
					print('[SERVICES] entry for date:{d} already exist'.format(d= date))
					return True
			return False
		else:
			return False


	def addEntry(self, email, date, intime, outtime ,ttime):
		emp = EmployeeUser.objects.get(email = email)

		entry_str = ''
		old_entry = emp.entry
		
		entry_str = str(date) +'/'+ str(intime) +'/'+ str(outtime) +'/'+ str(ttime) 

		if old_entry is None:
			new_entry = str(entry_str)
		else:
			new_entry = str(old_entry) + ';' + str(entry_str)

		emp.entry = new_entry
		emp.save()

	def retrieveEntries(self, email):
		emp = EmployeeUser.objects.get(email=email)
		rtr_list = []
		#print('\nemp ====>',emp.entry)
		data = emp.entry
		#print('\ndata---->',data)
		if data is not None:
			entry_list = data.split(';')

			for entry in entry_list:
				x = entry.split('/')
				rtr_list.append(x)

		return rtr_list



