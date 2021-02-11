import discord
import yahoo_fin.stock_info as si
import yahoo_fin.options as op
import pandas as pd

from discord.ext import commands
from yahoo_fin import options

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


client = commands.Bot(command_prefix = '!')

@client.event
async def on_ready():
    print("bot is ready")


@client.event
async def on_message(message):
    print(message.content)
    if message.content.find("!") != -1:
        content = message.content.strip('!').lower().split()
        print(content)
        print(content[0])

        if content[0] == "day":
            if content[1] == "gain":
                await message.channel.send(si.get_day_gainers().head(10).iloc[:, : 3])
                await message.channel.send("-------------------------------------------")
                await message.channel.send(si.get_day_gainers().head(10).iloc[:, 4: 7])
            elif content[1] == "lose":
                await message.channel.send(si.get_day_losers().head(10).iloc[:, :3])
                await message.channel.send("-------------------------------------------")
                await message.channel.send(si.get_day_losers().head(10).iloc[:, 4:7])
            elif content[1] == "active":
                await message.channel.send(si.get_day_most_active().head(10).iloc[:, :3])
                await message.channel.send("-------------------------------------------")
                await message.channel.send(si.get_day_most_active().head(10).iloc[:, 4:7])

        elif content[0] == "crypto":
            await message.channel.send(si.get_top_crypto().head(10).iloc[:, :3])
            await message.channel.send("-------------------------------------------")
            await message.channel.send(si.get_top_crypto().head(10).iloc[:, 4:5])

        elif content[0] == "help":
            embedVar = discord.Embed(title="List of functioning commands", description="", colour=0x00ff00)
            embedVar.add_field(name="\u200b", value="!tsla\n!day gain\n!day loss", inline=True)
            embedVar.add_field(name="\u200b", value="!calls tlsa 03/19/2021\n!puts tlsa 03/19/2021", inline=True)
            await message.channel.send(embed=embedVar)

        elif content[0] == "calls":
            await message.channel.send(op.get_calls(content[1], content[2]).iloc[:, 2:8])

        elif content[0] == "puts":
            await message.channel.send(op.get_puts(content[1], content[2]).iloc[:, 2:8])

        else:
            temp = si.get_quote_table(content[0])
            change = round(temp["Quote Price"] - temp["Previous Close"], 2)
            percentage = round(change/temp["Previous Close"]*100,2)

            displayQuote = str(round(temp["Quote Price"],2))
            displayChange = str(change)
            displayPercentage = str(percentage)
            displayTicker = content[0].upper()
            displayClose = str(round(temp["Previous Close"],2))

            dayRange = temp["Day's Range"].replace('-', '').split()

            dayLow = dayRange[0]
            dayHigh = dayRange[1]

            open = temp["Open"]
            close = temp["Previous Close"]

            volume = str(round(temp["Volume"] / 1000000, 2))
            volume = volume + "M"

            avgVolume = str(round(temp["Avg. Volume"] / 1000000, 2))
            avgVolume = avgVolume + "M"

            bid = temp["Bid"]
            ask = temp["Ask"]

            if change >= 0:
                rgb = 0x00ff00
                displayChange = "+" + displayChange
                displayPercentage = "+" + displayPercentage
            else:
                rgb = 0xff0000

            embedVar = discord.Embed(
                title=f"${displayTicker}\n${displayQuote} {displayChange} ({displayPercentage}%)",
                description="",
                colour=rgb)
            embedVar.add_field(name="\u200b", value=f"High: {dayHigh}\nLow: {dayLow}\n\nAsk: {ask}\nBid: {bid}", inline=True)
            embedVar.add_field(name="\u200b", value=f"Open: {open}\nPrev.: {close}", inline=True)
            embedVar.add_field(name="\u200b", value=f"Volume: {volume}\nAvg. Vol.: {avgVolume}", inline=True)

            await message.channel.send(embed=embedVar)



client.run('TOKEN')

