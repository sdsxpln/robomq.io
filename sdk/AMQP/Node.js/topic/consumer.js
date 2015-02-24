/**
* File: consumer.js
* Description: This is the AMQP consumer handles incoming
*     communication from clients publishing messages to a broker server.
*     Messages can be received over AMQP exchange types including one-to-one,
*     from broadcast pattern, or selectively using specified binding key.
*
* Author: Stanley
* robomq.io (http://www.robomq.io)
*/

var amqp = require("amqp");

var server = "localhost";
var port = 5672;
var vhost = "/";
var username = "guest";
var password = "guest";
var exchangeName = "testEx";
var queueName = "testQ1";
var routingKey = "test.#";

var connection = amqp.createConnection({host: server, port: port, vhost: vhost, login: username, password: password});
connection.on("ready", function(){
	connection.exchange(exchangeName, options = {type: "topic", autoDelete: true, confirm: true}, function(exchange){
		var queue = connection.queue(queueName, options = {exclusive: true, autoDelete: true}, function(queue){
			queue.bind(exchangeName, routingKey, function(){
				queue.subscribe(options = {ack: false}, function(message, headers, deliveryInfo, messageObject){
					//callback funtion on receiving messages
					console.log(message.data.toString());
				});
			});
		});
	}); 
});
