import discord
from discord.ext import commands
import random
import re


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())
TOKEN = "Bot Token"


@bot.event
async def on_ready():
    print("Qin Dice Bot is ready!")


@bot.command()
async def s(ctx, *args):
    try:
        args = " ".join(args)
        input_list = re.split(r'[+ ]', args)
        num_dice, num_sides = input_list[0].split("d")
        modifiers = [int(i)
                     for i in input_list[1:] if i.lstrip("+-").isdigit()]
        desc = [i for i in input_list[1:] if (
            not i.lstrip("+-").isdigit()) and i != '']
        result = roll_dice(int(num_dice), int(num_sides), modifiers, desc)
        await ctx.send(f"{ctx.author.mention}"+"\n"+result)
    except ValueError:
        await ctx.send("Error")


def roll_dice(num_dice, num_sides, modifiers, description):
    rolls = []
    desc = " ".join(description)
    for i in range(num_dice):
        rolls.append(random.randint(0, num_sides-1))
    rolls.sort()
    if rolls[0] == rolls[1]:
        if rolls[0] == 0:
            result = "("+str(rolls[1])+", "+str(rolls[0])+")"
            return ("**"+result+"\n"+"Critical Fail\nhi gained: 5"+"**")
        else:
            result = "("+str(rolls[1])+", "+str(rolls[0])+")"
            return ("**"+result+"\n"+"Critical Success\nChi gained: " + str(rolls[0])+"**")

    else:
        dice_rolls = "("+str(rolls[0])+", "+str(rolls[1])+")"
        dice_result = rolls[1] - rolls[0]
        sum_mod = sum(modifiers)
        result = dice_result + sum_mod
        if sum_mod < 0:
            final_result = ("**"+desc+": "+"**"+str(dice_result) +
                            str(sum_mod)+" = "+str(result))
        else:
            final_result = ("**"+desc+": "+"**"+str(dice_result)+"+" +
                            str(sum_mod)+" = "+str(result))
        return str(dice_rolls+"\n"+final_result)


bot.run(TOKEN)
