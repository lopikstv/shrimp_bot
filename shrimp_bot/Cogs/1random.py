from discord.ext import commands
from random import randint


# random함수 응용 명령어

class random(commands.Cog, name="랜덤 명령어"):
    def __init__(self, client):
        self.client = client
    
    @commands.command(name="동전")
    async def coin(self, ctx):
    # 동전 던지기
        random_coin = randint(1, 61)
        if random_coin == 61:
            await ctx.reply("소수의 확률로 동전이 세워졌어요!!!!")
        elif random_coin <= 30:
            await ctx.reply("앞면이 나왔어요!", mention_author=False)
        else:
            await ctx.reply("뒷면이 나왔어요!", mention_author=False)
        return


    @commands.command(name="주사위")
    # 주사위
    async def dice(self, ctx):
        random_number = randint(1, 6)
        uni = randint(1, 8000)
        if uni == 7777:
            await ctx.reply("0.0125%의 확률을 뚫고 주사위를 세웠어요!!!")
        else:
            await ctx.reply("주사위에서 나온 수: " + str(random_number), mention_author=False)
        return


    @commands.command(name="랜덤수", aliases=[ "랜덤", "수", "ㄹㄷㅅ" ])
    async def randomn(self, ctx, n1, n2):
        
        if n1 > n2:
            n1, n2 = n2, n1
        
        random_number = randint(n1, n2)
        await ctx.send(f"{n1}부터 {n2}까지의 수중 나온 수:\n{random_number}")
        return





def setup(client):
    client.add_cog(random(client))