# outside
from pymongo import MongoClient
import json
from datetime import datetime
import sys
import dateutil.parser

# me
import configs
import stubhub_api

events = MongoClient(configs.mongo_conn).stubhub.events

def store_new_event(event_id):
	event = get_event_info(event_id)	

	new_event = {
		'id': event['id'],
		'title': event['title'],
		'description': event['description'],
		'status': event['status']['statusId'],
		'localDate': dateutil.parser.parse(event['eventDateLocal']),
		'utcDate': dateutil.parser.parse(event['eventDateUTC']),
		'venue': {
			'id': event['venue']['id'],
			'name': event['venue']['name'],
			'address1': event['venue']['address1'],
			'city': event['venue']['city'],
			'state': event['venue']['state'],
			'zipCode': event['venue']['zipCode'],
			'country': event['venue']['country'],
		}
	}

	### Store it
	events.insert(new_event)

	print "Added event " + str(event_id)

if __name__ == "__main__":
	event_ids = []
	for line in sys.stdin:
		event_ids.append(int(line))

	for event_id in event_ids:
		store_new_event(event_id)

	print "Done adding events"