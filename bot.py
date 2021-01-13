# bot.py

# imports
import os
import discord
import requests
from dotenv import load_dotenv

load_dotenv('.env')

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    # set text channel
    channel = client.get_channel(798683983885107224)

    # mythic+ affixes: !pumpin -affixes
    if message.content == '!pumpin -affixes':
        response = requests.get('http://raider.io/api/v1/mythic-plus/affixes?region=us')
        if response:
            content = response.json()
            names = content["title"] + '\n'
            two = f'2+ | {content["affix_details"][0]["name"]} | {content["affix_details"][0]["description"]}\n'
            four = f'4+ | {content["affix_details"][1]["name"]} | {content["affix_details"][1]["description"]}\n'
            seven = f'7+ | {content["affix_details"][2]["name"]} | {content["affix_details"][2]["description"]}\n'
            ten = f'10+ | {content["affix_details"][3]["name"]} | {content["affix_details"][3]["description"]}\n'
            await channel.send(f'**{names}**\n{two}\n{four}\n{seven}\n{ten}')

    # mythic+ top 4 weekly keys: !pumpin -weekly {character name}
    # set to illidan server, US region
    elif message.content.startswith('!pumpin -weekly'):
        tokens = message.content.split(' ')
        name = tokens[2].capitalize()
        response = requests.get(f'http://raider.io/api/v1/characters/profile?region=us&realm=illidan&name={name}&fields=mythic_plus_weekly_highest_level_runs')
        if response:
            content = response.json()
            runs = content["mythic_plus_weekly_highest_level_runs"]
            # no weekly runs completed
            if runs == []:
                await channel.send(f'{name} has not completed any keystones this week')
            # format weekly runs
            else:
                string = f'**{name}\'s Top 4 Weekly runs\n**'
                for i in range(0,5):
                    if i < len(runs):
                        level = runs[i]["mythic_level"]
                        dungeon = runs[i]["dungeon"]
                        string += f'{level} - {dungeon}\n'
                await channel.send(string)
        # no response: character not found
        else:
            await channel.send(f'Could not find character {name} on Illidan US')

    # invalid command
    else:
        if message.content.startswith('!pumpin'):
            await channel.send('Invalid command, check pins for more info')
                
                                  
    

client.run(os.getenv('DISCORD_TOKEN'))
