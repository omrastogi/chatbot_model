from flask import Flask, render_template, session
from flask_socketio import SocketIO
import tensorflow
from Talk import ask


print ("This is socket file")
app = Flask(__name__)
app.config['SECRET_KEY'] = 'vnkdjnfjknfl1232#'
socketio = SocketIO(app)

## Config MySQL
# mysql = MySQL()
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'chatbotdb'
# app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

# # Initialize the app for use with this MySQL class
# mysql.init_app(app)

#starting point for the app, every time the page is open, session is called.
@app.route('/')
def sessions():
	session['greetings'] = True
	return render_template('session1.html')

# This is much needed 
def messageReceived(methods=['GET', 'POST']):
	print('message was received!!!')

# Whenever user writes a message 
@socketio.on('my event')
def handle_my_custom_event(json, methods=['POST']):
	try:
		socketio.emit('my response', json, callback=messageReceived)
		# Sender('checking logs')			
		bot(json['message'])
	except:
		pass


def bot(message):
	if session['greetings'] == False:		
		reply = ask(str(message))
		Sender(reply)
	else: 
		greet(message)


def Sender(message):
	json = {'user_name': '', 'message': ''}
	json['user_name'] = "Bot"
	json['message'] = message
	socketio.emit('my response', json, callback=messageReceived)


def greet(message):
	if session['greetings'] == True:
		reply = ask(str(message))
		Sender(reply)

		reply = "Please let me know your name"
		session['greetings'] = 'Name'
		Sender(reply)
	 


	elif session['greetings'] == 'Name':
		if Isname(message):
			name = message
			session['greetings'] = 'Mail'
			reply = 'Hello '+name+', please give us your email'
			Sender(reply)


	elif session['greetings'] == 'Mail':
		mail = message 
		session['greetings'] = False
		reply = 'Thankyou.....' 
		Sender(reply)
		Sender('How may I help you')


def Isname(name):
	negation = ['No','no','Nope','nope','Neither','None','nah']
	if name in negation:
		session['greetings'] = False
		Sender ("I respect your choice to be anonymous")
		Sender ("Please ask as many questions as you like")
		return False

	return True





if __name__ == '__main__':
	socketio.run(app, debug=True)
	# socketio.run(app, debug=True, host = '0.0.0.0')
	