import random
import time
import requests
from highrise import BaseBot, Highrise, Position, AnchorPosition, Reaction
from highrise import __main__
from asyncio import run as arun
from emotes import Dance_Floor
import asyncio
from random import choice
import json
from typing import List
from datetime import datetime, timedelta
from highrise.models import SessionMetadata
import re
from highrise.models import SessionMetadata,  GetMessagesRequest, User ,Item, Position, CurrencyItem, Reaction
from typing import Any, Dict, Union
from highrise.__main__ import *
import asyncio, random




class BotDefinition:
    
      
    def __init__(self, bot, room_id, api_token):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token
        self.following_username = None

class Counter:
    bot_id = ""
    static_ctr = 0
    usernames = ['Alionardo_']

class Bot(BaseBot):
    continuous_emote_tasks: Dict[int, asyncio.Task[Any]] = {}  
    user_data: Dict[int, Dict[str, Any]] = {}
    EMOTE_DICT = {
      "1"         :"dance-pinguin",
      "2"       : "idle-guitar",
      "3"     : "dance-anime",
      "4"           : "emoji-angry",
      "5"             : "emote-bow",
      "6"          : "idle-dance-casual",
      "7"        : "emote-charging",
      "8"       : "emote-confused",
      "9"         : "emoji-cursing",
      "10"          : "emote-curtsy",
      "11"           : "emote-cutey",
      "12"            : "dance-tiktok2",
      "13"       : "emote-cute",
      "14"      : "emote-energyball",
      "15"        : "idle-enthusiastic",
      "16"     : "emote-fashionista",
      "17"            : "emoji-flex",
      "18"      : "emote-lust",
      "19"           : "emote-float",
      "20"            : "emote-frog",
      "21"      : "dance-weird",
      "22"         : "emote-gravity",
      "23"          : "emote-greedy",
      "24"           : "emote-hello",
      "25"             : "emote-hot",
      "26"        : "dance-icecream",
      "27"            : "emote-kiss",
      "28"            : "dance-blackpink",
      "29"           : "emote-superpose",
      "30"           : "emote-laughing",
      "31"          : "dance-shoppingcart",
      "32"          : "emote-maniac",
      "33"           : "emote-model",
      "34"              : "emote-no",
      "35"         : "dance-macarena",
      "36"      : "dance-pennywise",      
      "37"           : "emote-pose1",
      "38"           : "emote-pose3",
      "39"           : "emote-pose5",
      "40"           : "emote-pose7",
      "41"           : "emote-pose8",
      "42"      : "emote-punkguitar",
      "43"    : "emoji-celebrate",
      "44"         : "dance-russian",
      "45"             : "emote-sad",
      "46"          : "dance-tiktok8",
      "47"         : "dance-tiktok10",
      "48"             : "emote-shy",
      "45"       : "idle_singing",
      "46"             : "idle-loop-sitfloor",
      "47"       : "emote-snowangel",
      "48"        : "emote-snowball",
      "49"      : "emote-swordfight",
      "50"     : "emote-telekinesis",
      "51"        : "emote-teleporting",
      "52"        : "emoji-thumbsup",
      "53"           : "emote-tired",
      "54"       : "emoji-gagging",
      "55"           : "dance-tiktok9",
      "56"            : "emote-wave",
      "57"           : "dance-weird",
      "58"            : "emote-snake",
      "59"          : "dance-wrong",
      "60"             : "emote-yes",
      "61"       : "emote-zombierun",
      "62"           : "emoji-angry",
      "63"             : "emote-bow",

    }
    continuous_emote_task = None
    cooldowns = {}  # Class-level variable to store cooldown timestamps
    emote_looping = False

    def __init__(self):
        super().__init__()
        self.load_membership()
        self.load_moderators()
        self.load_temporary_vips()
        self.load_tempvip()
        self.following_username = None
        self.maze_players = {}
        self.user_points = {}  # Dictionary to store user points

        #conversation id var
        self.convo_id_registry = []

        #dance floor position
        min_x = 15.5
        max_x = 18.5
        min_y = 0.0
        max_y = 1.0
        min_z = 1.5
        max_z = 8.5

        self.dance_floor_pos = [(min_x, max_x, min_y, max_y, min_z, max_z)]

        #dancer variable
        self.dancer = []

        #dance floor emotes var
        self.emotesdf = Dance_Floor

    def load_temporary_vips(self):
        try:
            with open("temporary.json", "r") as file:
                self.temporary_vips = json.load(file)
        except FileNotFoundError:
            self.temporary_vips = {}
    def load_tempvip(self):
         try:
            with open("tempvip.json", "r") as file:
              self.tempvip = json.load(file)
         except FileNotFoundError:
             self.tempvip = {}
        
    def save_tempvip(self):
        with open("tempvip.json", "w") as file:
            json.dump(self.tempvip, file)
    def save_temporary_vips(self):
      with open("temporary.json", "w") as file:
          json.dump(self.temporary_vips, file)
    def load_moderators(self):
        try:
            with open("moderators.json", "r") as file:
                self.moderators = json.load(file)
        except FileNotFoundError:
            self.moderators = []

        # Add default moderators here
        default_moderators = ['Alionardo_','Maebelle420']
        for mod in default_moderators:
            if mod.lower() not in self.moderators:
                self.moderators.append(mod.lower())
    

     
    def load_membership(self):
     try:
        with open("membership.json", "r") as file:
            self.membership = json.load(file)
     except FileNotFoundError:
        self.membership = []
    def save_membership(self):
     with open("membership.json", "w") as file:
        json.dump(self.membership, file)

  
    def save_moderators(self):

      with open("moderators.json", "w") as file:
            json.dump(self.moderators, file)

  
    async def announce(self,user_input,message: str):
      while True:        
              await self.highrise.chat(user_input)
              await asyncio.sleep(60)
              await self.highrise.send_emote('emote-hello')
    async def on_start(self, session_metadata: SessionMetadata) -> None:
      try:
       
        Counter.bot_id = session_metadata.user_id
        print("Ali is booting ...")
        asyncio.create_task(self.dance_floor())
        pass


        self.highrise.tg.create_task(self.highrise.walk_to(Position(15.5, 0.5, 14.5, facing='FrontRight')))
        self.load_temporary_vips()

        await self.highrise.chat(f"hi guys im here ")
      except Exception as e:
          print(f"An exception occured: {e}")  
    async def on_emote(self, user: User ,emote_id : str , receiver: User | None )-> None:
      print (f"{user.username} , {emote_id}")

    async def on_user_join(self, user: User) -> None:

     try:

        await self.highrise.send_whisper(user.id,f"hello {user.username}\nWelcome to what gonna be your lovely place\n           420's Rave\n• !list or -list \n  to veiw the functions \nfor bots dm @Alionardo_ .")
        await self.highrise.send_emote('emote-salute')
     
     except Exception as e:
            print(f"An error on user_on_join: {e}") 


    async def on_user_leave(self, user: User) ->None:
      try:
        print(f"{user.username} has left the room")
        await self.highrise.chat(f"  {user.username} left the room")
      
      except Exception as e:
         print(f"An error on user_on_join: {e}") 
      
    
    async def teleport_user_next_to(self, target_username: str, requester_user: User):
      room_users = await self.highrise.get_room_users()
      requester_position = None

      for user, position in room_users.content:
        if user.id == requester_user.id:
            requester_position = position
            break
      for user, position in room_users.content:
        if user.username.lower() == target_username.lower(): 
          z = requester_position.z 
          new_z = z + 1 

          user_dict = {
            "id": user.id,
            "position": Position(requester_position.x, requester_position.y, new_z, requester_position.facing)
          }
          await self.highrise.teleport(user_dict["id"], user_dict["position"])

   

    async def teleport_user_next_to(self, target_username: str, requester_user: User):
      room_users = await self.highrise.get_room_users()
      requester_position = None

      for user, position in room_users.content:
        if user.id == requester_user.id:
            requester_position = position
            break
      for user, position in room_users.content:
        if user.username.lower() == target_username.lower(): 
          z = requester_position.z 
          new_z = z + 1 

          user_dict = {
            "id": user.id,
            "position": Position(requester_position.x, requester_position.y, new_z, requester_position.facing)
          }
          await self.highrise.teleport(user_dict["id"], user_dict["position"])

   
    async def teleport_user_next_to(self, target_username: str, requester_user: User):
      room_users = await self.highrise.get_room_users()
      requester_position = None

      for user, position in room_users.content:
        if user.id == requester_user.id:
            requester_position = position
            break
      for user, position in room_users.content:
        if user.username.lower() == target_username.lower(): 
          z = requester_position.z 
          new_z = z + 1 

          user_dict = {
            "id": user.id,
            "position": Position(requester_position.x, requester_position.y, new_z, requester_position.facing)
          }
          await self.highrise.teleport(user_dict["id"], user_dict["position"])




    async def run(self, room_id, token):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions) 
    async def on_reaction(self, user: User, reaction: Reaction, receiver: User) -> None:
     try:
      if user.username == "Maebelle420" :
        if reaction == "heart":
          await self.highrise.chat(f"{receiver.username} is now a Permanent VIP, given by {user.username}")

          receiver_username = receiver.username.lower()
          if receiver_username not in self.moderators:
                self.moderators.append(receiver_username)
                self.save_moderators()


        if user.username == "Maebelle420"  :
          if reaction == "wink":
              await self.highrise.chat(f"{receiver.username} is now a Temporary VIP, given by {user.username}")

              receiver_username = receiver.username.lower()
              if receiver_username not in self.temporary_vips:
                    self.temporary_vips[receiver_username] = int(time.time()) + 24 * 60 * 60  # VIP for 24 hours
                    self.save_temporary_vips()


      if user.username in ["Maebelle420"] and reaction == "clap":
            await self.highrise.chat(f"{receiver.username} is remove from the commands by {user.username}")

            receiver_username = receiver.username.lower()

            # Remove user from moderators list
            if receiver_username in self.moderators:
                self.moderators.remove(receiver_username)
                self.save_moderators()

            # Add user to temporary VIPs list
            if receiver_username not in self.temporary_vips:
                self.temporary_vips[receiver_username] = int(time.time()) + 24 * 60 * 60  # VIP for 24 hours
                self.save_temporary_vips()

      if user.username in ["Maebelle420"] and reaction == "wave":
            await self.highrise.moderate_room(receiver.id, "kick")
            await self.highrise.chat(f"{receiver.username} is Kicked by {user.username}")

      if reaction =="thumbs" and user.username.lower() in self.moderators:
         target_username = receiver.username
         if target_username not in ["Maebelle420"]:
            await self.teleport_user_next_to(target_username, user)



     except Exception as e:
            print(f"An exception occured: {e}")

      

    def remaining_time(self, username):
        if username in self.temporary_vips:
            remaining_seconds = self.temporary_vips[username] - int(time.time())
            if remaining_seconds > 0:
                return str(timedelta(seconds=remaining_seconds))
        return "Not a temporary VIP."


    async def on_chat(self, user: User, message: str) -> None:
      try:
         user_input = None
         print(f"{user.username} said: {message}")     
         if message.lower().startswith("-announce "):
           if user.username.lower() in self.moderators:
             parts = message.split()
             if len(parts) >= 3:
                user_input =  message[len("-announce "):]
                await self.announce(user_input,message)
                
         if message.startswith("❤️all"):
           if user.username.lower() in self.moderators:
             roomUsers = (await self.highrise.get_room_users()).content
             for roomUser, _ in roomUsers:
                await self.highrise.react("heart", roomUser.id)
         if message.startswith("!kick"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !kick @username")
                    return

                mention = parts[1]
                username_to_kick = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_kick.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_kick.lower())
                    user_id_to_kick = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_kick, "kick")
                    await self.highrise.chat( f"Kicked {mention}.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

         elif message.startswith("!mute"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !mute @username")
                    return

                mention = parts[1]
                username_to_mute = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_mute.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_mute.lower())
                    user_id_to_mute = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_mute, "mute",3600)  # Mute for 1 hour
                    await self.highrise.chat(f"Muted {mention} for 1 hour.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

         elif message.startswith("!unmute"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !mute @username")
                    return

                mention = parts[1]
                username_to_mute = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_mute.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_mute.lower())
                    user_id_to_mute = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_mute, "mute",1)  # Mute for 1 hour
                    await self.highrise.chat(f"{mention} Unmuted.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

         elif message.startswith("!ban"):
            if user.username.lower() in self.moderators:
                parts = message.split()
                if len(parts) < 2:
                    await self.highrise.chat(user.id, "Usage: !ban @username")
                    return

                mention = parts[1]
                username_to_ban = mention.lstrip('@')  # Remove the '@' symbol from the mention
                response = await self.highrise.get_room_users()
                users = [content[0] for content in response.content]  # Extract the User objects
                user_ids = [user.id for user in users]  # Extract the user IDs

                if username_to_ban.lower() in [user.username.lower() for user in users]:
                    user_index = [user.username.lower() for user in users].index(username_to_ban.lower())
                    user_id_to_ban = user_ids[user_index]
                    await self.highrise.moderate_room(user_id_to_ban, "ban", 3600)  # Ban for 1 hour
                    await self.highrise.chat(f"Banned {mention} for 1 hour.")
                else:
                    await self.highrise.send_whisper(user.id, f"User {mention} is not in the room.")
            else:
                await self.highrise.send_whisper(user.id, "You can't use this command.")

        
        
         if message == "!tip5":
              if user.username == "Maebelle420" :
                roomUsers = (await self.highrise.get_room_users()).content
                for roomUser, _ in roomUsers:
                  await self.highrise.tip_user(roomUser.id, "gold_bar_5")
              else: 
                await  self.highrise.send_whisper(user.id, f"Only @Maebelle420 can use tip!")

         if message == "!tip1":
              if user.username == "Maebelle420":
                roomUsers = (await self.highrise.get_room_users()).content
                for roomUser, _ in roomUsers:
                  await self.highrise.tip_user(roomUser.id, "gold_bar_1")
              else: 
                await  self.highrise.send_whisper(user.id, f"Only the @Maebelle420 can use tip!")

                

         if message.lower().lstrip().startswith(("-list", "!list")):
                await self.highrise.chat("\\commands you can use:\n• !emote or -emote\n• !loop or -loop\n• !feedback or -feedback \n• !teleport or -teleport \n• -buy or !buy for \n 🎫VIP Membership🎫 ")
                await self.highrise.chat(f"\n ____________________________\n• !mod or -mod ( only for mods )")
        
         if message.lower().lstrip().startswith(("-buy" , "!buy")):
             await self.highrise.chat(f"\n -temp vip = 100 🎫 \n ____________________________\n -perm vip = 1k 🎫 ")
         if message.lower().lstrip().startswith(("-temp vip")):
             await self.highrise.chat(f"\nBy purshasing this you will be able to : \n ____________________________\n Use the vip spot only for 100g for 24 H , payment with host bot (me)")
         if message.lower().lstrip().startswith(("-perm vip")):
             await self.highrise.chat(f"\nBy purshasing this you will be able to : \n ____________________________\n Use the vip spot perm only for 1000g  , payment with host bot (me)")
         if message.lower().lstrip().startswith(("!loop","-loop")):
           await self.highrise.chat(f"mention loop before the emote name ")

         if message.lower().lstrip().startswith(("-teleport", "!teleport")):
                    await self.highrise.chat(f"\n • Teleports\n ____________________________\nGround floor : -0  \nvip : (vip only), make sure you have 🎫VIP Membership🎫 \n• type -buy or !buy for details \ndj :( Mods only )")
         if message.lower().lstrip().startswith(("!rules", "-rules")):
           await self.highrise.chat(f"\n\n        RULES\n ____________________________\n 1. NO UNDERAGE \n 2. No advertising\n 3. No hate speech \n 4. No begging (those trash will be immediately banned 🚫) \n 5. No spamming ")
         if message.lower().lstrip().startswith(("-feedback", "!feedback")):
                    await self.highrise.send_whisper(user.id, "• [ Submit Feedback ]\\Thank you for joining our room! \n We value your feedback,")
                    await self.highrise.send_whisper(user.id,"Please share your feedback/suggestions with @Alionardo_ to improve our environment. Your contributions are valuable and will help us improve.")  

         if message.lower().lstrip().startswith(("-emote", "!emote")):
                await self.highrise.send_whisper(user.id, "\n• Emote can be used either by EMOTE NAME  or by NUMBERS")
                await self.highrise.send_whisper(user.id, "\n•  Note that these commands will only work in room420's Rave. some expressions may not work because of restrictions.")

         if user.username.lower() in self.moderators:
            if message.lower().lstrip().startswith(("-mod","!mod")):
               await self.highrise.chat(f"\n  \n•Moderating :\n ____________________________\n !kick @username \n !ban @username \n !mute @username \n !unmute @username \n•Teleports : \n vip \n !vip @username \n !dj @username \n !d @username")
               await self.highrise.chat(f" \n •loops :\n ____________________________\n from L1 .. l16 \n•Poses :\nP1 and P2 ..etc")
             
         if message.lstrip().startswith(("!vip","!here","!giveVip","!d",'!1',"!2","!tip1", "!dj","!tip5","tip10","!tip50","!tip500"  )):
            response = await self.highrise.get_room_users()
            users = [content[0] for content in response.content]
            usernames = [user.username.lower() for user in users]
            parts = message[1:].split()
            args = parts[1:]

            if len(args) < 1:
                await self.highrise.send_whisper(user.id, f"Kullanım: !{parçalar[0]} <@Alionardo_>")
                return
            elif args[0][0] != "@":
                await self.highrise.send_whisper(user.id, "Invalid user format. Please use '@username'.")
                return
            elif args[0][1:].lower() not in usernames:
                await self.highrise.send_whisper(user.id, f"{args[0][1:]} is not in the room.")
                return

            user_id = next((u.id for u in users if u.username.lower() == args[0][1:].lower()), None)
            user_name = next((u.username.lower() for u in users if u.username.lower() == args[0][1:].lower()), None)
            if not user_id:
                await self.highrise.send_whisper(user.id, f"User {args[0][1:]} not found")
                return                     
            try:
                if message.startswith("!vip"):   
                  if user.username.lower() in self.moderators:
                    await self.highrise.teleport(user_id, Position(19, 5.75,16.5))
                if message.startswith("!giveVip"):   
                   if user.username == "Maebelle420" or user.username == "Maebelle420" :
                     if user_name.lower() not in self.membership:
                       self.membership.append(user_name)
                       self.save_membership()
                       await self.highrise.chat(f"Congratulations! {user_name}you been given a \n🎫 Permanent vip ticket 🎫 \n ____________________________\nUse the key vip to teleport")
                if message.startswith("!dj"):   
                  if user.username.lower() in self.moderators:
                    await self.highrise.teleport(user_id, Position(18.5,15.5,15.5))
                if message.startswith("!d"):   
                  if user.username.lower() in self.moderators:
                     await self.highrise.teleport(user_id, Position(13.5,0,15.5))
               
                if message.startswith("!tip1") and user.username  ==  "Maebelle420":
                    await self.highrise.tip_user(user_id, "gold_bar_1")
                if message.startswith("!tip5") and user.username  == "Maebelle420" :
                    await self.highrise.tip_user(user_id, "gold_bar_5")
                if message.startswith("!tip10") and user.username  ==  "Maebelle420" :
                  await self.highrise.tip_user(user_id, "gold_bar_10")
                if message.startswith("!tip50") and user.username  == "Maebelle420"  :
                  await self.highrise.tip_user(user_id, "gold_bar_50")
                if message.startswith("!tip500") and user.username  ==  "Maebelle420" :
                  await self.highrise.tip_user(user_id, "gold_bar_500")
                
            except Exception as e:
             print(f"An exception occurred[Due To {parts[0][1:]}]: {e}")

          
         if message.startswith("!time"):
            parts = message.split()
            if len(parts) == 2:
                target_mention = parts[1]

                # Remove the "@" symbol if present
                target_user = target_mention.lstrip('@')

                # Check if the target user has temporary VIP status
                remaining_time = self.remaining_time(target_user.lower())
                await self.highrise.send_whisper(user.id, f"Remaining time for {target_mention}'s temporary VIP status: {remaining_time}")
            else:
                await self.highrise.send_whisper(user.id, "Usage: !time @username")


       
         if message.startswith('vip') :
            if user.username.lower() in self.moderators or user.username.lower() in self.membership  or user.username.lower() in self.tempvip:    
              await self.highrise.teleport(f"{user.id}", Position(19, 5.75,16.5))
            else:
             await self.highrise.send_whisper((user.id)," this is a privet place for VIPs , uou can use it by purchaseing VIP membership  tye -buy")
         if message.startswith('dj') :
              if user.username.lower() in self.moderators:    
                await self.highrise.teleport(f"{user.id}", Position(18.5,15.5,15))

        
         if message.startswith('-d'):
             await self.highrise.teleport(f"{user.id}", Position(13.5,0,15.5))
           
        
         if message.startswith("/e1"):
                 await self.highrise.set_outfit(outfit=[
          Item(type='clothing', 
                    amount=1, 
                    id='body-flesh',
                    account_bound=False,
                    active_palette=12),
          Item(type='clothing',
                    amount=1,
                    id='shirt-n_starteritems2019raglanwhite',
                   account_bound=False,
                    active_palette=-1),
          Item(type='clothing', 
               amount=1, 
               id='pants-n_room12019blackacidwashjeans',
               account_bound=False,
               active_palette=-1),
          Item(type='clothing', 
               amount=1, 
               id='nose-n_01_b',
               account_bound=False,
               active_palette=-1),
         Item(type='clothing',
              amount=1, 
              id='watch-n_room32019blackwatch', 
              account_bound=False,
              active_palette=-1),
         Item(type='clothing', 
              amount=1, 
              id='watch-n_room32019blackwatch', 
              account_bound=False,
              active_palette=-1),
         Item(type='clothing', 
              amount=1, id='shoes-n_room22019tallsocks', 
              account_bound=False,
              active_palette=-1), 
         Item(type='clothing',
              amount=1, 
              id='shoes-n_converse_black',
              account_bound=False,
              active_palette=-1),       
         Item(type='clothing',
              amount=1, 
              id='freckle-n_basic2018freckle22', 
              account_bound=False,
              active_palette=-1),
         Item(type='clothing',
              amount=1,
              id='mouth-basic2018smirk',
              account_bound=False,
              active_palette=3),
         Item(type='clothing',
              amount=1,
              id= 'hair_back-n_malenew01',
              account_bound=False, active_palette=70),
        Item(type='clothing',
              amount=1,
              id= 'hair_front-n_malenew01',
              account_bound=False, active_palette=70),  
         Item(type='clothing', 
              amount=1, 
              id='eye-n_basic2018malediamondsleepy',
              account_bound=False,
              active_palette=2),
        Item(type='clothing', 
             amount=1,
             id='eyebrow-n_06', 
             account_bound=False,
             active_palette=-1)
      ])

         if  message.lower().startswith("wallet"):
            if user.username.lower() in self.moderators :

                  wallet = (await self.highrise.get_wallet()).content
                  await self.highrise.send_whisper(user.id, f"The bot wallet contains {wallet[0].amount} {wallet[0].type}")

            else: 
                await  self.highrise.send_whisper(user.id, f"Only Moderators Can View the Wallet")

         if message.startswith("Loop"):
           emote_name = message[5:].strip()
           if emote_name in self.EMOTE_DICT:
               emote_id = self.EMOTE_DICT[emote_name]
               delay = 7
               if " " in emote_name:
                   emote_name, delay_str = emote_name.split(" ")
                   if delay_str.isdigit():
                       delay = float(delay_str)

               if user.id in self.continuous_emote_tasks and not self.continuous_emote_tasks[user.id].cancelled():
                   await self.stop_continuous_emote(user.id)

               task = asyncio.create_task(self.send_continuous_emote(emote_id, user.id,delay))
               self.continuous_emote_tasks[user.id] = task  

         elif message.lower().startswith("stop"):
           if user.id in self.continuous_emote_tasks and not self.continuous_emote_tasks[user.id].cancelled():
               await self.stop_continuous_emote(user.id)

               await self.highrise.chat("Continuous emote has been stopped.")
           else:
               await self.highrise.chat("You don't have an active loop_emote.")
         elif message.lower().startswith("users"):
           room_users = (await self.highrise.get_room_users()).content
           await self.highrise.chat(f"There are {len(room_users)} users in the room")
         if message.startswith("0"):
           await self.highrise.send_emote("emote-float", user.id)
         if message.startswith("2"):
           await self.highrise.send_emote("dance-tiktok2", user.id)   
         if message.startswith("3"):
           await self.highrise.send_emote("emote-pose1", user.id)
         if message.startswith("4"):
           await self.highrise.send_emote("dance-shoppingcart", user.id)
         if message.startswith("5"):
           await self.highrise.send_emote("dance-russian", user.id)
         if message.startswith("6"):
           await self.highrise.send_emote("idle_singing", user.id)
         if message.startswith("7"):
           await self.highrise.send_emote("idle-enthusiastic", user.id)  
         if message.startswith("8"):
           await self.highrise.send_emote("idle-dance-casual", user.id)   
         if message.startswith("9"):
           await self.highrise.send_emote("idle-loop-sitfloor", user.id)
         if message.startswith("10"):
           await self.highrise.send_emote("emote-lust", user.id)
         if message.startswith("11"):
           await self.highrise.send_emote("emote-greedy", user.id)
         if message.startswith("12"):
           await self.highrise.send_emote("emote-bow", user.id)
         if message.startswith("13"):
           await self.highrise.send_emote("emote-curtsy", user.id)
         if message.startswith("14"):
           await self.highrise.send_emote("emote-snowball", user.id)
         if message.startswith("15"):
           await self.highrise.send_emote("emote-snowangel", user.id)
         if message.startswith("16"):
           await self.highrise.send_emote("emote-confused", user.id)
         if message.startswith("17"):
           await self.highrise.send_emote("emote-teleporting", user.id)
         if message.startswith("18"):
           await self.highrise.send_emote("emote-swordfight", user.id)
         if message.startswith("19"):
           await self.highrise.send_emote("emote-energyball", user.id)
         if message.startswith("20"):
           await self.highrise.send_emote("dance-tiktok8", user.id)
         if message.startswith("21"):
           await self.highrise.send_emote("dance-blackpink", user.id)
         if message.startswith("22"):
           await self.highrise.send_emote("emote-model", user.id)
         if message.startswith("23"):
           await self.highrise.send_emote("dance-pennywise", user.id)
         if message.startswith("24"):
           await self.highrise.send_emote("dance-tiktok10", user.id)
         if message.startswith("25"):
           await self.highrise.send_emote("emote-telekinesis", user.id)
         if message.startswith("26"):
           await self.highrise.send_emote("emote-hot", user.id)
         if message.startswith("27"):
           await self.highrise.send_emote("dance-weird", user.id)
         if message.startswith("28"):
           await self.highrise.send_emote("emote-pose7", user.id)
         if message.startswith("29"):
           await self.highrise.send_emote("emote-pose8", user.id)
         if message.startswith("30"):
           await self.highrise.send_emote("emote-pose3", user.id)
         if message.startswith("31"):
           await self.highrise.send_emote("emote-pose5", user.id)  
         if message.startswith("32"):
           await self.highrise.send_emote("emote-pose5", user.id)  
         if message.startswith("31"):
           await self.highrise.send_emote("emote-pose5", user.id)  
         if message.startswith("31"):
           await self.highrise.send_emote("emote-pose5", user.id)   


         if message.lower().strip() == "lambipose":
           await self.highrise.send_emote("emote-superpose", user.id)
         elif message.lower().strip() == "tiktok10":
           await self.highrise.send_emote("Gtg", user.id)
         elif message.lower().strip() == "tiktok10":
            await self.highrise.send_emote("idle-toilet", user.id)
         elif message.lower().strip() == "gravedance":
           await self.highrise.send_emote("dance-weird", user.id)
         elif message.lower().strip() == "fighter":
           await self.highrise.send_emote("idle-fighter", user.id)
         elif message.lower().strip() == "tiktok7":
           await self.highrise.send_emote("idle-dance-tiktok7", user.id)
         elif message.lower().strip() == "singalong":
           emote_name = "idle_singing"
         elif message.lower().strip() == "froggiehop":
           await self.highrise.send_emote("emote-frog", user.id)
         elif message.lower().strip() == "tiktok9":
           await self.highrise.send_emote("dance-tiktok9", user.id)
         elif message.lower().strip() == "swordfight":
           emote_name ="emote-swordfight"
         elif message.lower().strip() == "energyball":
           await self.highrise.send_emote("emote-energyball", user.id)
         elif message.lower().strip() == "emotecute":
           await self.highrise.send_emote("emote-cute", user.id)
         elif message.lower().strip() == "floating":
           await self.highrise.send_emote("emote-float", user.id)
         elif message.lower().strip() == "teleport":
           emote_name = "emote-teleporting"
         elif message.lower().strip() == "telekinesis":
           await self.highrise.send_emote("emote-telekinesis", user.id)
         elif message.lower().strip() == "maniac":
           await self.highrise.send_emote("emote-maniac", user.id)
         elif message.lower().strip() == "embarrassed":
           await self.highrise.send_emote("emote-embarrassed", user.id)
         elif message.lower().strip() == "pissedoff":
           await self.highrise.send_emote("emote-frustrated", user.id)
         elif message.lower().strip() == "slap":
           await self.highrise.send_emote("emote-slap", user.id)
         elif message.lower().strip() == "yılan":
           await self.highrise.send_emote("emote-snake", user.id)
         elif message.lower().strip() == "enth":
           await self.highrise.send_emote("idle-enthusiastic", user.id)
         elif message.lower().strip() == "confusion":
           await self.highrise.send_emote("emote-confused", user.id)
         elif message.lower().strip() == "shopping":
           await self.highrise.send_emote("dance-shoppingcart", user.id)
         elif message.lower().strip() == "roll":
           await self.highrise.send_emote("emote-roll", user.id)
         elif message.lower().strip() == "rofl":
           await self.highrise.send_emote("emote-rofl", user.id)
         elif message.lower().strip() == "superpunch":
           await self.highrise.send_emote("emote-superpunch", user.id)
         elif message.lower().strip() == "superrun":
           await self.highrise.send_emote("emote-superrun", user.id)
         elif message.lower().strip() == "creepycute":
           await self.highrise.send_emote(" emote-creepycute", user.id)
         elif message.lower().strip() == "superkick":
           await self.highrise.send_emote("emote-kicking", user.id)
         elif message.lower().strip() == "zombiedance":
           await self.highrise.send_emote("dance-zombie", user.id)
         elif message.lower().strip() == "monsterfail":
           await self.highrise.send_emote("emote-monster_fail", user.id)
         elif message.lower().strip() == "peekaboo":
           await self.highrise.send_emote("emote-peekaboo", user.id)
         elif message.lower().strip() == "sumofight":
           await self.highrise.send_emote("emote-sumo", user.id)
         elif message.lower().strip() == "charging":
           await self.highrise.send_emote("emote-charging", user.id)
         elif message.lower().strip() == "ninjarun":
           await self.highrise.send_emote("emote-ninjarun", user.id)
         elif message.lower().strip() == "proposing":
           await self.highrise.send_emote("emote-proposing", user.id)
         elif message.lower().strip() == "ropepull":
           await self.highrise.send_emote("emote-ropepull", user.id)
         elif message.lower().strip() == "secrethandshake":
           await self.highrise.send_emote("emote-secrethandshake", user.id)
         elif message.lower().strip() == "elbowbump":
           await self.highrise.send_emote("emote-elbowbump", user.id)
         elif message.lower().strip() == "homerun":
           await self.highrise.send_emote("emote-baseball", user.id)
         elif message.lower().strip() == "relaxing":
           await self.highrise.send_emote("idle-floorsleeping2", user.id)
         elif message.lower().strip() == "hug":
           await self.highrise.send_emote("emote-hug", user.id)
         elif message.lower().strip() == "cozynap":
           await self.highrise.send_emote("idle-floorsleeping", user.id)
         elif message.lower().strip() == "hugyourself":
           await self.highrise.send_emote("emote-hugyourself", user.id)
         elif message.lower().strip() == "snowballfight":
           await self.highrise.send_emote("emote-snowball", user.id)
         elif message.lower().strip() == "sweating":
           await self.highrise.send_emote("emote-hot", user.id)
         elif message.lower().strip() == "levelup":
           await self.highrise.send_emote("emote-levelup", user.id)
         elif message.lower().strip() == "snowangel":
           await self.highrise.send_emote("emote-snowangel", user.id)      
         elif message.lower().strip() == "gotago":
           await self.highrise.send_emote("emote-gotago", user.id)          

         elif message.lower().strip() == "posh":
           await self.highrise.send_emote("idle-posh", user.id)
         elif message.lower().strip() == "fallingapart":
           await self.highrise.send_emote("emote-apart", user.id)
         elif message.lower().strip() == "poutyface":
           await self.highrise.send_emote("idle-sad", user.id)
         elif message.lower().strip() == "Irritated":
           await self.highrise.send_emote("idle-angry", user.id)
         elif message.lower().strip() == "heroentrance":
           await self.highrise.send_emote("emote-hero", user.id)
         elif message.lower().strip() == "heropose":
           await self.highrise.send_emote("idle-hero", user.id)
         elif message.lower().strip() == "russiandance":
           await self.highrise.send_emote("dance-russian", user.id)
         elif message.lower().strip() == "curtsy":
           await self.highrise.send_emote("emote-curtsy", user.id)
         elif message.lower().strip() == "bow":
           await self.highrise.send_emote("emote-bow", user.id)
         elif message.lower().strip() == "ponder":
           await self.highrise.send_emote("idle-lookup", user.id)
         elif message.lower().strip() == "headball":
           await self.highrise.send_emote("emote-headball", user.id)
         elif message.lower().strip() == "clumsy":
           await self.highrise.send_emote("emote-fail2", user.id)
         elif message.lower().strip() == "fall":
           await self.highrise.send_emote("emote-fail1", user.id)
         elif message.lower().strip() == "penny":
           await self.highrise.send_emote("dance-pennywise", user.id)
         elif message.lower().strip() == "boo":
           await self.highrise.send_emote("emote-boo", user.id)
         elif message.lower().strip() == "fly":
           await self.highrise.send_emote("emote-wings", user.id)
         elif message.lower().strip() == "floss":
           await self.highrise.send_emote("dance-floss", user.id)
         elif message.lower().strip() == "kpop":
           await self.highrise.send_emote("dance-blackpink", user.id)
         elif message.lower().strip() == "model":
           await self.highrise.send_emote("emote-model", user.id)
         elif message.lower().strip() == "theatrical":
           await self.highrise.send_emote("emote-theatrical", user.id)
         elif message.lower().strip() == "amused":
           await self.highrise.send_emote("emote-laughing2", user.id)
         elif message.lower().strip() == "jetpack":
           await self.highrise.send_emote("emote-jetpack", user.id)
         elif message.lower().strip() == "bunnyhop":
           await self.highrise.send_emote("emote-bunnyhop", user.id)
         elif message.lower().strip() == "zombie":
           await self.highrise.send_emote("Idle_zombie", user.id)
         elif message.lower().strip() == "collapse":
           await self.highrise.send_emote("emote-death2", user.id)
         elif message.lower().strip() == "revival":
           await self.highrise.send_emote("emote-death", user.id)
         elif message.lower().strip() == "disco":
           await self.highrise.send_emote("emote-disco", user.id)
         elif message.lower().strip() == "harlem":
           await self.highrise.send_emote("emote-harlemshake", user.id)
         elif message.lower().strip() == "dance zombie":
            await self.highrise.send_emote("dance-zombie", user.id)
         elif message.lower().strip() == "attentive":
           await self.highrise.send_emote("idle_layingdown", user.id)
         elif message.lower().strip() == "faint":
           await self.highrise.send_emote("emote-faint", user.id)
         elif message.lower().strip() == "cold":
           await self.highrise.send_emote("emote-cold", user.id)
         elif message.lower().strip() == "sleepy":
           await self.highrise.send_emote("idle-sleep", user.id)
         elif message.lower().strip() == "handstand":
           await self.highrise.send_emote("emote-handstand", user.id)
         elif message.lower().strip() == "ghostfloat":
           await self.highrise.send_emote("emote-ghost-idle", user.id)
         elif message.lower().strip() == "ghost":
           await self.highrise.send_emote("emoji-ghost", user.id)
         elif message.lower().strip() == "splitsdrop":
           await self.highrise.send_emote("emote-splitsdrop", user.id)
         elif message.lower().strip() == "yogaflow":
           await self.highrise.send_emote("dance-spiritual", user.id)
         elif message.lower().strip() == "smoothwalk":
           await self.highrise.send_emote("dance-smoothwalk", user.id)
         elif message.lower().strip() == "ringonit":
           await self.highrise.send_emote("dance-singleladies", user.id)
         elif message.lower().strip() == "sick":
           await self.highrise.send_emote("emoji-sick", user.id)
         elif message.lower().strip() == "wiggledance":
           await self.highrise.send_emote("dance-sexy", user.id)
         elif message.lower().strip() == "robotic":
           await self.highrise.send_emote("dance-robotic", user.id)
         elif message.lower().strip() == "naughty":
           await self.highrise.send_emote("emoji-naughty", user.id)
         elif message.lower().strip() == "pray":
           await self.highrise.send_emote("emoji-pray", user.id)
         elif message.lower().strip() == "duckwalk":
           await self.highrise.send_emote("dance-duckwalk", user.id)
         elif message.lower().strip() == "faintdrop":
           await self.highrise.send_emote("emote-deathdrop", user.id)
         elif message.lower().strip() == "voguehands":
           await self.highrise.send_emote("dance-voguehands", user.id)
         elif message.lower().strip() == "orangejuicedance":
           await self.highrise.send_emote("dance-orangejustice", user.id)
         elif message.lower().strip() == "tiktok8":
           await self.highrise.send_emote("dance-tiktok8", user.id)
         elif message.lower().strip() == "hearthands":
           await self.highrise.send_emote("emote-heartfingers", user.id)
         elif message.lower().strip() == "partnerheartarms":
           await self.highrise.send_emote("emote-heartshape", user.id)
         elif message.lower().strip() == "levitate":
           await self.highrise.send_emote("emoji-halo", user.id)
         elif message.lower().strip() == "sneeze":
           await self.highrise.send_emote("emoji-sneeze", user.id)
         elif message.lower().strip() == "tiktok2":
           await self.highrise.send_emote("dance-tiktok2", user.id)
         elif message.lower().strip() == "rockout":
           await self.highrise.send_emote("dance-metal", user.id)
         elif message.lower().strip() == "pushups":
           await self.highrise.send_emote("dance-aerobics", user.id)
         elif message.lower().strip() == "karate":
           await self.highrise.send_emote("dance-martial-artist", user.id)
         elif message.lower().strip() == "macarena":
           await self.highrise.send_emote("dance-macarena", user.id)
         elif message.lower().strip() == "handsintheair":
           await self.highrise.send_emote("dance-handsup", user.id)
         elif message.lower().strip() == "breakdance":
           await self.highrise.send_emote("dance-breakdance", user.id)
         elif message.lower().strip() == "fireballlunge":
           await self.highrise.send_emote("emoji-hadoken", user.id)
         elif message.lower().strip() == "arrogance":
           await self.highrise.send_emote("emoji-arrogance", user.id)
         elif message.lower().strip() == "smirk":
           await self.highrise.send_emote("emoji-smirking", user.id)
         elif message.lower().strip() == "lying":
           await self.highrise.send_emote("emoji-lying", user.id)
         elif message.lower().strip() == "giveup":
           await self.highrise.send_emote("emoji-give-up", user.id)
         elif message.lower().strip() == "punch":
           await self.highrise.send_emote("emoji-punch", user.id)
         elif message.lower().strip() == "stinky":
           await self.highrise.send_emote("emoji-poop", user.id)
         elif message.lower().strip() == "point":
           await self.highrise.send_emote("emoji-there", user.id)
         elif message.lower().strip() == "annoyed":
           await self.highrise.send_emote("idle-loop-annoyed", user.id)
         elif message.lower().strip() == "taploop":
           await self.highrise.send_emote("idle-loop-tapdance", user.id)
         elif message.lower().strip() == "bummed":
           await self.highrise.send_emote("idle-loop-sad", user.id)
         elif message.lower().strip() == "chillin":
           await self.highrise.send_emote("idle-loop-happy", user.id)
         elif message.lower().strip() == "aerobics":
           await self.highrise.send_emote("idle-loop-aerobics", user.id)
         elif message.lower().strip() == "boogieswing":
           await self.highrise.send_emote("idle-dance-swinging", user.id)
         elif message.lower().strip() == "think":
           await self.highrise.send_emote("emote-think", user.id)
         elif message.lower().strip() == "blastoff":
           await self.highrise.send_emote("emote-disappear", user.id)
         elif message.lower().strip() == "gasp":
           await self.highrise.send_emote("emoji-scared", user.id)
         elif message.lower().strip() == "eyeroll":
           await self.highrise.send_emote("emoji-eyeroll", user.id)
         elif message.lower().strip() == "sob":
           await self.highrise.send_emote("emoji-crying", user.id)
         elif message.lower().strip() == "frolic":
           await self.highrise.send_emote("emote-frollicking", user.id)
         elif message.lower().strip() == "graceful":
           await self.highrise.send_emote("emote-graceful", user.id)
         elif message.lower().strip() == "otur":
           await self.highrise.send_emote("sit-idle-cute", user.id)
         elif message.lower().strip() == "greedyemote":
           await self.highrise.send_emote("emote-greedy", user.id)
         elif message.lower().strip() == "flirtywave":
           await self.highrise.send_emote("emote-lust", user.id)
         elif message.lower().strip() == "tiredx":
           await self.highrise.send_emote("idle-loop-tired", user.id)
         elif message.lower().strip() == "tummyache":
           await self.highrise.send_emote("emoji-gagging", user.id)
         elif message.lower().strip() == "flex":
           await self.highrise.send_emote("emoji-flex", user.id)
         elif message.lower().strip() == "raisetheroof":
           await self.highrise.send_emote("emoji-celebrate", user.id)
         elif message.lower().strip() == "cursingemote":
           await self.highrise.send_emote("emoji-cursing", user.id)
         elif message.lower().strip() == "stunned":
           await self.highrise.send_emote("emoji-dizzy", user.id)
         elif message.lower().strip() == "mindblown":
           await self.highrise.send_emote("emote-mindblown", user.id)
         elif message.lower().strip() == "shy":
           await self.highrise.send_emote("idle-loop-shy", user.id)
         elif message.lower().strip() == "sit":
           await self.highrise.send_emote("idle-loop-sitfloor", user.id)
         elif message.lower().strip() == "thumbsup":
           await self.highrise.send_emote("emote-thumbsup", user.id)
         elif message.lower().strip() == "clap":
           await self.highrise.send_emote("emote-clap", user.id)
         elif message.lower().strip() == "angry":
           await self.highrise.send_emote("emote-mad", user.id)
         elif message.lower().strip() == "tired":
           await self.highrise.send_emote("emote-sleepy", user.id)
         elif message.lower().strip() == "thewave":
           await self.highrise.send_emote("emote-thewave", user.id)
         elif message.lower().strip() == "thumbsuck":
           await self.highrise.send_emote("emote-suckthumb", user.id)
         elif message.lower().strip() == "shy":
           await self.highrise.send_emote("idle-loop-shy", user.id)
         elif message.lower().strip() == "peace":
           await self.highrise.send_emote("emote-peace", user.id)
         elif message.lower().strip() == "panic":
           await self.highrise.send_emote("emote-panic", user.id)
         elif message.lower().strip() == "jump":
           await self.highrise.send_emote("emote-jumpb", user.id)
         elif message.lower().strip() == "loveflutter":
           await self.highrise.send_emote("emote-hearteyes", user.id)
         elif message.lower().strip() == "exasperated":
           await self.highrise.send_emote("emote-exasperated", user.id)
         elif message.lower().strip() == "facepalm":
           await self.highrise.send_emote("emote-exasperatedb", user.id)
         elif message.lower().strip() == "dab":
           await self.highrise.send_emote("emote-dab", user.id)
         elif message.lower().strip() == "gangnamstyle":
           await self.highrise.send_emote("emote-gangnam", user.id)
         elif message.lower().strip() == "harlemshake":
           await self.highrise.send_emote("emote-harlemshake", user.id)
         elif message.lower().strip() == "tapdance":
           await self.highrise.send_emote("emote-tapdance", user.id)
         elif message.lower().strip() == "yes":
           await self.highrise.send_emote("emote-yes", user.id)
         elif message.lower().strip() == "sad":
           await self.highrise.send_emote("emote-sad", user.id)
         elif message.lower().strip() == "robot":
           await self.highrise.send_emote("emote-robot", user.id)
         elif message.lower().strip() == "rainbow":
           await self.highrise.send_emote("emote-rainbow", user.id)
         elif message.lower().strip() == "no":
           await self.highrise.send_emote("emote-no", user.id)
         elif message.lower().strip() == "nightfever":
           await self.highrise.send_emote("emote-nightfever", user.id)
         elif message.lower().strip() == "laugh":
           await self.highrise.send_emote("emote-laughing", user.id)
         elif message.lower().strip() == "kiss":
           await self.highrise.send_emote("emote-kiss", user.id)
         elif message.lower().strip() == "judochop":
           await self.highrise.send_emote("emote-judochop", user.id)
         elif message.lower().strip() == "hello":
           await self.highrise.send_emote("emote-hello", user.id)
         elif message.lower().strip() == "happy":
           await self.highrise.send_emote("emote-happy", user.id)
         elif message.lower().strip() == "moonwalk":
           await self.highrise.send_emote("emote-gordonshuffle", user.id)
         elif message.lower().strip() == "zombierun":
           await self.highrise.send_emote("emote-zombierun", user.id)
         elif message.lower().strip() == "cheerful":
           await self.highrise.send_emote("emote-pose8", user.id)
         elif message.lower().strip() == "embracingmodel":
           await self.highrise.send_emote("emote-pose7", user.id)
         elif message.lower().strip() == "embracing":
           await self.highrise.send_emote("emote-pose7", user.id)
         elif message.lower().strip() == "fashionpose":
           await self.highrise.send_emote("emote-pose5", user.id)
         elif message.lower().strip() == "fashion":
           await self.highrise.send_emote("emote-pose5", user.id)
         elif message.lower().strip() == "ichallengeyou":
           await self.highrise.send_emote("emote-pose3", user.id)
         elif message.lower().strip() == "challenge":
           await self.highrise.send_emote("emote-pose3", user.id)
         elif message.lower().strip() == "flirtywink":
           await self.highrise.send_emote("emote-pose1", user.id)
         elif message.lower().strip() == "wink":
           await self.highrise.send_emote("emote-pose1", user.id)

         elif message.lower().strip() == "casualdance":
           await self.highrise.send_emote("idle-dance-casual", user.id)
         elif message.lower().strip() == "casual":
           await self.highrise.send_emote("idle-dance-casual", user.id)
         elif message.lower().strip() == "cutie":
           await self.highrise.send_emote("emote-cutey", user.id)

         elif message.lower().strip() == "zerogravity":
           await self.highrise.send_emote("emote-astronaut", user.id)
         elif message.lower().strip() == "tiktok4":
           await self.highrise.send_emote("idle-dance-tiktok4", user.id)
         elif message.lower().strip() == "tiktok4":
           await self.highrise.send_emote("idle-dance-tiktok4", user.id)
         elif message.lower().strip() == "tiktok4":
           await self.highrise.send_emote("idle-dance-tiktok4", user.id)

         elif message.lower().strip() == "rock":
           await self.highrise.send_emote("emote-punkguitar", user.id)
         elif message.lower().strip() == "punk":
           await self.highrise.send_emote("emote-punkguitar", user.id)
         elif message.lower().strip() == "Sayso":
            await self.highrise.send_emote("emote-punkguitar", user.id)
         elif message.lower().strip() == "icecream":
           await self.highrise.send_emote("dance-icecream", user.id)
         elif message.lower().strip() == "gravity":
           await self.highrise.send_emote("emote-gravity", user.id)
         elif message.lower().strip() == "fashionista":
           await self.highrise.send_emote("emote-fashionista", user.id)
         elif message.lower().strip() == "uwu":
           await self.highrise.send_emote("idle-uwu", user.id)
         elif message.lower().strip() == "uwumood":
           await self.highrise.send_emote("idle-uwu", user.id)
         elif message.lower().strip() == "wrong":
           await self.highrise.send_emote("dance-wrong", user.id)
         elif message.lower().strip() == "dancewrong":
            await self.highrise.send_emote('idle-dance-tiktok4')

         if user.username.lower() in self.moderators:
                   roomUsers = (await self.highrise.get_room_users()).content

                   emote_name = None
                  
             
                   if message == ("L14"):
                     emote_name = ("idle-dance-casual")
                   elif message == ("L15"):
                     emote_name = ("idle-dance-tiktok4")
                  
                   elif message.startswith ("L0"):
                      emote_name = "emote-astronaut" 
                   elif message.startswith ("L1"):
                     emote_name = "dance-tiktok8"
                   elif message.startswith ("L2"):
                     emote_name = "dance-blackpink"
                   elif message.startswith ("L3"):
                     emote_name = "dance-tiktok2"
                   elif message.startswith ("L4"):
                     emote_name = "dance-pennywise"
                   elif message.startswith ("Bow"):
                     emote_name = "emote-bow"
                   elif message.startswith ("L5"):
                     emote_name = "dance-russian"
                   elif message.startswith ("Curtsy"):
                     emote_name = "L6"
                   elif message.startswith ("Snowball"):
                     emote_name = "emote-snowball"
                   elif message.startswith ("Spiiicy"):
                     emote_name = "emote-hot"
                   elif message.startswith("s1"):
                     emote_name = "emote-snowangel"
                   elif message.startswith("Drop"):
                     emote_name = "emote-charging"
                   elif message.startswith("L7"):
                     emote_name = "dance-shoppingcart"
                   elif message.startswith("Confuse"):
                     emote_name = "emote-confused"
                   elif message.startswith("Entu"):
                     emote_name = "idle-enthusiastic"
                   elif message.startswith("Telek"):
                     emote_name = "emote-telekinesis"
                   elif message.startswith("Fly"):
                     emote_name = "emote-float"
                   elif message.startswith("Tele"):
                     emote_name = "emote-teleporting"
                   elif message.startswith("Fight"):
                     emote_name = "emote-swordfight"
                   elif message.startswith("Maniac"):
                     emote_name = "emote-maniac"
                   elif message.startswith("Rise"):
                     emote_name = "emote-energyball"
                   elif message.startswith("Snake"):
                     emote_name = "emote-snake"
                   elif message.startswith("L8"):
                     emote_name = "idle_singing"
                   elif message.startswith("Frog"):
                     emote_name = "emote-frog"
                   elif message.startswith("Lambi"):
                     emote_name = "emote-superpose"
                   elif message.startswith("Cute"):
                     emote_name = "emote-cute"
                   elif message.startswith("L9"):
                     emote_name = "dance-tiktok9"
                   elif message.startswith("L10"):
                     emote_name = "dance-weird"
                   elif message.startswith("L11"):
                     emote_name = "dance-tiktok10"

                   elif message.startswith("P1"):
                     emote_name = "emote-pose7"
                   elif message.startswith("P2"):
                     emote_name = "emote-pose8"
                   elif message.startswith("L16"):
                     emote_name = "idle-dance-casual"
                   elif message.startswith("P3"):
                     emote_name = "emote-pose1"
                   elif message.startswith("P4"):
                     emote_name = "emote-pose3"
                   elif message.startswith("P5"):
                     emote_name = "emote-pose5"
                   elif message.startswith("Cutey"):
                     emote_name = "emote-cutey"
                   elif message.startswith("L13"):
                     emote_name = "dance-icecream"
                  
                   elif message.startswith("L12"):
                     emote_name = "emote-punkguitar"
                  
                   if emote_name is not None:
                    try:
                        if self.emote_looping:
                            self.emote_looping = False
                            await self.highrise.send_whisper(user.id, "Type Emote Again, Next time Type !stop before typing new emote.")
                        else:
                            self.emote_looping = True
                            while self.emote_looping:
                                for roomUser, _ in roomUsers:
                                    await self.highrise.send_emote(emote_name, roomUser.id)
                                await asyncio.sleep(7)  # Adjust the delay between emotes as needed
                    except asyncio.CancelledError:
                        pass

         if message == "!stop":
                if user.username.lower() in self.moderators:
                    self.emote_looping = False
                    await self.highrise.send_whisper(user.id, "Emote looping stopped.")
      except Exception as e:
        print(f"An exception occured: {e}")  


    async def follow_user(self, target_username: str):
      while self.following_username == target_username:

          response = await self.highrise.get_room_users()
          target_user_position = None
          for user_info in response.content:
              if user_info[0].username.lower() == target_username.lower():
                  target_user_position = user_info[1]
                  break

          if target_user_position:
              nearby_position = Position(target_user_position.x + 1.0, target_user_position.y, target_user_position.z)
              await self.highrise.walk_to(nearby_position)

              await asyncio.sleep(2)
            
    async def on_whisper(self, user: User, message: str ) -> None:

        if message == "here":
            if user.username.lower() in self.moderators:
                response = await self.highrise.get_room_users()
                users = [content for content in response.content]
                for u in users:
                    if u[0].id == user.id:
                        try:
                            await self.highrise.teleport(Counter.bot_id,Position((u[1].x),(u[1].y),(u[1].z),"FrontRight"))


                            break
                        except:

                            pass
       
        if message.startswith("/say"):
            if user.username.lower() in self.moderators:
                text = message.replace("/say", "").strip()
                await self.highrise.chat(text)

   
         

        elif message.startswith("/come"):
            if user.username.lower() in self.moderators:
                response = await self.highrise.get_room_users()
                your_pos = None
                for content in response.content:
                    if content[0].id == user.id:
                        if isinstance(content[1], Position):
                            your_pos = content[1]
                            break
                if not your_pos:
                    await self.highrise.send_whisper(user.id, "Invalid coordinates!")
                    return
                await self.highrise.chat(f"@{user.username} I'm coming ..")
                await self.highrise.walk_to(your_pos)

        elif message.lower().startswith("/follow"):
         
            target_username = message.split("@")[1].strip()

            if target_username.lower() == self.following_username:
                await self.highrise.send_whisper(user.id,"I am already following.")
            elif message.startswith("/say"):
              if user.username.lower() in self.moderators:
                  text = message.replace("/say", "").strip()
                  await self.highrise.chat(text)
            else:
                self.following_username = target_username
                await self.highrise.chat(f"hey {target_username}.")
            
                await self.follow_user(target_username)
        elif message.lower() == "stop following":
            self.following_username = None
          
            await self.highrise.walk_to(Position(15.5,0,1.5,"FrontRight"))

  
  
              
    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem) -> None:
        try:
            print(f"{sender.username} tipped {receiver.username} an amount of {tip.amount}")
            await self.highrise.chat(f"𝓣𝓱𝓮 𝓐𝓶𝓪𝔃𝓲𝓷𝓰 {sender.username} 𝓽𝓲𝓹𝓹𝓮𝓭 {receiver.username} 𝓪𝓷 𝓪𝓶𝓸𝓾𝓷𝓽 𝓸𝓯  {tip.amount}𝐆𝐎𝐋𝐃")

            
            if tip.amount == 500:
              if receiver.username  == "420hotties":
                 sender_username = sender.username.lower()
                 self.membership.append(sender_username)
                 self.save_membership()
                 await self.highrise.chat(f"Thank you {sender_username} for purchasing PERMEANT vip membership , now u can use the command vip to teleport to the vip from now on ! 🎫") 
            if tip.amount == 100:
              if receiver.username  == "420hotties ":    
                 sender_username = sender.username.lower()

                 self.tempvip[sender_username] = int(time.time()) + 24 * 60 * 60  # VIP for 24 hours
                 self.save_tempvip()
                 await self.highrise.chat(f"Thank you {sender_username} for purchasing TRMPORARY vip membership , now u can use the command vip to teleport to the vip now ! 🎫") 

                 await self.highrise.teleport(sender_username, Position(17.5,7.5, 1.5))

        except Exception as e:
             print(f"An exception occured: {e}")

    async def dance_floor(self):

        while True:

            try:
                if self.dance_floor_pos and self.dancer:
                    ran = random.randint(1, 73)
                    emote_text, emote_time = await self.get_emote_df(ran)
                    emote_time -= 1

                    tasks = [asyncio.create_task(self.highrise.send_emote(emote_text, user_id)) for user_id in self.dancer]

                    await asyncio.wait(tasks)

                    await asyncio.sleep(emote_time)

                await asyncio.sleep(1)

            except Exception as e:
                print(f"{e}")

    #function to get emote
    async def get_emote_df(self, target) -> None:

        try:
            emote_info = self.emotesdf.get(target)
            return emote_info
        except ValueError:
            pass

    async def on_user_move(self, user: User, pos: Position | AnchorPosition) -> None:

    #get user position on move and add them on self.dancer if on dancefloor
      if user:
        print(f"{user.username}: {pos}")

        if self.dance_floor_pos:

            if isinstance(pos, Position):

                for dance_floor_info in self.dance_floor_pos:

                    if (
                        dance_floor_info[0] <= pos.x <= dance_floor_info[1] and
                        dance_floor_info[2] <= pos.y <= dance_floor_info[3] and
                        dance_floor_info[4] <= pos.z <= dance_floor_info[5]
                    ):

                        if user.id not in self.dancer:
                            self.dancer.append(user.id)

                        return

            # If not in any dance floor area
            if user.id in self.dancer:
                self.dancer.remove(user.id)

          
    async def send_continuous_emote(self, emote_id: str, user_id: int,emote_duration: float):
            try:
                while True:
                    await self.highrise.send_emote(emote_id, user_id)
                    await asyncio.sleep(emote_duration)
            except ConnectionResetError:
               if message.lower().lstrip().startswith("loop"):
                parts = message.split("6 ")
                if len(parts) < 2:
                    await self.highrise.chat("Invalid command format. Usage: loop<emote_name> ")
                    return

                emote_name = parts[1]

                if len(parts) >= 3:
                    try:
                        float(parts[2])
                    except ValueError:
                        await self.highrise.chat("Invalid delay value. The delay must be a valid number in seconds.")
                        return
                else:
                    pass  # Default delay of 7.5 seconds
  
    

    async def stop_continuous_emote(self, user_id: int):
      if user_id in self.continuous_emote_tasks and not self.continuous_emote_tasks[user_id].cancelled():
          task = self.continuous_emote_tasks[user_id]
          task.cancel()
          with contextlib.suppress(asyncio.CancelledError):
              await task
          del self.continuous_emote_tasks[user_id]
          
    




    
