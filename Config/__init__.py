
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

email = config['Settings']['Email']
password = config['Settings']['Password']
server = config['Settings']['Server']
port = config['Settings']['Port']
desiredPosition = config['Queue']['DesiredPosition']
recheck = config['Settings']['Recheck']
queueNotifications = config['Settings']['QueueNotifications']