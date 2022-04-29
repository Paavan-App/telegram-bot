import time
import traceback
import logging
import sys
from telethon.errors import PeerFloodError, UserPrivacyRestrictedError, UserInvalidError, UserIdInvalidError
from telethon.tl.functions.channels import InviteToChannelRequest

wait_time = 900

logger = logging.getLogger()
logger.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')

stdout_handler = logging.StreamHandler(sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.setFormatter(formatter)

file_handler = logging.FileHandler('logs.log')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stdout_handler)


def add_users(users, client, target_group_entity):
    for user in users:
        time.sleep(1)
        print(f"Adding {user} to {target_group_entity}")
        if 'id' in user:
            try:
                if user['username'] == "":
                    continue
                print("Adding {}".format(user['id']))
                user_to_add = client.get_input_entity(user['username'])
                logger.info(f"Adding {user['username']} to {target_group_entity}")
                client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                print("Waiting for {} Seconds...".format(wait_time))
                logger.info("Waiting for {} Seconds...".format(wait_time))
                time.sleep(wait_time)
            except PeerFloodError:
                print("Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again after "
                      "some time.")
                logger.error("Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again ")
                pass
            except UserPrivacyRestrictedError:
                print("[!] The user's privacy settings do not allow you to do this. Skipping.")
                logger.error("[!] The user's privacy settings do not allow you to do this. Skipping.")
                pass
            except UserInvalidError:
                print("[!] Invalid user. Skipping.")
                logger.error("[!] Invalid user. Skipping.")
                pass
            except UserIdInvalidError as e:
                print(e)
                print("[!] Invalid user id. Skipping.")
                logger.error("[!] Invalid user id. Skipping.")
                pass
            except Exception as e:
                traceback.print_exc()
                print("[!] Unexpected Error")
                print(e)
                print("[!] Script is stopping now. Please try again after some time.")
                logger.error("[!] Unexpected Error")
                logger.error(e)
                pass
                continue
