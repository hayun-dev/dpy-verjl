# 모듈
import discord, random, asyncio, datetime, os, sys, time, traceback
from captcha.image import ImageCaptcha
from discord.utils import get

# 기본설정
intents = discord.Intents.default()
intents.members = True
client = discord.Client(intents=intents)

# 이모지
s = "<a:a_Success:892034062401798175>"
e = "<a:a_Error:892034061491650560>"
t = "<a:a_Slow:892034061617471618>"
p1 = "<a:667750586938294292:907844141906534460>"
p2 = "<a:playtime1:907844078778081370>"

# 정보/설정
token = "토큰"
vchannel = "인증채널 ID"
log = "로그채널 ID"

# 준비메세지/상태메세지
@client.event
async def on_ready():
    print(f"로그인 완료되었습니다!")
    await client.change_presence(status=discord.Status.online, activity=discord.Game(f"서버이름 | {len(client.users)}명"))

# 맴버 인증안내
@client.event
async def on_member_join(member):
    guild = member.guild
    try:
        await member.send(f"안녕하세요, {member.mention}님! {guild.name}에 오신걸 환영합니다!\n먼저 서버를 이용하시려면, 인증을 하셔야 합니다. <#{vchannel}> 채널에 `!인증`이라고 입력해주세요!\n\n좋은 시간 보내시길 {guild.name}가 기원합니다.")
    except:
        channel = client.get_channel(vchannel)
        await channel.send(f"{member.mention}님! 안녕하세요. 안내 메세지를 전송하는 도중에 실패하여, 메세지로 안내드립니다.\n인증을 하려면, 이채널에(<#{vchannel}>) `!인증`이라고 입력해주시면, 됩니다!")

# 인증 커멘드
@client.event
async def on_message(message):
    if message.content.startswith("!인증"):
        if not message.channel.id == int(vchannel):
            await message.channel.send(f"{message.author.mention}, 이 채널에서는 인증명령어를 사용할수 없습니다!")
            return

        try:
            dmsg = await message.channel.send(f"{message.author.mention}, 인증, DM전송 하는중입니다. 잠시만 기다려주세요!")
            a = ""
            Captcha_img = ImageCaptcha()
            for i in range(6):
                a += str(random.randint(0, 9))

            name = str(message.author. id) + ".png"
            Captcha_img.write(a, name)
            
            embed = discord.Embed(title="인증하기", description=f"{message.author.mention}님, 서버를 이용하시려면, 인증을 해야합니다.\n여기에 아래의 1분이내에, 인증번호를 입력해주세요!", color=0x7289DA, timestamp=message.created_at)
    
            verify = await message.author.send(embed=embed)
            img = await message.author.send(file=discord.File(name))
            await dmsg.edit(content=f"{message.author.mention}, DM을 확인해주세요!")
        

            def check(msg):
                return msg.author == message.author and msg.author == message.author

            try:
                msg = await client.wait_for("message", timeout=60, check=check)

            except:
                await message.channel.purge(limit=1)
                await verify.delete()
                await img.delete()
                embed = discord.Embed(title="시간초과", description="{}님이 시간초과로 인해 인증실패하였습니다.".format(message.author.mention), color=0xFCB801, timestamp=message.created_at)
                await client.get_channel(int(log)).send(embed=embed)
                embed = discord.Embed(title="시간초과", description="{} {}님, 인증에 실패 하였습니다. 다시시도 해주세요!".format(t, message.author.mention), color=0xFCB801, timestamp=message.created_at)
                await message.author.send(embed=embed)

            if msg.content == a:
                await verify.delete()
                await img.delete()

                embed = discord.Embed(title="성공", description="{}님이 인증에 성공하였습니다!".format(message.author.mention), color=0x43B481, timestamp=message.created_at)
                await client.get_channel(int(log)).send(embed=embed)

                channel = client.get_channel(907795611812761620)
                await channel.send(f"안녕하세요, {message.author.mention}님! HYDev에 오신걸 환영합니다!\n\n> ※ <#907790078137487400> 채널에서 약관을 확인해주시길 바랍니다!\n> ※ 질문 및 답변은 <#907846171567988737> 채널에서 역할을 먼저 받아주세요.\n\n좋은 시간 보내시길 HYDev Korea가 기원합니다.\n{p1} **모두 새로 온 유저를 환영해주세요!** {p2}")
                await message.author.add_roles(get(message.author.guild.roles, name="《　　Users　　》"))
                lv = discord.Embed(title="인증성공", description="{} {}님, 인증이 완료 되었습니다.".format(s, message.author.mention), color=0x43B481, timestamp=message.created_at)
                await message.author.send(embed=lv)
            else:
                await verify.delete()
                await img.delete()
                embed = discord.Embed(title="실패", description="{}님이 잘못된 코드로 인해 인증에 실패하였습니다.".format(message.author.mention), color=0xF04947, timestamp=message.created_at)
                await client.get_channel(int(log)).send(embed=embed)    
                embed = discord.Embed(title="인증실패", description="{} {}님, 인증에 실패 하였습니다. 다시시도 해주세요!".format(e, message.author.mention), color=0xF04947, timestamp=message.created_at)
                await message.author.send(embed=embed)

        except:
            await dmsg.edit(content=f"{message.author.mention}, DM을 차단하셨거나, 비활성화 되어있습니다.")

# 로그인
client.run(token)