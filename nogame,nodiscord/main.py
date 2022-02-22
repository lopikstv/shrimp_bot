import asyncio
from discord.ext.tasks import loop
from discord.ext import commands
import discord
import openpyxl
import time
from data import *
from func import now_time, end_of_row



client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
client.remove_command("help")

xl = openpyxl.load_workbook("user_data.xlsx")
sheet = xl.active



status_n = 0

@loop(count=None, seconds=7)
async def presence_loop():
    global status_n
    statuses = [ 
        "개발자와 게임",
        f"{client.command_prefix}도움말 입력!",
        f"{len(client.guilds)}개의 서버에서 게임",
        f"{len(client.users)}명의 유저와 게임",
        f"{client.command_prefix}명령어 입력!",
    ]
    await client.change_presence(activity=discord.Game(statuses[status_n]))
    status_n = (status_n + 1) % len(statuses) # 컴퓨터 폭력 멈춰!


@client.event
async def on_ready():
    nowtime = await now_time()
    print(f"봇이 시작되었습니다\n{client.user}\n[{nowtime}]\n============================")
    client.owner_ids = owner_ids

    for row in range(2, await end_of_row("user_data.xlsx")):
        user_list.append(int(sheet.cell(row=row, column=1).value))

    await client.change_presence(status=discord.Status.online, activity=discord.Game("모두들 오늘도 화이팅하시길!"))
    await asyncio.sleep(12)
    presence_loop.start()


@client.command(name="로드", aliases=[ "ㄹㄷ", "lo", "l", "ㅣ" ])
@commands.is_owner()
async def load(ctx):
    print(f"{ctx.author}가 load 사용")



@client.command(name="언로드", aliases=[ "ㅇㄹㄷ", "unlo", "ul", "ㅕㅣ" ])
@commands.is_owner()
async def unload(ctx):
    print(f"{ctx.author}가 unload 사용")



@client.command(name="리로드", aliases=[ "ㄹㄹㄷ", "relo", "rl", "기", "ㄱㅣ" ])
@commands.is_owner()
async def reload(ctx):
    print(f"{ctx.author}가 reload 사용")
    embed = discord.Embed(title="Game Reloading...", description="Cogs Unloading...")
    embed.set_footer(text=now_time())
    for game in game_extension:
        embed.add_field(name=f"{game}", inline=False)
    msg = await ctx.send(embed=embed)
    start = time.time()
    for cog in game_extension:
        client.unload_extension(cog)
    print("unload 완료")
    embed.description = "Cogs Loading..."
    await msg.edit(embed=embed)
    for cog in game_extension:
        client.load_extension(cog)
    print("load 완료")
    embed.set_footer(text=f"걸린 시간: {time.time() - start}초")
    embed.description = "Cogs Successfully Reloaded!"
    await msg.edit(embed=embed)
    print("reload 완료\n==============================")
    
    
    





if __name__ == "__main__":
    for cog in game_extension:
        client.load_extension(cog)
        print(f"extension loaded: {cog}")


    
    

client.run(bot_token)