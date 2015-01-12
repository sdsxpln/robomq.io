"""
 * File: consumer.py
 * Description: This is the MQTT consumer handles incoming messages
 *     published by producers from a particular topic.
 *     Consumer prints the topic and payload as it receives messages.
 *
 * Author: Eamin Zhang
 * robomq.io (http://www.robomq.io)
"""

import sys
import paho.mqtt.client as mqtt

server = "localhost"
port = 1883
vhost = "/"
username = "guest"
password = "guest"
topic = "test"

"""
 * This method is the callback on connecting to broker.
 * @ It subscribes the target topic.
"""
def on_connect(client, userdata, rc):	#event on connecting
	try:
		client.subscribe([(topic, 1)])	#subscribe
	except:
		print("Error: Failed to subscribe")
		sys.exit(-1)

"""
 * This method is the callback on receiving messages.
 * @ It prints the message topic and payload on console.
"""
def on_message(client, userdata, message):	#event on receiving message
	print("Topic: " + message.topic + ", Message: " + message.payload)

try:
	client = mqtt.Client(client_id="", clean_session=True, userdata=None, protocol="MQTTv31")
	client.username_pw_set(vhost + ":" + username, password)
	client.on_connect = on_connect
	client.on_message = on_message
	client.connect(server, port, keepalive=60, bind_address="")	#connect
	client.loop_forever()	#loop forever
except:
	print("Error: Failed to connect and start loop")
	sys.exit(-1)

#client.unsubscribe(topic)
#client.disconnect()
