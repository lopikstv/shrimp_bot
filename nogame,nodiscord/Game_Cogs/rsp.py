import asyncio
import discord
from discord.ext import commands
from discord_components import Button, ButtonStyle, DiscordComponents
import openpyxl
from func import search_row, id_generator, now_time
from data import game_playing


xl = openpyxl.load_workbook("user_data.xlsx")
sheet = xl.active
game = "가위바위보"


class rsp(commands.Cog, name="가위바위보"):
    def __init__(self, client):
        self.client = client
    '''
    async def jusik(self, ctx, bs : str = None, company : str = None, num : str = None):
    '''



    @commands.command(name="가위바위보", alias="ㄱㅇㅂㅇㅂ")
    async def rsp(self, ctx, author):
        # 여기 입구컷 부분은 대부분의 게임에 기본으로 들어갈듯
        # 새로운 겜은 만들 때는 기본적인 틀에 맞게 만들어주세요

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
                await message.edit(f"<@!{ctx.author.id}>상대가 초대를 거절했습니다")
                return
        except asyncio.TimeoutError:
            embed.title = "시간 초과로 인해 거절되었습니다"
            await msg.edit(embed=embed)
            await message.edit(f"<@!{ctx.author.id}>시간 초과로 인해 거절되었습니다")
            return
        embed.title = "수락되었습니다"
        await msg.edit(embed=embed)
        await message.edit(f"<@!{ctx.author.id}>상대가 초대를 수락했어요!\n자, 게임을 시작하죠!")
        await asyncio.sleep(3)
        # 여기까지가 모든 게임에 적용될 틀
        
        msg = await ctx.author.send("무엇을 낼지 골라주세요!(10초 안에 누르지 않으면 패배로 간주해요)", components= [
            Button(label="가위"),
            Button(label="바위"),
            Button(label="보"),
        ])
        try:
            res = await ddb.wait_for("button_click", timeout=10, user=ctx.author, message=msg)
            ctx_win = res.component.label
        except asyncio.TimeoutError:
            await msg.edit(f"시간초과로 패배했어요!\n이번 게임의 승자: {author_user.name}")
            await author_user.send(f"축하해요 상대가 시간초과로 인해 패배했어요!\n이번 게임의 승자: {author_user.name}")
            return
        try:
            message = await ctx.author.send("무엇을 낼지 골라주세요!(10초 안에 누르지 않으면 패배로 간주해요)", components= [
                Button(label="가위"),
                Button(label="바위"),
                Button(label="보"),
            ])
            res = await ddb.wait_for("button_click", timeout=10, user=author_user, message=message)
            author_win = res.component.label
        except asyncio.TimeoutError:
            await message.edit(f"시간초과로 패배했어요!\n이번 게임의 승자: {ctx.author.name}")
            await ctx.author.send(f"축하해요 상대가 시간초과로 인해 패배했어요!\n이번 게임의 승자: {ctx.author.name}")
            return
        await msg.edit("양쪽 모두 무엇을 낼지 정했으니 이제 결과를 발표할게요")
        await message.edit("양쪽 모두 무엇을 낼지 정했으니 이제 결과를 발표할게요")
        await asyncio.sleep(5)

        if ctx_win == author_win:
            embed = discord.Embed(title="무승부!", description=f"{ctx.author.name}: {ctx_win}\n{author_user.name}: {author_win}")
            embed.set_footer(text=await now_time)
            await msg.edit(embed=embed)
            await message.edit(embed=embed)
            return
        
        if ctx_win == "가위" and author_win == "보" or ctx_win == "보" and author_win == "바위" or ctx_win == "바위" and author_win == "가위":
            embed = discord.Embed(title=f"{ctx.author.name} 승리!", description=f"{ctx.author.name}: {ctx_win}\n{author_user.name}: {author_win}")
            embed.set_footer(text=await now_time)
            await msg.edit(embed=embed)
            await message.edit(embed=embed)
            return
        else:
            embed = discord.Embed(title=f"{author_user.name} 승리!", description=f"{ctx.author.name}: {ctx_win}\n{author_user.name}: {author_win}")
            embed.set_footer(text=await now_time)
            await msg.edit(embed=embed)
            await message.edit(embed=embed)
            return




def setup(client):
    client.add_cog(rsp(client))