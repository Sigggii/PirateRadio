import discord
from typing import Union


async def write_response(message: discord.Message, content: str):
    channel = message.channel
    await channel.send(content=content)


async def write_embeded_response(message: discord.Message, content: discord.Embed):
    channel = message.channel
    await channel.send(embed=content)


async def write_message(channel: Union[discord.TextChannel, discord.DMChannel], content: str):
    await channel.send(content=content)


async def write_embeded_message(channel: Union[discord.TextChannel, discord.DMChannel], content: discord.Embed):
    await channel.send(embed=content)


def get_error_embed(title: str, message: str):
    embed = discord.Embed(title=title, colour=0xff0033)
    embed.description = message
    return embed


def get_sucess_embed(title: str, message: str):
    embed = discord.Embed(title=title, colour=0x42ba96)
    embed.description = message
    return embed


async def write_command_error(message: discord.Message, example_command: str):
    embed = get_error_embed("Unknown Command", "The command you used should look like this: " + example_command + "\n"
                                                                                                                  "for help enter \"!help\"")

    await write_embeded_message(message.channel, embed)
