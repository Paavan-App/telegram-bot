import configparser
import csv
import os
import sys

from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, InputPeerChannel
from add_users import add_users

cpass = configparser.RawConfigParser()
cpass.read('./config/config.data')

offset = 100
members = 500
input_file_name = './config/members.csv'
target_group_id = '1728042268'

try:
    arg1 = int(sys.argv[1])
    start_range = (arg1 - 1) * offset
    end_range = arg1 * offset
    api_id = cpass['cred' + str(arg1)]['id']
    api_hash = cpass['cred' + str(arg1)]['hash']
    phone = cpass['cred' + str(arg1)]['phone']
    client = TelegramClient(phone, api_id, api_hash)

except Exception as e:
    os.system('clear')
    print(e)
    print('Argument missing')
    print('Syntax: python main.py [cred number]')
    sys.exit(1)

client.connect()

if not client.is_user_authorized():
    client.send_code_request(phone)
    os.system('clear')
    client.sign_in(phone, input(f'Enter the code for {phone}: '))

users = []
with open(input_file_name, encoding='UTF-8') as f:
    rows = csv.reader(f, delimiter=",", lineterminator="\n")
    next(rows, None)
    for row in rows:
        user = {'username': row[0], 'id': int(row[1]), 'access_hash': int(row[2]), 'name': row[3]}
        users.append(user)

# slice the users array to the selected range
users = users[start_range:end_range]

chats = []
last_date = None
chunk_size = 200
groups = []

result = client(GetDialogsRequest(
    offset_date=last_date,
    offset_id=0,
    offset_peer=InputPeerEmpty(),
    limit=chunk_size,
    hash=0
))
chats.extend(result.chats)

for chat in chats:
    try:
        if chat.megagroup:
            groups.append(chat)
    except Exception as e:
        print(str(e))
        continue

target_group_index = -1
for i in range(0, len(groups)):
    group = groups[i]
    if group.id == int(target_group_id):
        target_group_index = i
        break

if target_group_index == -1:
    print('Target group not found')
    sys.exit(1)

target_group = groups[int(target_group_index)]

target_group_entity = InputPeerChannel(target_group.id, target_group.access_hash)

try:
    add_users(users, client, target_group_entity)
except Exception as e:
    print(e)
    sys.exit(1)
