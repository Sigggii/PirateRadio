import discord
from entities.yt_video import YTvideo
from error.playlist_not_found_error import PlaylistNotFoundError
from music_player.playlist_db import PlaylistDB
import random


class Playlist:
    def __init__(self, guild: discord.Guild, playlist_name: str):
        self.guild = guild
        self.playlist_name = playlist_name
        self.playlist_db = PlaylistDB()

    def create_playlist(self, author_id: int):
        self.playlist_db.create_playlist(self.guild.id, self.playlist_name, author_id)

    def add_video(self, video: YTvideo):
        return self.playlist_db.add_video(self.guild.id, self.playlist_name, video)

    def add_videos(self, videos: []):
        return self.playlist_db.add_videos(self.guild.id, self.playlist_name, videos)

    def delete_video_by_title(self, title: str):
        return self.playlist_db.delete_video_by_title(self.guild.id, self.playlist_name, title)

    def delete_video_by_author(self, author: str):
        return self.playlist_db.delete_video_by_author(self.guild.id, self.playlist_name, author)

    def delete_playlist(self):
        self.playlist_db.delete_playlist(self.guild.id, self.playlist_name)

    def get_videos(self, shuffle: bool):
        videos = self.playlist_db.get_videos(self.guild.id, self.playlist_name)
        if not videos:
            raise PlaylistNotFoundError()
        if shuffle:
            random.shuffle(videos)

        return videos

