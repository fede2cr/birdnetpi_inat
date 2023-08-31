# birdnetpi_inat
Integration of BirdNetPi and iNaturalist

## Description

BirdNet-Pi is a project that uses a RaspberryPi and a microphone to listen to the songs of birds and uses AI models to identify them. iNaturalist is a platform that records pictures of species with metadata for scientific use.

This project takes the observations from a (slightly modified) BirdNet-Pi installation, uploads the scientific names of the species it records to Adafruit-IO; and then code running on a separate device takes care of listening to the Adafruit-IO stream for the names of the species, and then grabs an image from iNaturalist and displays it via an application or a website.

It is intended to help users of BirdNet-Pi to have an image of the species that are being recorded for the purpose of ornithological education.

## Code

### BirdNet-Pi -> Adafruit-IO

BirdNet-Pi uses *apprise* for notifications, but their implementation of MQTT plugin handles data in a way that is incompatible with Adafruit-IO. This part of the project is as much a dirty hack as there ever has been one, replacing the apprise Python script with a shell script that calls mosquitto_pub to send the data to Adafruit-IO easily enough.

Of course a BirdNet-Pi integration or even a patch for apprise to work properly with Adafruit-IO is preffered, but in the spirit of rapid development, some very large liberties have been taken on this code.

Modify the username and key of Adafruit-IO in this example code, and then run it in the device that has BirdNet-Pi installed.

Note: This ugly hack might be replaced by a BirdNet-Pi procedure. If you don't like this ugly hack, please help out, or at least insist that it is removed in a GitHub issue.

```bash
sudo apt install -y mosquitto-clients
cd ~/BirdNET-Pi/birdnet/bin/
mv apprise apprise.orig
cat << EOF
#!/bin/bash

sciname=$(echo $@ | awk -F% '{print $2}')
echo $sciname

mosquitto_pub -h io.adafruit.com -u username -P 'aio_key' -t username/feeds/birdnetpi -m "$sciname"
EOF
chmod +x apprise
```

Define in the web config of BirdNet-Pi the notification message as ``%$sciname%``.

### Adafruit-IO -> iNaturalist

```
python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt
```



