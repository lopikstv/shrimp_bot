from discord.ext import commands
import discord
import asyncio
import openpyxl
from discord_components import Button, ButtonStyle, DiscordComponents
from random import choice
from func import now_time, id_generator, search_row
from data import game_playing


xl = openpyxl.load_workbook("user_data.xlsx")
sheet = xl.active
game = "동전 던지기"


class coin(commands.Cog, name="동전 던지기"):
    def __init__(self, client):
        self.client = client


    @commands.command(name="동전던지기", aliases=[ "동전", "ㄷㅈ", "ㄷㅈㄷㅈㄱ" ])
    async def coin(self, ctx, author):
        if ctx.author.id in game_playing:
            await ctx.reply("이미 게임을 플레이중이에요\n동시에 여러가지 게임은 할 수 없어요")
            return
        
        author_id = await id_generator(author)
        author_row = await search_row("user_data.xlsx", author_id)
        author_user = self.client.get_user(author_id)


        if author_row == None:
            await ctx.reply(f"{author_user}님은 No game, No discord의 플레이어가 아니에요!")
            return
        
        elif ctx.guild.get_member(author_id) == None: # author이 같은 길드에 없는 경우
            await ctx.reply(f"{author_user.name}님은 같은 서버에 속해있지 않아요")
            return
        
        elif sheet.cell(row=author_row, column=5).value == "0":
            await ctx.reply(f"{author_user.name}님은 지금 모든 게임신청을 받지 않고 있어요")
            return

        elif author_id in game_playing:
            await ctx.reply(f"{author_user.name}님은 이미 게임을 하고 있어요")
            return

        embed = discord.Embed(title="새로운 게임 신청!", description=f"보낸 사람: {ctx.author.name}\n길드: {ctx.guild.name}\n게임: {game}")
        embed.set_footer(text=await now_time)

        components = [
            Button(style=ButtonStyle.green, label="수락"),
            Button(style=ButtonStyle.red, label="거절")
        ]
        msg = await author_user.send(embed=embed, components=components)
        message = await ctx.send(f"{author_user.name}님에게 초대장을 보냈습니다\n15초 안에 수락을 받지 못하면 자동으로 거절됩니다")
        try:
            ddb = DiscordComponents(self.client)
            res = await ddb.wait_for("button_click", timeout=15, user=author_user, message=msg)
            if res.component.label == "거절":
                embed.title = "거절되었습니다"
                await msg.edit(embed=embed)
                await message.edit(content=f"<@!{ctx.author.id}>상대가 초대를 거절했습니다")
                return
        except asyncio.TimeoutError:
            embed.title = "시간 초과로 인해 거절되었습니다"
            await msg.edit(embed=embed)
            await message.edit(content=f"<@!{ctx.author.id}>시간 초과로 인해 거절되었습니다")
            return
        embed.title = "수락되었습니다"
        await msg.edit(embed=embed)
        await message.edit(content=f"<@!{ctx.author.id}>상대가 초대를 수락했어요!\n자, 게임을 시작하죠!")
        await asyncio.sleep(3)
# ==============================================================================================================
        choices = []
        try:
            msg = await ctx.author.send("맞출 면을 선택해주세요(7초안에 선택하지 않으면 선택권은 상대방에게 넘어가요)", components=[
                Button(label="앞면"),
                Button(label="뒷면")
            ])
            message = await author_user.send("상대가 맞출 면을 고르고 있어요....(7초 안에 선택하지 않으면 선택권이 넘어가요)")
            res = await ddb.wait_for("button_click", timeout=7, user=ctx.author, message=msg)
            choices = [ "앞면", "뒷면" ]
            if res.label == "뒷면":
                choices.reverse()
        except asyncio.TimeoutError:
            try:
                await msg.edit(content="시간이 지나서 상대가 선택을 하게 되었어요(7초안에 상대가 선택 안하면 게임이 취소되요)")
                await message.edit(content="상대가 시간안에 선택하지 않았어요\n맞출 면을 선택해주세요(7초가 지나면 게임이 취소되요)", components=[
                    Button(label="앞면"),
                    Button(label="뒷면")
                ])
                res = await ddb.wait_for("button_click", timeout=7, user=author_user, message=message)
                choices = [ "앞면", "뒷면" ]
                if res.label == "앞면":
                    choices.reverse()
            except asyncio.TimeoutError:
                await msg.edit("상대가 시간안에 선택을 안해서 게임이 최소되었어요!")
                await message.edit("시간이 지나서 게임이 취소되었어요!")
                return
        embed = discord.Embed(title="결과발표", description="선택이 모두 끝났어요 그럼 한번 동전을 던져볼게요")
        embed.add_field(value=f"{ctx.author.name}: {choices[0]}, {author_user.name}: {choices[1]}")
        await msg.edit(embed=embed)
        await message.edit(embed=embed)
        await asyncio.sleep(5)
        win = choice([ "앞면", "뒷면" ])
        embed.set_footer(text=await now_time)
        if choices[0] == win:
            winner = ctx.author.name
        else:
            winner = author_user.name
        embed.description = f"{win}이 나왔어요!\n{winner}님의 승리에요!"
        await msg.edit(embed=embed)
        await message.edit(embed=embed)
        return


def setup(client):
    client.add_cog(coin(client))