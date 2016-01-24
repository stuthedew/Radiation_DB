'''MQTT and MySQL based radiation sensor logger'''
from __future__ import division
from radDB import DB, parse
import argparse
import paho.mqtt.client as mqtt
import cymysql as mdb
import sys

feed_id = "RadESP"

return_str =[
    "Connection successful",
    "incorrect protocol version",
    "invalid client identifier",
    "server unavailable",
    "bad username or password",
    "not authorised"
    ]

args = None

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
        client.reconnect()

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    try:
        pMsg = parse.parseMsg(msg.payload)
        print(("Received \"{}\", {}, {}".format(pMsg[0], pMsg[1], pMsg[2])))
        if(args.dry_run == False):
            with DB.Helper('192.168.0.11', 'Rad_DB_py', '12345678', 'RadDB') as rdb:
                print("Adding to database")
                rdb.add_data(pMsg[0], pMsg[2])


    except Exception as err:
        print err
        #sys.exit(1)


def argBegin():
    parser = argparse.ArgumentParser(description='Read values from MQTT and upload to database')
    parser.add_argument('--dry-run', action='store_true', default=False, help='Do not store values in database')
    return parser.parse_args()


def main():
    """Wait for incoming radiation data, and log it to MySQL database"""
    args = argBegin()
    print(args)
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
