from turtle import title
from discord.ext import commands
from discord.ext.tasks import loop
import discord
import asyncio
import openpyxl
from data import *

client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
token = token

game_n = 0


xl4 = openpyxl.load_workbook("log_channel.xlsx")
sheet4 = xl4.active
xl5 = openpyxl.load_workbook("custom_msg.xlsx")
sheet5 = xl5.active


@loop(count=None, seconds=7)
async def presence_loop():
    global game_n
    game_list = [ "실험당", f"{len(client.guilds)}개의 서버에서 활동", f"{len(client.users)}명의 사용자와 함께", "ㅇㅅㅇ명령어 입력!" ]
    await client.change_presence(activity=discord.Game(game_list[game_n]))
    game_n = (game_n + 1) % len(game_list) # 컴퓨터 폭력 멈춰!


@client.event
async def on_ready(): # 실행됨
    print(f'봇 준비 완료\n{client.user}\n=========================')
    await client.change_presence(status=discord.Status.online, activity=discord.Game("봇이 방금 켜졌어요!"))
    await asyncio.sleep(10)
    presence_loop.start()


@client.command(name="콬", alias="ㅋ")
@commands.is_owner()
async def cog_list(ctx):
    txt = ""
    for value in extension.values():
        txt += value + "\n"
    embed = discord.Embed(title="Cog list",description=txt ,colour=discord.Colour.orange())
    await ctx.reply(embed=embed)
    return




@client.command(name="리로드", aliases=[ "ㄹㄹㄷ", "relo", "rl", "기", "ㄱㅣ" ])
@commands.is_owner()
async def reload(ctx, name:str=None):
    print(f"{ctx.author}가 reload 사용")
    if name == None:
        for value in extension.values():
            client.reload_extension(value)
        print("파일 전채 리로드")
        await ctx.reply("전채 리로드 성공!")
    else:
        try:
            print("단일 파일 리로드...")
            client.reload_extension(extension[name])
            print(f"리로드된 파일 : {extension[name]}")
            await ctx.reply(f"{extension[name]} 리로드 성공!")
        except KeyError:
            await ctx.reply("Cog의이름이 잘못되었어요!")
            print("존재하지 않는 Cog")
    print("================================================")
    return


@client.command(name="로드", aliases=[ "ㄹㄷ", "lo", "l", "ㅣ" ])
@commands.is_owner()
async def load(ctx, name:str=None):
    print(f"{ctx.author}가 load 사용")
    if name == None:
        for value in extension.values():
            client.reload_extension(value)
        print("파일 전채 로드")
        await ctx.reply("전채 로드 성공!")
    else:
        try:
            print("단일 파일 로드...")
            client.reload_extension(extension[name])
            print(f"로드된 파일 : {extension[name]}")
            await ctx.reply(f"{extension[name]} 로드 성공!")
        except KeyError:
            await ctx.reply("Cog의이름이 잘못되었어요!")
            print("존재하지 않는 Cog")
    print("================================================")
    return


@client.command(name="언로드", aliases=[ "ㅇㄹㄷ", "unlo", "ul", "ㅕㅣ" ])
@commands.is_owner()
async def unload(ctx, name:str=None):
    print(f"{ctx.author}가 unload 사용")
    if name == None:
        for value in extension.values():
            client.reload_extension(value)
        print("파일 전채 언로드")
        await ctx.reply("전채 언로드 성공!")
    else:
        try:
            print("단일 파일 언로드...")
            client.reload_extension(extension[name])
            print(f"언로드된 파일 : {extension[name]}")
            await ctx.reply(f"{extension[name]} 언로드 성공!")
        except KeyError:
            await ctx.reply("Cog의이름이 잘못되었어요!")
            print("존재하지 않는 Cog")
    print("================================================")
    return


@client.event
async def on_raw_reaction_add(payload):
    if payload.channel_id != 818108117245493248 and payload.channel_id != 817408498408226868:
        return

    if payload.member.bot:
        return

    if payload.emoji.name == "0️⃣":
        try:
            role = discord.utils.get(payload.member.guild.roles, name="사용자")
            await payload.member.add_roles(role)
        except AttributeError:
            pass
    return


@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("값을 정확히 입력해주세요!")
        return
    elif isinstance(error, commands.DisabledCommand):
        await ctx.send("해당 명령어는 지금 사용할 수 없어요!")
        return
    elif isinstance(error, commands.CommandOnCooldown):
        await ctx.send(f"해당 명령어는 `{(round(error.retry_after, 2))}`초 후에 다시 사용하실 수 있어요!")
        return
    elif isinstance(error, commands.CommandNotFound):
        return
    else:
        print("알 수 없는 에러 발생")
        print("===============================================")
        embed = discord.Embed(title="오류 발생!", description=f"알 수 없는 에러\n```{error}```", colour=discord.Colour.red())
        await ctx.send(embed=embed)
        await client.get_user(owner_ids[0]).send(f"일해라ㅏ 주인\n서버: {ctx.guild}\n채널: {ctx.channel}\n메시지: {ctx.message.content}", embed=embed)
        return


if __name__ == "__main__":
    for value in extension.values():
        client.load_extension(value)
        print(f"extension loaded: {value}")
    print("=========================================")

client.run(token)