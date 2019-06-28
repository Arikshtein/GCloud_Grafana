from google.cloud import pubsub_v1
import keyboard as kb
from pynput import keyboard
from pynput import mouse
import re
import json 
from datetime import datetime
import ctypes

apps = '(Visual Studio)|(Facebook)|(YouTube)|(Power BI)|(Sublime Text)|(Microsoft Edge)|(Skype)|(Management Studio)|(DataGrip)|(Chrome)'
buttons = {'Button.left': 1, 'Button.right': 2, 'Button.middle': 3}
project_id = "optimum-pier-188814"
publisher = pubsub_v1.PublisherClient.from_service_account_json(r'C:\Users\proshyan\Documents\BigData\Keys\prooducer.json')
topic_path_keys = 'projects/optimum-pier-188814/topics/keys-4'
topic_path_clicks = 'projects/optimum-pier-188814/topics/clicks-4'

def map_apps(current_app):
	m = re.search(apps, current_app)
	if m is None:
		return 'Other'
	else:
		return m[0]


def get_current_app_title():
	active = ctypes.windll.user32.GetForegroundWindow()
	length = ctypes.windll.user32.GetWindowTextLengthW(active)
	# ctypes.windll.user32.GetWindowTextW(active)
	buff = ctypes.create_unicode_buffer(length + 1)
	ctypes.windll.user32.GetWindowTextW(active, buff, length + 1)
	return buff.value

def listen_keyboard(key):
	purekey = str(key).replace("'", '', 2)
	if ((purekey in 'aeouiycv')):
		is_shift_pressed = True if kb.is_pressed('shift') else False
		is_ctrl_pressed = True if kb.is_pressed('ctrl') else False
		a = {'key': purekey, 
				'shift': is_shift_pressed, 
				'ctrl' : is_ctrl_pressed,
				'timestamp': datetime.utcnow().strftime(r'%Y-%m-%dT%H:%M:%SZ'),
				'active_window': map_apps(get_current_app_title())
			} 
		data=json.dumps(a).encode('utf-8')
		publisher.publish(topic_path_keys, data=data)
		with open(r'C:\Users\proshyan\Documents\aaa.txt', 'a') as the_file:
			the_file.write(json.dumps(a) + '\n')


def listen_mouse(x,y,button, pressed):
	if (pressed):
		a = {'button': buttons.get(str(button),0), 
				'timestamp': datetime.utcnow().strftime(r'%Y-%m-%dT%H:%M:%SZ'),
				'active_window': map_apps(get_current_app_title())
			} 
		data=json.dumps(a).encode('utf-8')
		publisher.publish(topic_path_clicks, data=data)
		with open(r'C:\Users\proshyan\Documents\bbb.txt', 'a') as the_file:
			the_file.write(json.dumps(a) + '\n')



a = keyboard.Listener(on_press = listen_keyboard)
a.start()
b = mouse.Listener(on_click = listen_mouse)
b.start()

a.join()

#and(str(key) in 'aeoui') or  ( 'Key' in (str(key))) 