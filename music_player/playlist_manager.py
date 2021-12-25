import discord
import pymongo.errors

import entities.yt_video

from entities.yt_video import url_to_song
from message_manager import write_embeded_message, get_error_embed, get_sucess_embed
from music_player.playlist import Playlist


class PlaylistManager():
    def __init__(self, message: discord.Message, playlist_name: str):
        self.message = message
        self.playlist_name = playlist_name
        self.playlist = Playlist(self.message.guild, self.playlist_name)

    async def create_playlist(self):
        try:
            self.playlist.create_playlist(self.message.author.id)
            await self.write_success_embed('Playlist created', 'Playlist was successfully created: ' + self.playlist_name)
        except pymongo.errors.DuplicateKeyError:
            await self.write_error_embed('Already exists', 'A Playlist with that name already exists on this Server')
        except pymongo.errors.PyMongoError:
            await self.write_error_embed("Couldn't create Playlist", 'Reason unknown')

    async def add_video(self, url: str):
        try:
            updated = self.playlist.add_video(url_to_song(url).to_mongo_entity())
            if updated >= 1:
                await self.write_success_embed('Video added', 'Video added to Playlist: ' + self.playlist_name)
            else:
                await self.write_error_embed('NOT FOUND', "Couldn't find Playlist: " + self.playlist_name)

        except pymongo.errors.PyMongoError:
            await self.write_error_embed("Couldn't add Video to Playlist: " + self.playlist_name, 'Reason unknown')

    async def add_videos(self, videos: []):
        try:
            updated = self.playlist.add_videos(videos)
            if updated >=1:
                await self.write_success_embed("Videos added",  "Videos added to playlist: " + self.playlist_name)
            else:
                await self.write_error_embed('NOT FOUND', "Couldn't find playlist: " + self.playlist_name)
        except pymongo.errors.PyMongoError:
            await self.write_error_embed("Couldn't add Videos to playlist: " + self.playlist_name, 'Reason unknown')

    async def delete_video_by_title(self, title: str):
        try:
            updated = self.playlist.delete_video_by_title(title)
            if updated >=1:
                await self.write_success_embed("Video Deleted", "Video(s) with the title " + title + " got deleted")
            else:
                await self.write_error_embed('NOT FOUND', "Couldn't find video or playlist: " + self.playlist_name)
        except pymongo.errors.PyMongoError:
            await self.write_error_embed("Couldn't delete Video", "Reason unknown")

    async def delete_video_by_author(self, author: str):
        try:
            updated = self.playlist.delete_video_by_author(author)
            if updated >=1:
                await self.write_success_embed("Video(s) Deleted", "Video(s) from the author:  " + author + " got deleted")
            else:
                await self.write_error_embed('NOT FOUND', "Couldn't find videos or playlist: " + self.playlist_name)
        except pymongo.errors.PyMongoError:
            await self.write_error_embed("Couldn't delete Video", 'Reason Unknown')

    async def delete_playlist(self):
        try:
            self.playlist.delete_playlist()
            await self.write_success_embed('Playlist deleted', 'Playlist ' + self.playlist_name + 'deleted')
        except pymongo.errors.PyMongoError:
            await self.write_error_embed("Couldn't delete playlist", 'Reason Unknown')

    async def write_success_embed(self, title: str, message: str):
        embed = get_sucess_embed(title, message)
        await write_embeded_message(self.message.channel, embed)

    async def write_error_embed(self, title: str, message: str):
        embed = get_error_embed(title, message)
        await write_embeded_message(self.message.channel, embed)






