import asyncio
from discord.ext import commands
import discord
import openpyxl
from discord_components import Button, ButtonStyle, DiscordComponents
from random import choice
from func import end_of_row, search_row, id_generator
from data import game_extension, game_bot, game_name, game_playing



class game(commands.Cog, name="게임 명령어"):
    def __init__(self, client):
        self.client = client
    # 랭겜만 다른 길드와 가능, 일반 겜은 같은 길드에만 있어야 가능
    # column=5값에 있는 수-> 0 == 신청 다 안받음, 1 == 같은 길드에 있으면 받음, 2 == 다 받음
    
    @commands.command(name="게임신청", alias="신청")
    async def game_request(self, ctx, author):
        if ctx.author.id in game_playing:
            await ctx.send("이미 게임을 플레이중이에요")
            return

        author_id = await id_generator(author)
        if author_id == self.client.user.id:
            message = await ctx.send("오, 저한테 도전하는건가요?\n(10초 안에 버튼을 눌러주세요)", components=[
                Button(style=ButtonStyle.green, label="네"),
                Button(style=ButtonStyle.red, label="아니요")
            ])
            try:
                ddb = DiscordComponents(self.client)
                res = await ddb.wait_for("button_click", timeout=10, user=ctx.author)
                await message.delete()
                if res.component.label == "취소":
                    message = await ctx.send("취소되었습니다\n(이 메시지는 5초 후에 사라집니다)")
                    await asyncio.sleep(5)
                    await message.delete()
                    return
            except asyncio.TimeoutError:
                message = await ctx.send("시간 초과로 인해 취소되었습니다\n(이 메시지는 5초 후에 사라집니다)")
                await asyncio.sleep(5)
                await message.delete()
                return
            game = 0
            while True:
                game = choice(game_extension)
                if game_bot[game.split(".")[1]]:
                    break
            game_playing.append(ctx.author.id) # 겜 플레이 하는 사람중에 이사람 추가





def setup(client):
    client.add_cog(game(client))