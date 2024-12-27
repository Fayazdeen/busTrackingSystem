"""
Replace this code snippet at the following location: 
File name: aws-iot-device-sdk-python-v2/samples/pubsub.py
line no: 133 to 150
"""


lat_count = 0.1
long_count = 2.1
while message_count == 0:
    message_dict = {
        "Lat": lat_count,
        "Long": long_count
    }
    message = json.dumps(message_dict)
    # message = "{} [{}]".format(message_string, publish_count)
    print("Publishing Bus live location to topic '{}': {}".format(message_topic, message))
    message_json = json.dumps(message)
    mqtt_connection.publish(
        topic=message_topic,
        payload=message_json,
        qos=mqtt.QoS.AT_LEAST_ONCE)
    time.sleep(10)
    lat_count += 2
    long_count += 2
