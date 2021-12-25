import discord
from pytube import YouTube
from music_player.music_player_db import MusicPlayerDB
from typing import Optional
from entities.yt_video import YTvideo
import asyncio

from music_player.playlist import Playlist


class MusicPlayer:
    def __init__(self, guild: discord.Guild, voice_client: discord.VoiceClient, client: discord.Client):
        self.guild = guild
        self.client = client
        self.music_player_db = MusicPlayerDB()
        self.music_player_db.create_if_new(self.guild.id)
        self.voice_client: discord.VoiceClient = voice_client
        self.bool = False
        self.loop = None

    def play(self, error=None):
        self.bool = False
        audio = self.music_player_db.next_song(self.guild.id)
        if audio and self.voice_client:
            """if not self.loop:
                self.loop = asyncio.get_event_loop()
            self.loop.create_task(self.set_nickname(audio))"""
            url = YouTube(audio.url).streams.get_audio_only('webm').url
            self.music_player_db.change_currently_playing(audio, self.guild.id)
            self.voice_client.play(discord.FFmpegOpusAudio(executable="ffmpeg.exe", source=url,
                                                           before_options="-reconnect 1 -reconnect_at_eof 1 "
                                                                          "-reconnect_streamed 1 -reconnect_delay_max 2"),
                                   after=self.play)

    def play_playlist(self, playlist_name: str, shuffle: bool):
        playlist = Playlist(self.guild, playlist_name)
        videos = playlist.get_videos(shuffle)
        self.music_player_db.clear_queue(self.guild.id)
        self.music_player_db.add_songs(self.guild.id, videos)
        if self.voice_client.is_playing():
            self.skip_song()
        else:
            self.play()

    def add_song(self, song):
        self.music_player_db.add_song(song, self.guild.id)

    def skip_song(self):
        self.voice_client.stop()

    """async def set_nickname(self, song: YTvideo):
        self.bool = True
        bot_id = self.client.user.id
        bot_member: Optional[discord.Member] = self.guild.get_member(bot_id)
        if bot_member:
            nickname = bot_member.display_name
            while self.bool:
                await bot_member.edit(nick="Playing: "+ song.title[0:20])
                await asyncio.sleep(15)
                await bot_member.edit(nick="Artist: "+ song.author)
                await asyncio.sleep(15)

            await bot_member.edit(nick=nickname)"""


