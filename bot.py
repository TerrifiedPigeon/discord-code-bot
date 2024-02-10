import discord
from discord.ext import commands
targetBotID = 0
yourBotID = 0
intents = discord.Intents.default()
intents.message_content = True
# replace 'g!' and 'g' with your own prefixes
bot = commands.Bot(command_prefix=commands.when_mentioned_or("g!", "g"), case_insensetive=True, help_command=None, intents=intents)


@bot.event
async def on_ready():
    print('Bot is ready.')
    # replace 'g!help' with your own bot status
    activity = discord.Game(name="g!help", type=0)
    await bot.change_presence(status=discord.Status.online, activity=activity)


@bot.command()
async def help(ctx):
    # replace the text bellow with your own messages 
    embedvar = discord.Embed(title="Help command title", description="Help command description",color=0x283593)
    await ctx.send(embed=embedvar)


@bot.command(aliases=['c'])
async def codes(ctx):
    # replace the 'instructions' with your own message
    introMsg = 'instructions'
    intro = await ctx.send(introMsg)

    def check(msg):
        if msg.channel == ctx.channel:
            if msg.author.id == targetBotID:
                for embed in msg.embeds:
                # following section works for tofu bot as of 2024
                    title = (embed.author.name).split("'")
                    x = len(title) - 1
                    titles_list = ['s Card Collection', 's Hexes', 's Gear', 's Spells', 's Auras', 's FastFuse', 's Rings']
                    if title[x] in titles_list:
                        return True
            elif msg.author.id == yourBotID and msg.id != intro.id:
                return True
    def check1(before, after):
        if after.channel.id == ctx.channel.id:
            if after.author.id == targetBotID:
                for embed in after.embeds:
                    title2 = embed.author.name
                    return title1 == title2
    
    msg = await bot.wait_for('message', check=check, timeout=30.0)
    if not (msg.author.id == yourBotID and msg.content == introMsg):
        for embed in msg.embeds:
            titleA = (embed.author.name).split("'")
            x = len(titleA) - 1
            title1 = embed.author.name
            card_codes1, card_codes2, full_list = [], [], []
            desc = "\n".join(("".join((embed.description).split('`'))).split(' · ')).split('\n')
            embed = msg.embeds[0]
            rowNum = 0
            extra = None
            if titleA[x] == 's Card Collection':
                offset = 2
                perRow = 9
            if titleA[x] == 's Gear':
                offset = 1
                perRow = 9
            if titleA[x] == 's Spells':
                offset = 1
                perRow = 3
            if titleA[x] == 's Hexes':
                offset = 1
                perRow = 6
            if titleA[x] == 's Auras':
                offset = 1
                perRow = 4
            if titleA[x] == 's Rings':
                desc2 = ("".join((embed.description).split('`'))).split('> · ')[1:]
                desc = []
                for item in desc2:
                    desc.append(item.split(" · ")[0])
                    x += 1
                    offset = 0
                    perRow = 1
                extra = "Rings"
            if titleA[x] == 's FastFuse':
                desc = ("\n".join(("".join(((embed.description).split('\n\n`')[1]).split('`'))).split(' · '))).split('\n')
                offset = 2
                perRow = 8
                extra = "FastFuse"
            x = (len(desc) + 1)/perRow - 1
            while rowNum < x:
                full_list.append(desc[offset + (rowNum * perRow)])
                card_codes1.append(desc[offset + (rowNum * perRow)])
                rowNum = rowNum + 1
            msg1 = await ctx.send(" , ".join(card_codes1))
            while True:
                msg2 = await bot.wait_for('message_edit', check=check1, timeout=15.0)
                channel1 = await bot.fetch_channel(msg2[1].channel.id)
                msg4 = await channel1.fetch_message(msg2[1].id)
                if msg4.id == msg.id:
                    for embed in msg4.embeds:
                        desc = "\n".join(("".join((embed.description).split('`'))).split(' · ')).split('\n')
                        if extra == 'Rings':
                            desc2 = ("".join((embed.description).split('`'))).split('> · ')[1:]
                            desc = []
                            for item in desc2:
                                desc.append(item.split(" · ")[0])
                                x += 1
                                offset = 0
                                perRow = 1
                        if extra == 'FastFuse':
                            desc = ("\n".join(("".join(((embed.description).split('\n\n`')[1]).split('`'))).split(' · '))).split('\n')
                        x = len(desc) + 1
                        x = x / perRow - 1
                        rowNum = 0
                        while rowNum < x:
                            if desc[offset + (rowNum * perRow)] not in full_list:
                                full_list.append(desc[offset + (rowNum * perRow)])
                                if len(card_codes1) < 50:
                                    card_codes1.append(desc[offset + (rowNum * perRow)])
                                else:
                                    card_codes2.append(desc[offset + (rowNum * perRow)])
                            rowNum = rowNum + 1
                        card_codes1a = " , ".join(card_codes1)
                        if card_codes1a != msg1.content:
                            msg1 = await msg1.edit(content=card_codes1a)
                        if len(card_codes2) > 0:
                            card_codes2a = " , ".join(card_codes2)
                            msg1 = await ctx.send(card_codes2a)
                            card_codes1 = card_codes2
                            card_codes2 = []
    else:
        # replace the 'cancel message' with your own message
        await intro.reply("cancel message")
# replace token with your bots token
bot.run(token='token')
