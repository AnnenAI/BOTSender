# -*- coding: utf-8 -*-
import discord
import asyncio
import time
from discord.ext import commands
from Shelter import Shelter

#link to add https://discordapp.com/oauth2/authorize?&client_id=732540975670493214&scope=bot&permissions=8
TOKEN = 'NzMyNTQwOTc1NjcwNDkzMjE0.XxljYA.hwRORb2zNgaAbaIuquVRQYpMqSc'
bot = commands.Bot(command_prefix='!')
bot.remove_command("help")

#Команда БОТА - Информация о командах бота
@bot.command(pass_context=True)
async def help(ctx):
    user = ctx.message.author
    try:    
        await ctx.message.delete()
    finally:
        fields=""
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name='Команды бота')
        fields+=f"**!game** --> Начать игру\n"
        fields+=f"**!card** --> Поменять карточку\n"
        fields+=f"**!cards** --> Поменять карточку всем игрокам\n"
        fields+=f"**!vote** --> Голосование за изгнание\n"
        fields+=f"**!txt** --> Получить обновленный TXT файл\n"
        fields+=f"**!show** --> Открыть карточку\n"
        fields+=f"**!swap** --> Обменятся карточкой с игроком\n"
        fields+=f"**!shift** --> Перемешать карточки игроков \n"
        fields+=f"**!player** --> Получить открытые карточки игрока\n"
        fields+=f"**!players** --> Получить список игроков в игре\n"
        embed.description=fields
        await user.send(embed=embed)
    
def switch_change(x):
   return {
        '1': f"Профессия:{session.gen_prof()}",
        '2': f"Биографические характеристики:{session.gen_bio()}",
        '3': f"Здоровье:{session.gen_health()}",
        '4': f"Человеческое качество:{session.gen_character()}",
        '5': f"Фобия:{session.gen_fear()}",
        '6': f"Хобби:{session.gen_hobby()}",
        '7': f"Багаж:{session.gen_baggage()}",
        '8': f"Дополнительная информация:{session.gen_addons()}"
    }.get(x)
    
#Команда БОТА -  замены карточки с игроком
@bot.command(pass_context=True)
async def swap(ctx,field=None,pl=None):
    try:
        user=ctx.message.author
        await ctx.message.delete()
        if session.exists(user.display_name) is None:
            raise NameError('Игрок покинул игру').with_traceback(traceback_obj)
        fields=""
        embed = discord.Embed(color=discord.Colour(0x332842))
        if field is None or int(field)>8 or int(field)<1 or pl is None or int(pl)<1 or int(pl)>len(session.players):
            embed.set_author(name='Команда чтобы поменяться карточкой с игроком')
            fields+=f"**!swap 1 Номер игрока** --> Профессия\n"
            fields+=f"**!swap 2 Номер игрока** --> Биографические характеристики\n"
            fields+=f"**!swap 3 Номер игрока** --> Здоровье\n"
            fields+=f"**!swap 4 Номер игрока** --> Человеческое качество\n"
            fields+=f"**!swap 5 Номер игрока** --> Фобия\n"
            fields+=f"**!swap 6 Номер игрока** --> Хобби\n"
            fields+=f"**!swap 7 Номер игрока** --> Багаж\n"
            fields+=f"**!swap 8 Номер игрока** --> Дополнительная информация\n"
            embed.description=fields
            await user.send(embed=embed)
        else:
            user1=session.players[session.exists(user.display_name)]
            field=switch_show(field)
            session.swap(user1.name,int(pl)-1,field)
            embed.set_author(name=f"{field} : {user1.Cards[field]}")
            embed.description=f"Измененная карточка для игрока: {user1.name}"
            await user1.link.send(embed=embed)
            user2=session.players[int(pl)-1]
            embed.set_author(name=f"{field}:{user2.Cards[field]}")
            embed.description=f"Измененная карточка для игрока: {user2.name}"
            await user2.link.send(embed=embed)
            embed.set_author(name=f"Игрок {user1.name} обменялся с игроком {user2.name}")
            embed.description=f"Карточка : {field}"
            await ctx.send(embed=embed)
    except NameError:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Вы покинули игру и не можете использовать эту команду")
        await user.send(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Эту команду вы можете использовать только в чате канала")
        await user.send(embed=embed)

#Команда БОТА - передача карточек игрокам
@bot.command(pass_context=True)
async def shift(ctx,field=None):
    try:
        user=ctx.message.author
        await ctx.message.delete()
        if session.exists(user.display_name) is None:
            raise NameError('Игрок покинул игру').with_traceback(traceback_obj)
        fields=""
        embed = discord.Embed(color=discord.Colour(0x223d4a))
        if (field is None or int(field)>8 or int(field)<1):
            embed.set_author(name='Команда чтобы поменяться картами по часовой стрелке')
            fields+=f"**!shift 1** --> Профессия\n"
            fields+=f"**!shift 2** --> Биографические характеристики\n"
            fields+=f"**!shift 3** --> Здоровье\n"
            fields+=f"**!shift 4** --> Человеческое качество\n"
            fields+=f"**!shift 5** --> Фобия\n"
            fields+=f"**!shift 6** --> Хобби\n"
            fields+=f"**!shift 7** --> Багаж\n"
            fields+=f"**!shift 8** --> Дополнительная информация\n"
            embed.description=fields
            await user.send(embed=embed)
        else:
            field=switch_show(field)
            session.shift(field)
            for pl in session.players:
                embed.set_author(name=f"{field} : {pl.Cards[field]}")
                embed.description=f"Измененная карточка для игрока: {pl.name}"
                await pl.link.send(embed=embed)
            embed.set_author(name=f"Игрок {user.display_name} перемешал карточки игроков ")
            embed.description=f"Карточка: {field}"
            await ctx.send(embed=embed)
    except NameError:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Вы покинули игру и не можете использовать эту команду")
        await user.send(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Эту команду вы можете использовать только в чате канала")
        await user.send(embed=embed)

#Команда БОТА -  замены карточки для себя   
@bot.command(pass_context=True)
async def card(ctx,arg=None):
    try:
        user = ctx.message.author
        await ctx.message.delete()
        if session.exists(user.display_name) is None:
            raise NameError('Игрок покинул игру').with_traceback(traceback_obj)
        await ctx.message.delete()
        fields=""
        embed = discord.Embed(color=discord.Colour.orange())
        if (arg is None or int(arg)>8 or int(arg)<1):
            embed.set_author(name='Команда чтобы сменить карточку')
            fields+=f"**!card 1** --> Профессия\n"
            fields+=f"**!card 2** --> Биографические характеристики\n"
            fields+=f"**!card 3** --> Здоровье\n"
            fields+=f"**!card 4** --> Человеческое качество\n"
            fields+=f"**!card 5** --> Фобия\n"
            fields+=f"**!card 6** --> Хобби\n"
            fields+=f"**!card 7** --> Багаж\n"
            fields+=f"**!card 8** --> Дополнительная информация\n"
            embed.description=fields
            await user.send(embed=embed)
        else:
            changed_card=switch_change(arg)
            field=list(changed_card.split(':'))[0]
            member=session.exists(user.display_name)
            session.players[member].change_card(list(changed_card.split(':')))
            embed.set_author(name=changed_card)
            embed.description=f"Измененная карточка для игрока: {session.players[member].name}"
            await user.send(embed=embed)
            embed.set_author(name=f"Игрок {user.display_name} поменял себе карточку")
            embed.description=f"Карточка : {field}"
            await ctx.send(embed=embed)
    except NameError:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Вы покинули игру и не можете использовать эту команду")
        await user.send(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Эту команду вы можете использовать только в чате канала")
        await user.send(embed=embed)

#Команда БОТА - замены карточки для всех игроков
@bot.command(pass_context=True)
async def cards(ctx,arg=None):
    try: 
        user=ctx.message.author
        await ctx.message.delete()
        if session.exists(user.display_name) is None:
            raise NameError('Игрок покинул игру').with_traceback(traceback_obj)
        fields=""
        if (arg is None or int(arg)>8 or int(arg)<1):
            embed = discord.Embed(color=discord.Colour.orange())
            embed.set_author(name='Команда чтобы сменить всем карточку')
            fields+=f"**!cards 1** --> Профессия\n"
            fields+=f"**!cards 2** --> Биографические характеристики\n"
            fields+=f"**!cards 3** --> Здоровье\n"
            fields+=f"**!cards 4** --> Человеческое качество\n"
            fields+=f"**!cards 5** --> Фобия\n"
            fields+=f"**!cards 6** --> Хобби\n"
            fields+=f"**!cards 7** --> Багаж\n"
            fields+=f"**!cards 8** --> Дополнительная информация\n"
            embed.description=fields
            await user.send(embed=embed)
        else:
            for member in session.players:
                user=member.link
                changed_card=switch_change(arg)
                field=list(changed_card.split(':'))[0]
                member.change_card(list(changed_card.split(':')))
                embed = discord.Embed(color=discord.Colour.purple())
                embed.set_author(name=changed_card)
                embed.description=f"Измененная карточка для игрока: {member.name}"
                await user.send(embed=embed)
            embed.set_author(name=f"Игрок {sender.display_name} поменял всем карточку")
            embed.description=f"Карточка : {field}"
            await ctx.send(embed=embed)
    except NameError:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Вы покинули игру и не можете использовать эту команду")
        await user.send(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Эту команду вы можете использовать только в чате канала")
        await user.send(embed=embed)
    

#Команда БОТА - отправки TXT своего персонажа
@bot.command(pass_context=True)
async def txt(ctx):
    try:
        await ctx.message.delete()
    finally:
        session.create_txt()
        embed = discord.Embed(color=discord.Colour.red())
        user = ctx.message.author
        await user.send(file=discord.File(f"{session.PATH_GAME}{user.display_name}.txt"))
        for usr in session.players:
            if usr.name==user.display_name:
                embed.set_author(name=f"Игрок {usr.name}")
                embed.description=usr.print_cards()
                await user.send(embed=embed)        

#Команда БОТА -  отображения открытых карточек любого игрока
@bot.command(pass_context=True)
async def player(ctx, index=None,arg=None):
    fields=""
    try:
        user=ctx.message.author
        await ctx.message.delete()
    except discord.errors.NotFound:
        pass
    finally:
        embed = discord.Embed(color=discord.Colour(0xc2828e))
        if index is None or int(index)>len(session.players) or int(index)<1:
            embed.set_author(name='Получить иноформацию о игроке')
            for i in range(0,len(session.players)):
                fields+=f"{session.players[i].name} --> **!player {i+1}**\n"
                embed.description=fields
        else:
            i=int(index)-1
            embed.description=session.players[i].print_showed_cards()
            embed.set_author(name=f"Игрок  {session.players[i].name}")
        if not arg is None:
            await ctx.send(embed=embed)
        else:
            await user.send(embed=embed)

#Команда БОТА -  отображения игроков в игре
@bot.command(pass_context=True)
async def players(ctx):
    user = ctx.message.author
    try:
        await ctx.message.delete()
    finally:
        members=""
        embed = discord.Embed(color=discord.Colour(0xbec282))
        for i in range(0,len(session.players)):
            members+=f"**{i+1}. {session.players[i].name}**\n"
        embed.description=members
        embed.set_author(name="Игроки которые участвуют в игре")
        await user.send(embed=embed)
        

def switch_show(x):
    return {
        '1': "Профессия",
        '2': "Биографические характеристики",
        '3': "Здоровье",
        '4': "Человеческое качество",
        '5': "Фобия",
        '6': "Хобби",
        '7': "Багаж",
        '8': "Дополнительная информация",
        '9': "Специальная карточка 1",
        '10': "Специальная карточка 2"
    }.get(x)

#Команда БОТА -  открытия карточки игрока
@bot.command(pass_context=True)
async def show(ctx, arg=None):
    user = ctx.message.author
    try:
        await ctx.message.delete()
        if session.exists(user.display_name) is None:
            raise NameError('PlayerNotFound').with_traceback(traceback_obj)
        fields=""
        embed = discord.Embed(color=discord.Colour.purple())
        if (arg is None or int(arg)>10 or int(arg)<1):
            embed.set_author(name='Какую карточку хотите открыть?')
            fields+=f"**!show 1** --> Профессия\n"
            fields+=f"**!show 2** --> Биографические характеристики\n"
            fields+=f"**!show 3** --> Здоровье\n"
            fields+=f"**!show 4** --> Человеческое качество\n"
            fields+=f"**!show 5** --> Фобия\n"
            fields+=f"**!show 6** --> Хобби\n"
            fields+=f"**!show 7** --> Багаж\n"
            fields+=f"**!show 8** --> Дополнительная информация\n"
            fields+=f"**!show 9** --> Специальная карточка 1\n"
            fields+=f"**!show 10** --> Специальная карточка 2\n"
            embed.description=fields
            await user.send(embed=embed)
        else:
            for pl in session.players:
                if pl.name==user.display_name:
                    res=pl.show_card(switch_show(arg))
            if res is None:
                embed.set_author(name=switch_show(arg))
                embed.description="Эта карточка уже открыта"
                await user.send(embed=embed)
            else:
                if int(arg)==9 or int(arg)==10:
                    if not res.find('убежище,')==-1 or not res.find('погреб')==-1:
                        session.info+='\n'+list(res.split(':'))[1]
                    if not res.find('меньше на 1 место')==-1:
                        session.info=session.info.replace(f"Вместимость убежища—{session.capacity}",f"Вместимость убежища—{session.capacity-1}")
                        session.capacity-=1
                    if not res.find('больше на 1 место')==-1:
                        session.info=session.info.replace(f"Вместимость убежища—{session.capacity}",f"Вместимость убежища—{session.capacity+1}")
                        session.capacity+=1
                embed.set_author(name=res)
                embed.description=f"Игрок **{user.display_name}** открыл карточку"
                await ctx.send(embed=embed)
    except NameError:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Вы покинули игру и не можете использовать эту команду")
        await user.send(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Эту команду вы можете использовать только в чате канала")
        await user.send(embed=embed)


def add_vote(user,voter):
    if len(session.votes)>0:
            for vote in list(session.votes.keys()):
                if voter in session.votes[vote]:
                    if len(session.votes[vote])==1:
                        del session.votes[vote]
                    else:
                        session.votes[vote].remove(voter)
    if not user==None:
        if user in session.votes.keys():
            session.votes[user].append(voter)
        else:
            session.votes[user]=[voter]

#Команда БОТА -  получения информации о убежище
@bot.command(pass_context=True)
async def info(ctx,author=None):
    sender=ctx.message.author
    try:
        if author is None:
            await ctx.message.delete()
        else:
            sender=author
    finally:
        embed = discord.Embed(color=discord.Colour.green())
        embed.set_author(name="Информация о убежище")
        embed.description=session.info
        await sender.send(embed=embed)
        
#Команда БОТА -  голосования за изгнание игрока
@bot.command(pass_context=True)
async def vote(ctx,arg=None):
    sender=ctx.message.author
    try:
        await ctx.message.delete()
        if session.exists(sender.display_name) is  None:
            raise NameError('Игрок покинул игру').with_traceback(traceback_obj)
        embed = discord.Embed(color=discord.Colour.green())
        fields=""
        embed.set_author(name='Голосование за изгнание')
        if (arg=='accept'):
            bedolaga=list(session.votes.keys())[0]
            await ctx.send(f"{bedolaga} покидает нас, пока пока")
            session.kick_player(bedolaga)
            session.votes.clear()
            if session.capacity==session.count_players:
                await game(ctx, 'end')
        elif (arg=='cancel'):
            session.votes.clear()
            await ctx.send("Голосование отменено")
        elif (arg is None or int(arg)>len(session.players)):
            for member in range(0,len(session.players)):
                user=session.players[member].name
                fields+=f"{user} --> **!vote {member+1}**\n"
                embed.description=fields
            await sender.send(embed=embed)
        else:
            if int(arg)==0:
                user=None
            else:
                user=session.players[int(arg)-1].name
            voter= sender.display_name
            add_vote(user,voter)
            session.votes=dict(sorted(session.votes.items(), key=lambda i: -len(i[1])))
            for vote in session.votes.keys():
                fields+=f"**{len(session.votes[vote])}** за изгнание **{vote}**, тебя не любят **: {', '.join(session.votes[vote])}**\n"
            embed.description=fields
            await ctx.send(embed=embed)
    except NameError:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Вы покинули игру и не можете использовать эту команду")
        await sender.send(embed=embed)
    except discord.errors.Forbidden:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Эту команду вы можете использовать только в чате канала")
        await sender.send(embed=embed)

#Начало игры COMMAND==> !start
@bot.command(pass_context=True)
async def game(ctx, end=None):
    sender=ctx.message.author
    try:
        await ctx.message.delete()
    except discord.errors.Forbidden:
        embed = discord.Embed(color=discord.Colour.red())
        embed.set_author(name="Эту команду вы можете использовать только в чате канала")
        await sender.send(embed=embed)
    except discord.errors.NotFound:
        pass
    finally:
        if end is None:
            global session
            listUsers=[]
            voice_channel_list = ctx.guild.voice_channels
            for voice_channels in voice_channel_list:
                if len(voice_channels.members) != 0:
                    if voice_channels.name == "Основной":
                        for member in voice_channels.members:
                            listUsers.append(member)
            index=1
            listUsers=sorted(listUsers, key=lambda x: x.display_name)
            if len(listUsers)<1:
                embed = discord.Embed(color=discord.Colour.red())
                embed.set_author(name="Для начала игры необходимо как минимум 6 игроков\n")
                await ctx.send(embed=embed)
            else:
                session=Shelter(listUsers)
                await ctx.send("Игра началась, всем отправлены карточки")
                session.create_txt()
                embed = discord.Embed(color=discord.Colour.blue())
                for member in session.players:
                    user=member.link
                    await user.send("=============Новая игра=============")
                    await user.send(file=discord.File(f"{session.PATH_GAME}{user.display_name}.txt"))
                    await info(ctx,user)
                    embed.set_author(name=f"Игрок  {member.name}")
                    embed.description=member.print_cards()
                    await user.send(embed=embed)
        else:
            embed = discord.Embed(color=discord.Colour.red())
            embed.set_author(name="Игра закончилась, спасибо за игру! В убежище попали:\n")
            await ctx.send(embed=embed)
            for i in range(1,len(session.players)+1):
                await player(ctx,i,"end")
            del session

def run_client(client, *args, **kwargs):
    loop = asyncio.get_event_loop()
    while True:
        try:
            loop.run_until_complete(client.start(*args, **kwargs))
        except Exception as e:
            print("Error", e)  # or use proper logging
            print("Waiting until restart")
        time.sleep(1800)

run_client(bot,TOKEN)