import time
import traceback

from telethon.errors import PeerFloodError, UserPrivacyRestrictedError
from telethon.tl.functions.channels import InviteToChannelRequest
from telethon.tl.types import InputPeerUser
from tqdm import tqdm

wait_time = 900


def add_users(users, client, target_group_entity):
    for user in users:
        time.sleep(1)
        try:
            print("Adding {}".format(user['id']))
            user_to_add = InputPeerUser(user['id'], user['access_hash'])
            client(InviteToChannelRequest(target_group_entity, [user_to_add]))
            print("Waiting for {} Seconds...".format(wait_time))
            for _ in tqdm(range(wait_time)):
                time.sleep(1)
        except PeerFloodError:
            print("Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after "
                  "some time.")
        except UserPrivacyRestrictedError:
            print("[!] The user's privacy settings do not allow you to do this. Skipping.")
        except Exception as e:
            traceback.print_exc()
            print("[!] Unexpected Error")
            print(e)
            print("[!] Script is stopping now. Please try again after some time.")
            continue
