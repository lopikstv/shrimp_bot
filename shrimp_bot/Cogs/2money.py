from discord.ext import commands
import discord
import asyncio
from discord_components import *
from supporter import *
from random import uniform, randint

'''
다 만든 명령어: 사용자등록, 도박, 돈, 돈받기
'''

xl2 = openpyxl.load_workbook("user_money.xlsx")
sheet2 = xl2.active

class money(commands.Cog, name="도박 명령어"):
    def __init__(self, client):
        self.client = client

    @commands.command(name="사용자등록", aliases=[ "등록", "가입" ])
    async def join(self, ctx):
        row = await search_row("user_money.xlsx", ctx.author.id)
        if row != None:
            await ctx.reply(f"<@!{ctx.author,id}>님은 이미 등록되어 있어요!")
        else:
            try:
                embed = discord.Embed(title="새우봇 도박 관련 기능\n이용 약관 동의", description='''동의 버튼을 누르면 앞으로 도박 관련 기능을 사용할 수 있습니다.
                그리고 도박 기능을 사용할 때 사용자 식별을 위하여 
                사용자 고유 ID를 수집 및 저장하게 됩니다. 동의 하시겠습니까?
                (10초 안에 버튼을 눌러주세요)''', colour=discord.Colour.orange())
                msg = await ctx.reply(embed=embed, 
                components=[
                    Button(style=ButtonStyle.green, label="동의"),
                    Button(style=ButtonStyle.red, label="취소")
                ])

                try:
                    ddb = DiscordComponents(client)
                    res = await ddb.wait_for("button_click", timeout=10, user=ctx.author)
                    await msg.delete()
                    if res.component.label == "취소":
                        msg = await ctx.send("취소되었습니다\n(이 메시지는 5초 후에 사라집니다)")
                        await asyncio.sleep(5)
                        await msg.delete()
                        return
                except asyncio.TimeoutError:
                    await msg.delete()
                    msg = await ctx.send("시간 초과로 인해 취소되었습니다\n(이 메시지는 5초 후에 사라집니다)")
                    await asyncio.sleep(5)
                    await msg.delete()
                    return
                row = await end_of_row("user_money.xlsx")
                sheet2.cell(row=row, column=1).value = f"{ctx.author.id}"
                sheet2.cell(row=row, column=2).value = "100000"
                sheet2.cell(row=row, column=5).value = "43.00"
                await ctx.reply(f'사용자 리스트에 <@!{ctx.author.id}>님이 추가되었어요!\n이제부터 도박 관련 기능을 사용할 수 있어요!')
                xl2.save("user_money.xlsx")
            except PermissionError:
                await ctx.reply("개발자가 사용자 정보 파일을 열고 있어요!\n잠시 기다린후 다시해 주세요")
        return
    

    @commands.command(name="돈")
    async def money(self, ctx):
        row = await search_row("user_money.xlsx", ctx.author.id)
        if row == None:
            await ctx.reply("도박 관련 기능 명령어를 사용하려면\n`ㅇㅅㅇ사용자등록` 명령어로 등록을\n먼저 해주세요!")
            return
        user_money = sheet2.cell(row=row, column=2).value
        user_luck = sheet2.cell(row=row, column=5).value
        user_lotto = sheet2.cell(row=row, column=6).value
        bonus_num = sheet2.cell(row=row, column=7).value
        if user_lotto == None or user_lotto == "":
            user_lotto = "로또 미보유"
        if bonus_num == None or bonus_num == "":
            bonus_num = "미보유"
        embed = discord.Embed(title=f"{ctx.author}님의 돈", description=f"보유한 돈: **`{user_money}`**\n나의 로또번호: `{user_lotto}`\n보너스 번호: `{bonus_num}`\n도박확률: `{user_luck}%`", colour=discord.Colour.orange())
        await ctx.reply(embed=embed)
        return
    

    @commands.command(name="도박", alias="ㄷㅂ")
    async def batting(self, ctx, money):
        row = await search_row("user_money.xlsx", ctx.author.id)
        if row == None:
            await ctx.reply("도박 관련 기능 명령어를 사용하려면\n`ㅇㅅㅇ사용자등록` 명령어로 등록을\n먼저 해주세요!")
            return
        try:
            batting_money = int(money)
        except:
            await ctx.reply("값을 정확히 입력해주세요!")
            return
        if batting_money < 500:
            await ctx.reply("적어도 500원 이상 배팅을 해야 해요!")
            return
        user_money = int(sheet2.cell(row=row, column=2).value)
        if user_money < batting_money:
            await ctx.reply("가지고 있는 돈보다 많은 수를 입력했어요...")
            return
        random_value = round(uniform(0, 100), 2)
        user_luck = round(float(sheet2.cell(row=row, column=5).value), 2)
        if random_value > user_luck:
            random_luck_up = round(uniform(1,4), 2)
            user_luck += random_luck_up
            user_money -= batting_money
            sheet2.cell(row=row, column=5).value = f"{user_luck}"
            sheet2.cell(row=row, column=2).value = f"{user_money}"
            await ctx.reply(f"저런...돈을 잃었어요......\n`- {batting_money}`")
        else:
            sheet2.cell(row=row, column=5).value = "43.00"
            random_up = randint(1, 101)
            if random_up == 101:
                user_money += batting_money * 99
                sheet2.cell(row=row, column=2).value = f"{user_money}"
                await ctx.reply(f"1/100의 확률로 100배에 성공 했어요!\n`+ {batting_money * 99}`")
            elif random_up <= 50:
                user_money += batting_money
                sheet2.cell(row=row, column=2).value = f"{user_money}"
                await ctx.reply(f"오! 두배로 성공 했어요!\n`+ {batting_money}`")
            elif random_up <= 80:
                user_money += batting_money * 2
                sheet2.cell(row=row, column=2).value = f"{user_money}"
                await ctx.reply(f"와! 3배의 보상을 지급 해드릴게요!\n`+ {batting_money * 2}`")
            else:
                user_money += batting_money * 4
                sheet2.cell(row=row, column=2).value = f"{user_money}"
                await ctx.reply(f"축하해요! 5배로 성공 했어요!\n`+ {batting_money * 4}`")
            xl2.save("user_money.xlsx")
            return
    

    @commands.command(name="돈받기", alias="돈받기")
    async def get_money(self, ctx):
        row = await search_row("user_money.xlsx", ctx.author.id)
        if row == None:
            await ctx.reply("도박 관련 기능 명령어를 사용하려면\n`ㅇㅅㅇ사용자등록` 명령어로 등록을\n먼저 해주세요!")
            return
        user_money = int(sheet2.cell(row=row, column=2).value)
        if user_money > 1000:
            await ctx.reply("돈이 1000원 이하여야 받을 수 있어요!(파산 방지)")
        else:
            random_money = randint(2, 10) * 1000
            sheet2.cell(row=row, column=2).value = f"{user_money + random_money}"
            await ctx.reply(f"돈을 받았어요!\n`+{random_money}`")
        return
    

    @commands.command(name="송금")
    async def give_money(self, ctx, author, money):
        row = await search_row("user_money.xlsx", ctx.author.id)
        if row == None:
            await ctx.reply("도박 관련 기능 명령어를 사용하려면\n`ㅇㅅㅇ사용자등록` 명령어로 등록을\n먼저 해주세요!")
            return
        try:
            target_user = await id_generator(author)
            money = int(money)
        except:
            await ctx.reply("값을 정확히 입력해주세요!\nㅇㅅㅇ송금 <유저맨션> 돈")
            return

        if target_user == ctx.author.id:
            await ctx.reply("자신에게는 송금할 수 없어요!")
            return
        target_user_row = await search_row("user_money.xlsx", target_user)
        if target_user_row == None:
            await ctx.reply("송금할 사람은 새우봇 도박 시스템에 등록되어 있지 않아요!")
            return
        user_money = int(sheet2.cell(row=row, column=2).value)
        if user_money < money:
            await ctx.reply("가지고 있는 돈보다 많은 수량을 입력했어요...")
            return
        if money < 10000:
            await ctx.reply("10000원 이상 입력해주세요!")
            return
        target_user_money = int(sheet2.cell(row=target_user_row, column=2).value)
        user_money -= money
        target_user_money += money
        sheet2.cell(row=row, column=2).value = f"{user_money}"
        sheet2.cell(row=target_user_row, column=2).value = f"{target_user_money}"
        await ctx.reply(f"송금이 완료되었어요!\n`-{money}`")
        return
    

    @commands.command(name="랭킹", aliases=[ "순위", "ㅅㅇ", "ㄹㅋ" ])
    async def ranking(self, ctx):
        end = await end_of_row("user_money.xlsx")
        row = 2
        ranking = [ "없음\n0", "없음\n0", "없음\n0", "없음\n0", "없음\n0", "없음\n0", "없음\n0", "없음\n0", "없음\n0", "없음\n0"]
        while row != end:
            user = self.client.get_user(int(sheet2.cell(row=row, column=1).value))
            user_money = int(sheet2.cell(row=row, column=2).value)

            if user_money < int(ranking[9].split("\n")[1]) or user == None:
                row += 1
                continue # 입구컷

            for n in range(0, 10):
                if user_money > int(ranking[n].split("\n")[1]):
                    for x in range(0, 10 - n):
                        ranking[9 - x] = ranking[8 - x]
                    ranking[n] = f"{user}\n{user_money}"
                    break
            row += 1
        
        await ctx.author.send(f'''```1위: {ranking[0]}원
2위: {cal(ranking[1])}
3위: {cal(ranking[2])}
4위: {cal(ranking[3])}
5위: {cal(ranking[4])}
6위: {cal(ranking[5])}
7위: {cal(ranking[6])}
8위: {cal(ranking[7])}
9위: {cal(ranking[8])}
10위: {cal(ranking[9])}```''')
        await ctx.reply("DM을 확인해주세요!")
        return




def setup(client):
    client.add_cog(money(client))