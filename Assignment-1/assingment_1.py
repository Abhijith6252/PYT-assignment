# import
import json
from typing import Set
import events
import datetime
from dateutil import parser
import pandas as pd
import pytz

# to convert to ist
ist = pytz.timezone('Asia/Kolkata')

# the given events.json was processed and saved as events.py for accessing the data
events_list = events.events_list

# The date given was 12th July 2021
check_date = datetime.date(2021, 7, 12)

result_list = []


for event in events_list:

    created_at_str = event['createdAt']
    created_at = parser.parse(created_at_str)

    # checking is created_at matches the given check_date
    if created_at.date() == check_date:
        # the necessary data is parsed and stored as list of dicts
        event_dict = {}
        event_dict['anonymousId'] = event['anonymousId']
        event_dict['name'] = event['name']
        event_dict['timestamp in IST'] = created_at.astimezone(
            ist).strftime("%m/%d/%Y %H:%M:%S")
        event_dict['page_url'] = event['attributes']['page_url']
        if 'utm_source' in event['attributes']['leadSource']:
            event_dict['utm_source'] = event['attributes']['leadSource']['utm_source']
        else:
            event_dict['utm_source'] = ""
        if 'utm_medium' in event['attributes']['leadSource']:
            event_dict['utm_medium'] = event['attributes']['leadSource']['utm_medium']
        else:
            event_dict['utm_medium'] = ""

        result_list.append(event_dict)

# dict-->name_dict
# key-->unique event_name
# value--> all the events under the event_name
name_dict = {}
for result in result_list:
    if result['name'] not in name_dict:
        name_dict[result['name']] = []
    name_dict[result['name']].append(result)


# all the values of each key are put as each tab
# the tabs are numbered because excel restricts the tab_name<32chars
# strings_to_urls is used because it viloates the 256char restiction of excel
with pd.ExcelWriter('./Assignment-1_Results.xlsx', engine='xlsxwriter', options={'strings_to_urls': False}) as writer:
    i = 1
    for name in name_dict:
        df = pd.DataFrame(name_dict[name])
        df.to_excel(writer, sheet_name=str(i), index=False)
        i = i+1

    writer.close()
