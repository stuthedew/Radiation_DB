'''MQTT and MySQL based radiation sensor logger'''
from __future__ import division
from radDB import DB, parse
import paho.mqtt.client as mqtt
import cymysql as mdb
import sys

feed_id = "raw"

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
    print("MQTT: "),
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
    try:
        with DB.Helper('localhost', 'Rad_DB_py', '12345678', 'RadDB') as rdb:
            #rdb.get_version()
            pMsg = parse.parseMsg(msg.payload)
            #print(pMsg)
            #print(pMsg[0])
            #print(pMsg[2])
            #print(pMsg[1])

            print("Adding \"{}\", {}, {} to DB...".format(pMsg[0], pMsg[1], pMsg[2]))
            rdb.add_data(pMsg[0], pMsg[2])


    except mdb.Error as err:
        print "Error %d: %s" % (err.args[0], err.args[1])
        sys.exit(1)


def main():
    """Wait for incoming radiation data, and log it to MySQL database"""
    #connect to MySQL database
    #start mqtt server
    #wait for data
    #if data then log to MySQL database

    print("Hello")
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
