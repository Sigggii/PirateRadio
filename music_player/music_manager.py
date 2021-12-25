from typing import Optional
import discord
from entities.yt_video import YTvideo, url_to_song
from error.playlist_not_found_error import PlaylistNotFoundError
from music_player.music_player import MusicPlayer
from message_manager import write_embeded_message, get_sucess_embed, get_error_embed


class MusicManager:

    def __init__(self, message: discord.Message, client: discord.Client):
        self.message: discord.Message = message
        self.client: discord.Client = client
        self.author: discord.Member = message.author

    async def play(self):
        url = self.parseUrl(self.message.content)
        voice_client = await self.get_voice_client()
        if voice_client:
            song = url_to_song(url)
            music_player = MusicPlayer(self.message.guild, voice_client, self.client)
            music_player.add_song(song)
            await self.write_added_song(song)
            if not voice_client.is_playing():
                music_player.play()

    async def play_playlist(self, playlist: str, shuffle: bool):
        print("test")
        voice_client = await self.get_voice_client()
        if voice_client:
            music_player = MusicPlayer(self.message.guild, voice_client, self.client)
            try:
                music_player.play_playlist(playlist, shuffle)
                await write_embeded_message(self.message.channel, get_sucess_embed('Playing', 'Playing playlist: ' + playlist))
            except PlaylistNotFoundError:
                await write_embeded_message(self.message.channel, get_error_embed('NOT FOUND', 'Playlist not found'))

    async def skip(self):
        voice_client = await self.get_voice_client()
        if voice_client:
            music_player = MusicPlayer(self.message.guild, voice_client, self.client)
            music_player.skip_song()

    async def pause(self):
        voice_client = await self.get_voice_client()
        if voice_client:
            voice_client.pause()

    async def resume(self):
        voice_client = await self.get_voice_client()
        if voice_client:
            voice_client.resume()

    async def get_voice_client(self) -> Optional[discord.VoiceClient]:
        if not self.message.guild:
            await write_embeded_message(self.message.channel,
                                        get_error_embed("No Server found", "To execute this "
                                                                                "command, plz go in a Voice-Channel on "
                                                                                "a Server, where I am avaiable"))
            return
        if not self.author.voice:
            await write_embeded_message(self.message.channel, get_error_embed("You are not in a Voice-Channel",
                                                                                   "To execute this command, "
                                                                                   "plz go in a Voice-Channel"))
            return

        guild: Optional[discord.Guild] = self.client.get_guild(self.message.guild.id)
        use_voice_client: Optional[discord.VoiceClient] = None
        if guild:
            use_voice_client = guild.voice_client

        if use_voice_client:
            if not use_voice_client.channel == self.author.voice.channel:
                await write_embeded_message(self.message.channel, get_error_embed("Im already connected to another "
                                                                                       "Channel",
                                                                                       "Maybe more luck next time :)"))
                return

        if not use_voice_client and len(self.client.voice_clients) == 0:
            use_voice_client = await self.author.voice.channel.connect()

        return use_voice_client

    def parseUrl(self, url: str):
        return url.split(" ")[1]

    async def write_added_song(self, song: YTvideo):
        message_string = "Added " + song.title + " from " + song.author + " to queue"
        await write_embeded_message(self.message.channel, get_sucess_embed("Song added", message_string))






