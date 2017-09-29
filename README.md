# IOT-Fingerprint-Scanner
Setting up an Adafruit Fingerprint Scanner with Nokia 5110 LCD. Using a Particle photon for communication with MQTT. Raspberry Pi installed with SQLite3 acting as a server database for all the fingerprints. 

Required:

Adafruit Fingerprint Sensor, 
Particle Photon, 
Nokia 5110 LCD, 
Raspberry PI 3, 
SQLite3 installed your Raspberry PI, 
MQTT server


FINGERPRINT SCANNING PROCESS

1. Place finger on scanner.
2. If fingerprint is verified, photon sends fingerprint ID# to MQTT.
fp/id – ID#
3. Raspberry pi subscribes to fp/id and reads the employee name and employee ID# from FINGERPRINTS table.
4. Raspberry pi publishes the Employee's name to MQTT.
fp/name – NAME
5. Particle photon subscribes to fp/name and prints the name on the LCD.
6. Photon returns to fingerprint scanning mode.

Enroll new ID process

1. User publishes the new employee name and employee ID# to MQTT.
fp/enroll – Name,EmployeeID (No Spaces)
2. Particle photon subscribes to fp/enroll, generates a new fingerprint ID# from the Eeprom memory and registers the new ID.
3. Particle phtoon adds the new fingerprint ID# to the original payload and publishes the name, employee ID and the fingerprint ID# to MQTT.
4. Raspberry pi subscribes to fp/log and adds the new entry to the FINGERPRINTS table.
5. Particle photon returns to fingeprint scanning mode.

Time logging process

1. When employee scans his fingerprint on the scanner, the photon and sensor verify the image.
2. If ID is verified, the photon publishes the ID3 to MQTT.
fp/id – Fingerprint ID#
3. Raspberry pi subscribes to fp/id and depending on the flag (Entry/exit), registers the time log details to the TIMELOG Table.
4. If he flag is exit, it calculates the working hrs for the day.
