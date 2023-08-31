from Adafruit_IO import MQTTClient
from PIL import Image
from pyinaturalist import get_observations
import requests
import json
import secrets

FEED_ID="birdnetpi"

def connected(client):
    """Connected function will be called when the client is connected to
    Adafruit IO.This is a good place to subscribe to feed changes.  The client
    parameter passed to this function is the Adafruit IO MQTT client so you
    can make calls against it easily.
    """
    # Subscribe to changes on a feed named Counter.
    print('Subscribing to Feed {0}'.format(FEED_ID))
    client.subscribe(FEED_ID)
    print('Waiting for feed data...')

def disconnected(client):
    """Disconnected function will be called when the client disconnects."""
    sys.exit(1)

def message(client, feed_id, payload):
    """Message function will be called when a subscribed feed has a new value.
    The feed_id parameter identifies the feed, and the payload parameter has
    the new value.
    """
    print(payload)
    observations = get_observations(taxon_name=payload, photos=True, per_page=1, page=1)
    url=observations['results'][0]['taxon']['default_photo']['medium_url']
    response = requests.get(url)
    open("birdnetpi.jpg", "wb").write(response.content)
    image = Image.open('birdnetpi.jpg')
    image.show()

# Create an MQTT client instance.
client = MQTTClient(secrets.username, secrets.aiokey)

# Setup the callback functions defined above.
client.on_connect = connected
client.on_disconnect = disconnected
client.on_message = message

# Connect to the Adafruit IO server.
client.connect()

# The first option is to run a thread in the background so you can continue
# doing things in your program.
client.loop_blocking()
