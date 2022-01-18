#!/usr/bin/env python

import discord
import os
from env import *
client=discord.Client()

@client.event
async def on_ready():
   channel = client.get_channel(CHANNEL) 
   await channel.send('$Server-On') 
   exit()

client.run(TOKEN)          
