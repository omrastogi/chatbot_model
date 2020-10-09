
import requests 
import json


def login():
	username = "omr"
	pas = "om1234"
	loc_lat = ""
	loc_lang = ""
	org_code = 2
	
	r = requests.post("http://www.sisoft.in/training/admin/webapi/ws-login.php", data = {
		'org_code':2,
		'username':username,
		'password':pas,
		'loc_lat':loc_lat,
		'loc_lang':loc_lang}) 
	print((r.text))
	token = (r.text).split(",")[-1].split(":")[-1].split('"')[1]
	
	return token



def load_data(token):
	phone_num = "8588988194"
	name = "om"
	city = "gzb"
	r = requests.post("http://www.sisoft.in/training/admin/webapi/ws-lead-add.php",data = {
		'org_code':2,
		'username':'omr',
		'name':name,
		'loc_lat':"34.3",
		'loc_lang':"12.1",
		'email':"omrastogi@gmail.com",
		'qry_type':"Course",
		'street':"Nitikhand-1",
		'sector':"--",
		'market':"--",
		'phone_num': phone_num,
		'city':city,
		'date':"28/june",
		'time':"12:30",
		'source':"mail",
		'comp_name':"Sisoft",
		'auth_token':token
		})
	print (r.text)
token = login()
load_data(token)

