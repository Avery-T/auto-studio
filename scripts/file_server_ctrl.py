#!/usr/bin/env python

import sys 
import discord
import os
from env import *

switch = str(sys.argv[1]) #index zero is the name of the program not the cmd argument
client=discord.Client()

@client.event
async def on_ready():
    
   channel = client.get_channel(CHANNEL) 
   if switch == 'on': 
     await channel.send('$Server-On') 

   elif switch =='off': 
     await channel.send('$Server-Off') 

   exit()

client.run(TOKEN)          
