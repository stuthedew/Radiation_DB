"""MQTT function helper"""
import paho.mqtt.client as mqtt
import sys

feed_id= "raw"

return_str =[
    "Connection successful",
    "incorrect protocol version",
    "invalid client identifier",
    "server unavailable",
    "bad username or password",
    "not authorised"
    ]

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, rc):
    """callback function on connect. Subscribes or exits depending on outcome"""
    print(return_str[rc])
    if(rc > 1):
        print("Connection refused - " + return_str[rc])
        sys.exit(rc)
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    else:
        print(return_str[rc])
        client.subscribe(feed_id)

def on_disconnect(client, userdata, rc):
    """Callback for disconnect"""
    if rc != 0:
        print("Unexpected disconnection.")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    #print(msg.topic+" "+str(msg.payload))
    print("".join("{:02x}".format(ord(c)) for c in msg.payload))

def main():
    """MQTT test function"""
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.username_pw_set('radpi', 'testpassword')
    client.connect("localhost", 1883, 60)

    # Blocking call that processes network traffic, dispatches callbacks and
    # handles reconnecting.
    # Other loop*() functions are available that give a threaded interface and a
    # manual interface.
    client.loop_forever()



if __name__ == '__main__':
    sys.exit(main())
