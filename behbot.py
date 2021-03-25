# bot.py
########################
# This file is part of BehBOT.
#
# BehBOT is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# BehBOT is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with BehBOT. If not, see <https://www.gnu.org/licenses/>.
########################
import os
import discord
from dotenv import load_dotenv
from urllib.parse import quote

import string_utils
import youtube_video
import youtube_search

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class DiscordBot(discord.Client):
	def __init__(self):
		super().__init__()
		self.__mVoiceHandle = None
			
	async def __connectToChannel(self, channel):
		await self.__disconnectFromChannel()	
		self.__mVoiceHandle = await channel.connect()
		
	async def __disconnectFromChannel(self):
		if self.__mVoiceHandle != None:
			await self.__mVoiceHandle.disconnect()
			return True
			
		return False
			
	async def __tryConnect(self, message, voice_channel):
		if voice_channel != None and voice_channel.channel != None:
			await self.__connectToChannel(voice_channel.channel)
			return True
			
		await message.channel.send("Connect to a voice channel!")
		return False

	async def __handleCommands(self, message, command, value):		
		if command == "!play":
			if len(value) > 0:
				if await self.__tryConnect(message, message.author.voice):
					video_info = None
					
					try:
						search_result = youtube_search.getYoutubeSearchResults(value.replace(' ', '+'))						
						if len(search_result) > 0:
							for i in range(0, len(search_result)):
								try:
									# Get the 'top' most result since it is (usually) the most relevant
									video_title = search_result[i].title
									video_videoSource = search_result[i].videoSource
									
									video_info = youtube_video.getYoutubeVideoInformation(youtube_video.getYoutubeVideoID(video_videoSource))
									video_info.originalVideoSource = video_videoSource
									break
								except youtube_video.VideoMetaDataException:
									continue
						else:
							await message.channel.send("Cannot find \"{0}\"".format(value))
						
						# ~ video_id = youtube_video.getYoutubeVideoID(value)
						# ~ video_information = youtube_video.getYoutubeVideoInformation(video_id)
						# ~ video_information.originalVideoSource = value
					except:
						await message.channel.send("Cannot play {0}".format(value))
						return
					
					if video_info != None and len(video_info.title) and len(video_info.videoSource) > 0:
						# Fix from user Mr_Spaar at https://stackoverflow.com/questions/61959495/when-playing-audio-the-last-part-is-cut-off-how-can-this-be-fixed-discord-py
						# Accessed March 2021
						FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
						
						print("Getting video from source {0}...".format(video_info.originalVideoSource))
						print("Found underlying video source at {0}...".format(video_info.videoSource))
						await message.channel.send("Playing \"{0}\"".format(video_info.title))
						self.__mVoiceHandle.play(discord.FFmpegPCMAudio(video_info.videoSource, **FFMPEG_OPTS))
						self.__mVoiceHandle.is_playing()
					else:
						await message.channel.send("Cannot play \"{0}\"".format(value))
						# ~ video_info = youtube_video.getYoutubeVideoInformation(youtube_video.getYoutubeVideoID(video_search_to_play.videoSource))
						# ~ if video_info == None:
							# ~ await message.channel.send("Cannot play \"{0}\"".format(video_search_to_play.title))
							# ~ return

						# ~ print("Found underlying video source at {0}...".format(video_info.videoSource))
						# ~ await message.channel.send("Playing: \"{0}\"".format(video_search_to_play.title))						
						# ~ self.__mVoiceHandle.play(discord.FFmpegPCMAudio(video_info.videoSource))
			else:
				await message.channel.send("No title specified")
		elif command == "!play_test":
			if len(value) > 0 :
				if await self.__tryConnect(message, message.author.voice):
					video_information = youtube_video.VideoInformation()
					try:
						video_id = youtube_video.getYoutubeVideoID(value)
						video_information = youtube_video.getYoutubeVideoInformation(video_id)
						video_information.originalVideoSource = value
					except youtube_video.VideoMetaDataException:
						return
						
					if len(video_information.title)> 0:
						# Fix from user Mr_Spaar at https://stackoverflow.com/questions/61959495/when-playing-audio-the-last-part-is-cut-off-how-can-this-be-fixed-discord-py
						# Accessed March 2021
						FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}
						
						await message.channel.send("Playing: \"{0}\"".format(video_information.title))
						print("Getting video from source {0}...".format(video_information.originalVideoSource))
						print("Found underlying video source at {0}...".format(video_information.videoSource))
						self.__mVoiceHandle.play(discord.FFmpegPCMAudio(video_information.videoSource, **FFMPEG_OPTS))
						self.__mVoiceHandle.is_playing()
			else:
				await message.channel.send("No title specified")
		elif command == "!stop":
			if self.__mVoiceHandle.is_playing():
				self.__mVoiceHandle.stop()
			await self.__disconnectFromChannel()
		else:
			await message.channel.send("Unknown command \"{0}\"".format(command))
		
	async def on_ready(self):
		print(f'{self.user} has connected to Discord!')

	async def on_message(self, message):
		if message.author == self.user:
			return

		(command, value) = string_utils.tokenizeKeyValue(message.content, ' ')
		value = string_utils.combineTokens(string_utils.tokenize(value, ' '))
		await self.__handleCommands(message, command, value)
						
client = DiscordBot()
client.run(TOKEN)
