import discord
from error.unknown_command_error import UnknownCommandError
from music_player.music_manager import MusicManager
from music_player.playlist_manager import PlaylistManager


def concat_list_values(from_index, to_index, list: []):
    if to_index == -1:
        to_index = len(list)

    concat_string = ''
    for i in range(from_index, to_index-1):
        concat_string = concat_string + list[i] + ' '

    concat_string = concat_string + list[to_index-1]
    return concat_string


class Commands:

    def __init__(self, message: discord.Message, client: discord.Client):
        self.message: discord.Message = message
        self.client = client
        self.__author: discord.Member = message.author
        self.music_manager = MusicManager(self.message, self.client)

    async def map_commands(self):
        command_parts = self.message.content.split()
        if command_parts[0] == '!playlist':
            if not len(command_parts) >= 3:
                raise UnknownCommandError("!playlist <option> <name of playlist> ...")

            playlist_manager = PlaylistManager(self.message, command_parts[2])
            if command_parts[1] == 'create':
                await playlist_manager.create_playlist()

            elif command_parts[1] == 'delete':
                await playlist_manager.delete_playlist()

            elif command_parts[2] == 'play':
                if len(command_parts) == 4:
                    if command_parts[3] == 'shuffle':
                        await self.music_manager.play_playlist(command_parts[1], True)

                    else:
                        await self.music_manager.play_playlist(command_parts[1], False)

            elif len(command_parts) >= 4:
                playlist_manager = PlaylistManager(self.message, command_parts[1])
                if command_parts[2] == 'add':
                    await playlist_manager.add_video(command_parts[3])

                elif command_parts[2] == 'delete_title':
                    await playlist_manager.delete_video_by_title(concat_list_values(3, -1, command_parts))

                elif command_parts[2] == 'delete_author':
                    await playlist_manager.delete_video_by_author(command_parts[3])
                else:
                    raise UnknownCommandError("!playlist <name of playlist> <option> <input>")

            else:
                raise UnknownCommandError("!playlist <option> <name of playlist> ...")

        elif command_parts[0] == "!play":
            if not len(command_parts) == 2:
                raise UnknownCommandError("!play <yt-watch-url>")

            await self.music_manager.play()
            return

        elif command_parts[0] == "!skip":
            await self.music_manager.skip()
            return

        elif command_parts[0] == "!pause":
            await self.music_manager.pause()
            return

        elif command_parts[0] == "!resume":
            await self.music_manager.resume()
            return

        else:
            raise UnknownCommandError('!<command> ....')



    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value





