from models import *
from errorhandlers import *
from sqlalchemy.exc import IntegrityError
from flask import current_app

def ShowAllUsers():

	allusers = g.tenant_session.query(Users).all()
	output = []

	try:
		if allusers:
			for user in allusers:
				curruser = {}
				curruser['id'] = user.id
				curruser['name'] = user.name
				curruser['mail'] = user.mail
				curruser['mobile'] = user.mobile
				curruser['address'] = user.address
				output.append(curruser)
			return {'items': output}
		else:
			raise UserNotFound("No users found in the database")
	except UserNotFound as e:
		return e.msg


def AddUser(newuser):
	user = Users(
		name=newuser['name'],
		mail=newuser['mail'],
		mobile=newuser['mobile'],
		address=newuser['address'])
	try:
		g.tenant_session.add(user)
		g.tenant_session.commit()
		return "User added succesfully"

	except IntegrityError:
		raise DuplicateUser('User exists')

	return user


def DeleteUser(id):
	deluser = Users.query.filter_by(id=id).first()

	if deluser:
		g.tenant_session.delete(deluser)
		g.tenant_session.commit()
		return "User Deleted"
	else:
		raise UserNotFound("User not found with the id - "+ id)
	# except UserNotFound as e:
	# 	return e.msg

def UpdateUser(newDetails, id):
	up_record = Users.query.filter_by(id=id).first()
	print(up_record.email, newDetails['emailAddress'])
	try:
		if (up_record.email != newDetails['emailAddress'] or
			up_record.mobile != newDetails['mobileNumber'] or
			up_record.username != newDetails['userName'] or
			up_record.address != newDetails['address']):

			up_record.email = newDetails['emailAddress'],
			up_record.mobile = newDetails['mobileNumber'],
			up_record.username = newDetails['userName'],
			up_record.address = newDetails['address']

			g.tenant_session.add(up_record)
			g.tenant_session.commit()

			return "User updated successfully"
		else:
			raise User_already_exists("No different values found to update the " + newDetails['userName'] + " user")

	except 	User_already_exits as e:
		return e.msg




def SearchUser(mobile):
	getuser = Users.query.filter_by(mobile=mobile).first()

	try:
		if not getuser:
			return {'items': getuser}
		else:
			raise UserNotFound("No users found with the mobile number - "+ str(mobile))
	except UserNotFound as e:
		return e.msg


