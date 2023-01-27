import discord
from discord.ext import commands
import random
import re
import os
from openpyxl import load_workbook


bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())

emo_yin = "<:yin:1064122799091884082>"
emo_yang = "<:yang:1064122752866463775>"
emo_yy = "<:yin_yang:1064348918672015380>"
emo_yin_m = "<:yin_m:1065391100132605953>"
emo_yang_m = "<:yang_m:1065391125176799343>"


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
        result = skill_check(int(num_dice), int(num_sides), modifiers, desc)
        await ctx.send(f"{ctx.author.mention}"+"\n"+result)
    except ValueError:
        await ctx.send("Error")


@bot.command()
async def a(ctx, *args):
    args = " ".join(args)
    input_list = re.split(r'[+ ]', args)
    num_dice, num_sides = input_list[0].split("d")
    modifiers = [int(i)
                 for i in input_list[1:] if i.lstrip("+-").isdigit()]
    desc = [i for i in input_list[1:] if (
        not i.lstrip("+-").isdigit()) and i != '']
    weapon_name, weapon_damage = choosen_weapon(desc)
    result = attack_check(int(num_dice), int(num_sides),
                          modifiers, weapon_name, int(weapon_damage))
    await ctx.send(f"{ctx.author.mention}"+"\n"+result)


def roll_dice2(num_dice, num_sides):
    rolls = []
    for i in range(num_dice):
        rolls.append(random.randint(0, num_sides-1))
    yin = rolls[0]
    yang = rolls[1]
    return yin, yang


def dice_checker(yin, yang):
    if yin == yang:
        if yin == 0:
            result = "Crit Fail"
            dice_result = 0
            return result, yin
        else:
            result = "Crit Success"
            dice_result = yin
            return result, dice_result
    else:
        if yin > yang:
            result = 0
            dice_result = yin - yang
            return result, dice_result
        else:
            result = 1
            dice_result = yang - yin
            return result, dice_result


def skill_check(num_dice, num_sides, modifiers, description):
    desc = " ".join(description)
    yin, yang = roll_dice2(num_dice, num_sides)
    checker, dice_result = dice_checker(yin, yang)
    sum_mod = sum(modifiers)
    total = dice_result + sum_mod
    if checker == "Crit Fail":
        result = f"**{desc}: \n{yin} {emo_yin} {yang} {emo_yang} Critical Fail!\nResult: 0 {emo_yy}**"
        return result
    elif checker == "Crit Success":
        if sum_mod < 0:
            result = f"**{desc}: \n{yin} {emo_yin} {yang} {emo_yang} Critical Success!\nResult: {yin} {emo_yy} {sum_mod}**"
            return result
        else:
            result = f"**{desc}: \n{yin} {emo_yin} {yang} {emo_yang} Critical Success!\nResult: {yin} {emo_yy} + {sum_mod} = {total}**"
            return result
    else:
        if checker == 0:
            result = f"**{desc}: **\n{yin} {emo_yin} {yang} {emo_yang}\n**Result: ** {dice_result} {emo_yin_m} + {sum_mod} = {total}"
            return result
        else:
            result = f"**{desc}: **\n{yin} {emo_yin} {yang} {emo_yang}\n**Result: ** {dice_result} {emo_yang_m} + {sum_mod} = {total}"
            return result


def choosen_weapon(weapon):
    weapon_names, weapon_descs, weapon_damages, weapon_resiliences, weapon_skilsl, weapon_prices = load_weapon()
    weapon_name = weapon[0]
    if weapon_name in weapon_names:
        # Do something with the weapon
        index = weapon_names.index(weapon_name)
        alt_name = weapon_name.split("_")
        if len(alt_name) == 1:
            # case where input is "bang"
            name_join = " ".join(alt_name)
            weapon_name = name_join
            print(f"{weapon_name} {weapon_damages[index]}")
            return weapon_name, weapon_damages[index]
        else:
            # case where input is "bang_xiao"
            alt_name = alt_name[::-1]
            name_join = " ".join(alt_name)
            weapon_name = name_join
            print(f"{weapon_name} {weapon_damages[index]}")
            return weapon_name, weapon_damages[index]
    else:
        print("Invalid weapon")
        return None, None


def damage_check(num_dice, num_sides, modifiers, weapon_name, weapon_damage):
    damage_yin, damage_yang = roll_dice2(num_dice, num_sides)
    damage_checker, damage_dice_result = dice_checker(damage_yin, damage_yang)
    if (damage_checker == (("Crit Fail") or ("Crit Success"))):
        total_damage = modifiers + weapon_damage + damage_dice_result
        return f"**Damage:**\n{damage_yin} {emo_yin} {damage_yang} {emo_yang}\n**Result: **{damage_dice_result} {emo_yy} + {modifiers}(Metal) + {weapon_damage}({weapon_name.title()}) = {total_damage}"
    else:
        if (damage_checker == 1):
            total_damage = modifiers + weapon_damage + damage_dice_result
            return f"**Damage:**\n{damage_yin} {emo_yin} {damage_yang} {emo_yang}\n**Result: **{damage_dice_result} {emo_yang_m} + {modifiers}(Metal) + {weapon_damage}({weapon_name.title()}) = {total_damage}"
        else:
            total_damage = modifiers + weapon_damage
            return f"**Damage:**\n{damage_yin} {emo_yin} {damage_yang} {emo_yang}\n**Result: **{modifiers}(Metal) + {weapon_damage}({weapon_name.title()}) = {total_damage}"


def attack_check(num_dice, num_sides, modifiers, weapon_name, weapon_damage):
    attack_yin, attack_yang = roll_dice2(num_dice, num_sides)
    attack_checker, attack_dice_result = dice_checker(attack_yin, attack_yang)
    attack_mod = sum(modifiers)
    damage_mod = modifiers[0]
    total = attack_dice_result + attack_mod
    damage_result = damage_check(
        int(num_dice), int(num_sides), int(damage_mod), weapon_name, int(weapon_damage))

    if attack_checker == "Crit Fail":
        result = f"**Attack with {weapon_name.title()}! \n{attack_yin} {emo_yin} {attack_yang} {emo_yang} Critical Fail!\nResult: 0 {emo_yy}**"
        return result
    elif attack_checker == "Crit Success":
        if attack_mod < 0:
            result = f"**Attack with {weapon_name.title()}! \n{attack_yin} {emo_yin} {attack_yang} {emo_yang} Critical Success!\nResult: {attack_yin} {emo_yy} {attack_mod} = {total}**\n\n{damage_result}"
            return result
        else:
            result = f"**Attack with {weapon_name.title()}! \n{attack_yin} {emo_yin} {attack_yang} {emo_yang} Critical Success!\nResult: {attack_yin} {emo_yy} + {attack_mod} = {total}**\n\n{damage_result}"
            return result
    else:
        if attack_checker == 0:
            result = f"Attack with {weapon_name.title()}! \n{attack_yin} {emo_yin} {attack_yang} {emo_yang}\n**Result: ** {attack_dice_result} {emo_yin_m} + {attack_mod} = {total}\n\n{damage_result}"
            return result
        else:
            result = f"Attack with {weapon_name.title()}! \n{attack_yin} {emo_yin} {attack_yang} {emo_yang}\n**Result: ** {attack_dice_result} {emo_yang_m} + {attack_mod} = {total}\n\n{damage_result}"
            return result


def load_weapon():
    file = os.path.join(os.path.dirname(__file__), 'weapons.xlsx')
    workbook = load_workbook(file)

    sheet_name = 'weapons'

    if sheet_name in workbook.sheetnames:
        sheet = workbook[sheet_name]
        weapon_name = []
        weapon_desc = []
        weapon_damage = []
        weapon_resilience = []
        weapon_skill = []
        weapon_price = []

        # Print the data starting from the B3
        row_index = 0
        for row in sheet.iter_rows(values_only=True):
            if row_index >= 2:
                # print(row)
                weapon_name.append(row[0])
                weapon_desc.append(row[1])
                weapon_damage.append(row[2])
                weapon_resilience.append(row[3])
                weapon_skill.append(row[4])
                weapon_price.append(row[5])
            row_index += 1
        return weapon_name, weapon_desc, weapon_damage, weapon_resilience, weapon_skill, weapon_price
    else:
        return None, None, None, None, None, None


bot.run(TOKEN)
