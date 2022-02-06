from discord.ext import commands
from discord.ext.tasks import loop
import discord
import asyncio
from data import *
from supporter import n_generator
import requests
from bs4 import BeautifulSoup


client = commands.Bot(command_prefix=prefix, intents=discord.Intents.all())
token = token

game_n = 0


@loop(count=None, seconds=7)
async def presence_loop():
    global game_n
    game_list = [ "실험당", f"{len(client.guilds)}개의 서버에서 활동", f"{len(client.users)}명의 사용자와 함께", "ㅇㅅㅇ명령어 입력!" ]
    await client.change_presence(activity=discord.Game(game_list[game_n]))
    game_n = (game_n + 1) % len(game_list) # 컴퓨터 폭력 멈춰!


@client.event
async def on_ready(): # 실행됨
    client.owner_ids = owner_ids
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


@client.command(name="명령어", aliases=["도움말", "도움"])
async def help(ctx, options:str=None):
    devoloper = client.get_guild(815092214303948839).get_member(700222381058293793)
    title = ""
    description = ""
    footer = ""
    if options == None:
        devoloper_2 = client.get_guild(815092214303948839).get_member(458528026645495808)
        embed = discord.Embed(title="도움말", description="안녕하세요! 아래의 명령어를 입력해서 새우봇 명령어를 확인하세요!", colour=discord.Colour.orange())
        embed.add_field(name="`ㅇㅅㅇ명령어`", value="명령어들의 종류를 크게 구분해서 보여줄게요.", inline=True)
        embed.add_field(name="`ㅇㅅㅇ명령어 검색엔진`", value="검색 엔진과 관련된 명령어들을 보여줄게요.", inline=True)
        embed.add_field(name="`ㅇㅅㅇ명령어 랜덤`", value="랜덤에 관한 명령어들을 보여줄게요.", inline=True)
        embed.add_field(name="`ㅇㅅㅇ명령어 도박`", value="도박과 관련된 명령어들을 보여줄게요.", inline=True)
        embed.add_field(name="`ㅇㅅㅇ명령어 로또`", value="로또에 관련된 명령어들을 보여줄게요.", inline=True)
        embed.add_field(name="`ㅇㅅㅇ명령어 음악`", value="음악과 관련된 명령어들을 보여줄게요.", inline=True)
        embed.add_field(name="`ㅇㅅㅇ명령어 기타`", value="다른 종류에 해당되지 않는 나머지 명령어들을 보여줄게요.", inline=True)
        embed.set_footer(text=f"개발자 : {devoloper}, {devoloper_2}", icon_url= devoloper.avatar_url)
        await ctx.reply(embed=embed)
        return
    
    elif options == "검색엔진":
        title=f"**명령어->{options}**"
        description = '''
```ㅇㅅㅇ유튜브검색 <검색할 내용>
> 유튜브에 <검색할 내용>을 검색해요
ㅇㅅㅇ네이버검색 <검색할 내용>
> 네이버에 <검색할 내용>을 검색해요```'''
        footer = f"개발자 : {devoloper}"
    
    elif options == "랜덤":
        title= f"**명령어->{options}**"
        description = f'''```
{prefix}동전
> 같은 확률로 앞면 뒷면이 나와요
(극소수의 확률로 동전이 세워질 수도??)
{prefix}가위바위보 <가위, 바위, 보 중 하나 입력>
> 봇과 가위바위보를 해요
{prefix}주사위
> 랜덤으로 1~6까지의 수 중 하나 나와요
(0.0125%의 확률로 주사위가 세워질 수 있어요!)```'''
        footer = f"개발자 : {devoloper}"

    elif options == "도박":
        title = f"**명령어->{options}**"
        description = f'''```
{prefix}사용자등록
> 도박 관련 명령어를 사용하기 전에 꼭 해주세요!
{prefix}돈
> 현재 도박 정보를 보여줘요
{prefix}도박 <배팅할 금액>
> 도박을 해서 성공하면 2배 또는 3배 또는 10배의 돈을 받을 수 있어요!
(극소수의 확률로 100배의 돈도 받을 수 있어요)
{prefix}송금 <유저맨션> <송금할 금액>
> 자신의 돈을 소모해 다른 사람에게 줄 수 있어요
{prefix}돈받기
> 돈이 천원 이하일때만 사용할 수 있어요(파산 방지)
2000~10000까지의 돈을 받을 수 있어요
{prefix}랭킹
> 1~10위까지의 순위를 보여줘요
(도배 방지를 위해 DM으로 보냅니다)```'''
        footer = f"개발자 : {devoloper}"
    
    elif options == "로또":
        title = f"**명령어->{options}**"
        description = f'''```
{prefix}로또구매 <값>
> 로또를 하나 구매해요. <값>에는 1~45까지의 6개의 숫자가 들어오고 중복될 수 없어요
<값>으로 자동을 입력하면 랜덤으로 로또번호를 지정해줘요
{prefix}로또확인
> 자신의 로또번호가 당첨되었는지 확인해보아요
순위에 따라 돈을 받을 수 있어요!
{prefix}보너스번호 <값>
> 보너스 번호를 정해서 로또 당첨 확률을 조금이라도 올려봐요
<값>에는 마찬가지로 1~45까지의 자연수 중 하나를 입력해주세요
```'''
        footer = f"개발자 : {devoloper}"

    elif options == "음악":
        title = f"**명령어->{options}**"
        description = f'''```
{prefix}입장
> 새우봇이 음성채널에 들어오게 해줘요
{prefix}퇴장
> 새우봇을 음성채널에서 나가게 해줘요
{prefix}재생 <유튜브영상url 또는 검색어>
> <유튜브영상url 또는 검색어>를 입력해서 음성채널에서 재생해요!
{prefix}스킵
> 새우봇이 현재 재생하고 있는 노래를 스킵해요!
{prefix}반복재생
> 현재 재생하고 있는 노래를 반복해줘요!```'''
        footer = f"개발자 : {devoloper}"

    elif options == "기타":
        devoloper_2 = client.get_guild(815092214303948839).get_member(458528026645495808)
        title = f"명령어->{options}"
        description = f'''```
{prefix}공지
> 개발자가 새우봇을 사용하는 모두에게 전하는 공지를 보여줘요
{prefix}코로나현황
> 코로나 현황을 알려줘요
{prefix}공식서버
> 새우봇 공식 서버 초대 링크를 보내줘요
{prefix}핑
> 디스코드 지연시간을 알려줘요!```'''
        footer = f"개발자 : {devoloper}, {devoloper_2}"
    
    else:
        await ctx.reply("값을 정확히 입력해주세요!")
        return
    embed = discord.Embed(title=title, description=description)
    embed.set_footer(text=footer)
    embed.colour = discord.Colour.orange()
    await ctx.reply(embed=embed)
    return


@client.command(name="공지")
async def gongzi(ctx):
    await ctx.send('''```
1. 새우봇에 많이 쓰는 기능들만 남겼어요
2. Bot방식으로 바꿨습니다(discord.ext)
```''')


@client.command(name="코로나현황", alias="코로나")
async def corona(ctx):
    url = "https://kosis.kr/covid/covid_index.do"
    res = requests.get(url).text
    soup = BeautifulSoup(res, "html.parser")

    # 확진
    c1 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(1) > strong:nth-child(2)").get_text()  # 총 수
    c2 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(1) > span").get_text().replace(" ", "").replace("\n", "")  # 증가
    c2 = await n_generator(c2)

    # 격리해제
    c3 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(2) > strong:nth-child(2)").get_text()  # 총 수
    c4 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(2) > span").get_text().replace(" ", "").replace("\n", "")  # 증가
    c4 = await n_generator(c4)

    # 사망자
    c5 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(3) > strong:nth-child(2)").get_text()  # 총 수
    c6 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(3) > span").get_text().replace(" ", "").replace("\n", "")  # 증가
    c6 = await n_generator(c6)
    
    # 백신 접종 완료
    c7 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(4) > strong:nth-child(2)").get_text()  # 총 수
    c8 = soup.select_one("#Cont > article.Dashboard > div > p:nth-child(4) > span").get_text().replace(" ", "").replace("\n", "")  # 증가
    c8 = await n_generator(c8)

    embed = discord.Embed(title="코로나 현황", description=f"확진자수: `{c1}` `{c2}`↑\n격리해제: `{c3}` `{c4}`↑\n사망자: `{c5}` `{c6}`↑\n백신접종완료: `{c7}` `{c8}`↑", colour=discord.Colour.green())
    await ctx.reply(embed=embed, mention_author=True)
    return


@client.command(name="공식서버", alias="서버")
async def ofc_server(ctx):
    await ctx.reply("https://discord.gg/BBZKmmAebj", mention_author=True)
    return


@client.command(name="핑")
async def ping(ctx):
    ping = round(client.latency * 1000, 2)
    if ping <= 195:
        status = ":green_circle: 양호함"
    elif ping <= 250:
        status = ":yellow_circle: 보통"
    elif ping <= 300:
        status = ":red_circle: 나쁨"
    else:
        status = ":warning: ??????"
    embed = discord.Embed(title=':ping_pong: 퐁!', description=f'**{ping}**ms\n{status}')
    await ctx.reply(embed=embed, mention_author=True)
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