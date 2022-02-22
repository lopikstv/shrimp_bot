import discord
from discord.ext import commands
from data import owner_ids


class event(commands.Cog, name="이벤트가 모인 Cog"):
    def __init__(self, client):
        self.client = client
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        if isinstance(error, commands.CommandOnCooldown):
            await ctx.send(f"해당 명령어는 {(round(error.retry_after, 2))}초 후에 사용할 수 있어요")
            return
        elif isinstance(error, commands.BadArgument) or isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("값을 정확히 입력해주세요!")
            return
        elif isinstance(error, commands.CommandNotFound):
            return
        else:
            embed = discord.Embed(title="오류 발생!", description=f"알 수 없는 에러", colour=discord.Colour.red())
            embed.add_field(value=f"```{error}```")
            await ctx.send(embed=embed)
            await self.client.get_user(owner_ids[0]).send("일해라ㅏ 주인", embed=embed) # 이 부분은 마음대로 바꾸셔도 되요








def setup(client):
    client.add_cog(event(client))