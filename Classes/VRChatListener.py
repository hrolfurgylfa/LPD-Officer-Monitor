import vrcpy
import asyncio
from termcolor import colored
from datetime import datetime

loop = asyncio.get_event_loop()
client = vrcpy.Client(loop=loop)

def printd(string):
    timestamp = (str(datetime.now().strftime("%d-%b-%Y (%H:%M:%S)")))
    string = colored(timestamp, 'magenta') + ' - ' + string
    print(string)


async def main(username, password):
    await client.login(
        username=username,
        password=password
    )

    try:
        # Start the ws event loop
        await client.start()
    except KeyboardInterrupt:
        await client.logout()

async def start(username, password):
    loop.create_task(main(username, password))


@client.event
async def on_friend_location(friend_b, friend_a):
    try:
        instance = await client.fetch_instance_via_id(friend_a.world_id, friend_a.instance_id)
        #print(world.__dict__)
        print(instance.world_id + ' #' + instance.name)
    except:
        print("{} is now in {}".format(colored(friend_a.display_name, 'green'), colored(friend_a.location, 'yellow')))

@client.event
async def on_friend_active(friend_a):
    printd("{} is now {}.".format(colored(friend_a.display_name, 'green'), friend_a.state))


@client.event
async def on_friend_online(friend_a):
    printd("{} is now {}.".format(colored(friend_a.display_name, 'green'), colored(('online'), 'cyan')))


@client.event
async def on_friend_add(friend_b, friend_a):
    printd("{} is now your friend.".format(colored(friend_a.display_name, 'green')))


@client.event
async def on_friend_delete(friend_b, friend_a):
    printd("{} is no longer your friend.".format(colored(friend_a.display_name, 'green')))


#@client.event
#async def on_friend_update(friend_b, friend_a):
#    printd("{} has updated their profile/account.".format(colored(friend_a.display_name, 'green')))


#@client.event
#async def on_notification(notification):
#    printd("Got a {} notification from {}.".format(
#        notification.type, notification.senderUsername))


@client.event
async def on_connect():
    printd("Connected to wss pipeline.")


@client.event
async def on_disconnect():
    printd("Disconnected from wss pipeline.")


async def join_user(user_id):
    user = await client.fetch_user_via_id(user_id)
    join_link = 'vrchat://launch?' + user.location
    return join_link
    
async def send_invite(user_id):
    user = await client.fetch_user_via_id(user_id)
    join_link = 'vrchatL//launch?' + user.location
    return join_link