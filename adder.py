from telethon.sync import TelegramClient
from telethon.tl.types import InputPeerEmpty
from telethon.tl.functions.messages import GetDialogsRequest
from telethon import functions
import csv
import time

# Your credentials
name = 'adder'
api_id = 123456    # Replace with your actual API ID
api_hash = 'your_api_hash_here'    # Replace with your actual API HASH
phone = 'your_phone_number_here'    # Replace with your actual phone number

# Connect to the client
client = TelegramClient(phone, api_id, api_hash)
client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    client.sign_in(phone, input('Enter the code: '))

# Read users from CSV file
users = []
with open(r"members.csv", encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)  # Skip the header
    for row in rows:
        user = {
            'username': row[0],
            'id': int(row[1]),
            'access_hash': int(row[2]),
            'name': row[3]
        }
        users.append(user)

# Fetch dialogs (channels and chats)
result = client(GetDialogsRequest(
    offset_date=None,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=100,  # Set limit appropriately
    hash=0
))

# Loop through the users list to add all users
for user in users:
    user_to_add = user['username']
    
    if user_to_add:
        try:
            client(functions.contacts.AddContactRequest(
                id=user_to_add,
                first_name=user['name'],  # First name from the CSV
                last_name='',              # Optionally add the last name
                phone='',                  # Phone required if adding by phone
                add_phone_privacy_exception=True
            ))
            print(f"Added {user['username']} successfully")
            time.sleep(1)  # Add a delay to avoid hitting rate limits (adjust as needed)
        except Exception as e:
            print(f"Failed to add {user['username']}: {e}")
