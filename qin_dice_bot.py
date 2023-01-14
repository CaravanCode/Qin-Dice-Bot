import discord
import random

client = discord.Client()


@client.event
async def on_message(message):
    if message.content.startswith("!s"):
        num_dice, num_sides = map(int, message.content[3:].split("d"))
        result = roll_dice(num_dice, num_sides)
        await message.channel.send(result)


def roll_dice(num_dice, num_sides):
    rolls = []
    for i in range(num_dice):
        rolls.append(random.randint(1, num_sides))
    rolls.sort()
    if rolls[0] == rolls[1]:
        if rolls[0] == 0:
            result = "("+str(rolls[1])+", "+str(rolls[0])+")"
            return result+"\n"+"Critical Fail"
        else:
            result = "("+str(rolls[1])+", "+str(rolls[0])+")"
            return result+"\n"+"Critical Success\nChi gained: " + str(rolls[0])

    else:
        result = "("+str(rolls[1])+", "+str(rolls[0])+")"
        return result+"\n"+rolls[1] - rolls[0]


client.run(
    "MTA2MzY0OTI3MzcwNDYxMTk3MA.GA61xl.18tN2Rah9JyAztDk4wbWkjZ90jHQ7-9-VkMWBk")
