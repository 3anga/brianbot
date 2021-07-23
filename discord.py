import discord, asyncio, logging, configuration

client = discord.Client()

@client.event
async def on_ready():
    print(f'{client.user} подключен к Дискорду')

@client.event
async def on_member_join(member):
    await member.create_dm()
    await member.dm_channel.send(
        f'Привет {member.name}. Провери #верификация!'
    )

client.run(configuration.DISCORD_TOKEN)