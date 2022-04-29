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


def add_users(users, client, target_group_entity, bot_id):
    total_users = len(users)
    index = 1
    for user in users:
        time.sleep(1)
        if 'id' in user:
            try:
                if user['username'] == "":
                    continue
                user_to_add = client.get_input_entity(user['username'])
                logger.info(f"Adding {user['username']} to {target_group_entity}")
                client(InviteToChannelRequest(target_group_entity, [user_to_add]))
                logger.info("Waiting for {} Seconds...".format(wait_time))
                logger.info("Bot {} was adding {}/{} users".format(bot_id, index, total_users))
                time.sleep(wait_time)
            except PeerFloodError:
                logger.error("Getting Flood Error from telegram. \n[!] Script is stopping now. \n[!] Please try again ")
                pass
            except UserPrivacyRestrictedError:
                logger.error("[!] The user's privacy settings do not allow you to do this. Skipping.")
                pass
            except UserInvalidError:
                logger.error("[!] Invalid user. Skipping.")
                pass
            except UserIdInvalidError as e:
                print(e)
                logger.error("[!] Invalid user id. Skipping.")
                pass
            except Exception as e:
                traceback.print_exc()
                print(e)
                logger.error("[!] Unexpected Error")
                logger.error(e)
                pass
                continue
        index += 1
