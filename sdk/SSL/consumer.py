# File: consumer.py
# Description: This is the AMQP SSL consumer handles incoming
#     communication from clients publishing messages to a broker server.
#     This example applies routing-key pattern out of 5 patterns.
#     It needs to acquire the public CA certificate to verify certificate of robomq.io.
#
# Author: Eamin Zhang
# robomq.io (http://www.robomq.io)

import pika
import time

server = "hostname"
port = 5671
vhost = "yourvhost" 
username = "username"
password = "password"
caCert = "http://www.tbs-x509.com/AddTrustExternalCARoot.crt"
exchangeName = "testEx"
queueName = "testQ1"
routingKey = "test"

#callback funtion on receiving messages
def onMessage(channel, method, properties, body):
	print body

while True:
	try:
		#connect
		credentials = pika.PlainCredentials(username, password)
		parameters = pika.ConnectionParameters(host = server, port = port, virtual_host = vhost, credentials = credentials, ssl=True, ssl_options={"ca_certs": caCert})
		connection = pika.BlockingConnection(parameters)
		channel = connection.channel()

		#declare exchange and queue, bind them and consume messages
		channel.exchange_declare(exchange = exchangeName, exchange_type = "direct", auto_delete = True)
		channel.queue_declare(queue = queueName, exclusive = True, auto_delete = True)
		channel.queue_bind(exchange = exchangeName, queue = queueName, routing_key = routingKey)
		channel.basic_consume(consumer_callback = onMessage, queue = queueName, no_ack = True)
		channel.start_consuming()
	except Exception, e:
		#reconnect on exception
		print "Exception handled, reconnecting...\nDetail:\n%s" % e
		try:
			connection.close()
		except:
			pass
		time.sleep(5)