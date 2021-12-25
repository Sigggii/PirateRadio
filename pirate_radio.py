import discord
from dotenv import load_dotenv
import os
from commands import Commands
from error.unknown_command_error import UnknownCommandError
from message_manager import write_command_error


class PirateRadio(discord.Client):

    async def on_ready(self):
        print("Joined")

    async def on_message(self, message: discord.Message):
        author: discord.Member = message.author
        if author == self.user:
            return
        command = Commands(message, self)
        try:
            await command.map_commands()
        except UnknownCommandError as err:
            await write_command_error(message, str(err))


if __name__ == '__main__':
    try:
        load_dotenv('.env')
    except Exception:
        pass
    client: discord.Client = PirateRadio()
    client.run(os.getenv('bot-token'))
