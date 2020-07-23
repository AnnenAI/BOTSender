# -*- coding: utf-8 -*-
import random
import copy
import os
import discord
import shutil
import asyncio
import time
from discord.ext import commands


class Player:
    #Функция инициализации игрока
    def __init__(self,user):
        self.name=copy.copy(user.display_name)
        self.link=copy.copy(user)
        self.Cards={}  
        self.ShowedCards={
        'Профессия':'Скрыто',
        'Биографические характеристики':'Скрыто',
        'Здоровье':'Скрыто',
        'Человеческое качество':'Скрыто',
        'Фобия':'Скрыто',
        'Хобби':'Скрыто',
        'Багаж':'Скрыто',
        'Дополнительная информация':'Скрыто',
        'Специальная карточка 1':'Скрыто',
        'Специальная карточка 2':'Скрыто'
        }        
    
    #Функция инициализации начальных карточек
    def get_cards(self,lst):
        self.Cards={
       'Профессия':lst[0],
        'Биографические характеристики':lst[1],
        'Здоровье':lst[2],
        'Человеческое качество':lst[3],
        'Фобия':lst[4],
        'Хобби':lst[5],
        'Багаж':lst[6],
        'Дополнительная информация':lst[7],
        'Специальная карточка 1':lst[8],
        'Специальная карточка 2':lst[9]
    }
    
    #Функция печати карточек игрока    
    def print_cards(self):
        index=1
        result=""
        for key, value in self.Cards.items():
            result+=f"{index}) {key} : {value}\n"
            if index==8: break
            index+=1
        result+=f"\n Специальная карточка 1: {self.Cards.get('Специальная карточка 1')}\n"
        result+=f" Специальная карточка 2: {self.Cards.get('Специальная карточка 2')}\n"
        return result
        
    #Функция печати открытых карточек игрока    
    def print_showed_cards(self):
        index=1
        result=""
        for key, value in self.ShowedCards.items():
            result+=f"{index}) {key} : {value}\n"
            if index==8: break
            index+=1
        result+=f"\n Специальная карточка 1: {self.ShowedCards.get('Специальная карточка 1')}\n"
        result+=f" Специальная карточка 2: {self.ShowedCards.get('Специальная карточка 2')}\n"
        return result
    
    #Функция изменения карточки игрока
    def change_card(self,lst):
        item=lst[0]
        value=lst[1]
        self.Cards[item]=value
        if not self.ShowedCards.get(item)=='Скрыто':
            self.ShowedCards[item]=value
    
    #Функция открытия карточки игрока 
    def show_card(self, key):
        if not self.ShowedCards[key]=='Скрыто':
            return None
        else:
            self.ShowedCards[key]=self.Cards[key]
            return f"{key} : {self.Cards[key]}"

class Shelter:

    #Инициализация убежища
    def __init__(self,users):
        self.load_files()
        self.players=[]
        self.info=[]
        for user in users:
            self.players.append(Player(user))
        self.count_players=len(self.players)
        self.capacity=self.count_players//2
        self.gen_shelter()
        if os.path.exists(self.PATH_GAME):
            shutil.rmtree(self.PATH_GAME,ignore_errors=True)
        os.mkdir(self.PATH_GAME)
        for pl in self.players:
            pl.get_cards(self.gen_cards())
        self.votes={}
    
    #Загрузка всех файлов
    def load_files(self):
        parent_dir = os.path.dirname(os.path.abspath(__file__))
        #local
        #self.PATH_CARDS=parent_dir+"\\Cards\\"
        #self.PATH_GAME=parent_dir+"\\Game\\"
        #self.PATH_CATASTROPHES=parent_dir+"\\Cards\\catastrophes\\"
        #server
        self.PATH_CARDS=parent_dir+"/Cards/"
        self.PATH_GAME=parent_dir+"/Game/"
        self.PATH_CATASTROPHES=parent_dir+"/Cards/catastrophes/"
        with(open(f"{self.PATH_CATASTROPHES}catastrophes.txt",'r',encoding='utf8')) as file_catastrophes:
            self.catastrophes=file_catastrophes.read().split('>')
        with(open(f"{self.PATH_CATASTROPHES}equipment.txt",'r',encoding='utf8')) as file_equipment:
            self.equipment=file_equipment.read().split('\n')
        with(open(f"{self.PATH_CARDS}prof.txt",'r',encoding='utf8')) as file_prof:
            self.prof=file_prof.read().split('\n')
        with(open(f"{self.PATH_CARDS}health.txt",'r',encoding='utf8')) as file_health:
            self.health=file_health.read().split('\n')
        with(open(f"{self.PATH_CARDS}fear.txt",'r',encoding='utf8')) as file_fear:
            self.fear=file_fear.read().split('\n')
        with(open(f"{self.PATH_CARDS}hobby.txt",'r',encoding='utf8')) as file_hobby:
            self.hobby=file_hobby.read().split('\n')
        with(open(f"{self.PATH_CARDS}addons.txt",'r',encoding='utf8')) as file_addons:
            self.addons=file_addons.read().split('\n')
        with(open(f"{self.PATH_CARDS}character.txt",'r',encoding='utf8')) as file_character:
            self.character=file_character.read().split('\n')
        with(open(f"{self.PATH_CARDS}baggage.txt",'r',encoding='utf8')) as file_baggage:
            self.baggage=file_baggage.read().split('\n')
        with(open(f"{self.PATH_CARDS}goldCard.txt",'r',encoding='utf8')) as file_gold_card:
            self.goldCard=file_gold_card.read().split('\n')        
    
    #Функция создания информации о убежище
    def gen_shelter(self):
        self.info=random.choice(self.catastrophes)
        self.info+="\nИнформация о убежище:\n"
        self.info+=f"Вместимость убежища—{self.capacity} чел.\n"
        self.info+=f"﻿Площадь убежища — {random.choice([30,45,50,60,100,80,200,150,180,220,160])} м2\n"
        self.info+=f"Время пребывания — {random.choice([2,5,12,24,6,3,7,8,4,15,18,13,9])} мес.\n"
        self.info+=self.equipment.pop(0)+'\n'
        self.info+=self.equipment.pop(0)+'\n'
        self.info+=self.equipment.pop(random.randint(0, len(self.equipment)-1))+'\n'
        self.info+=self.equipment.pop(random.randint(0, len(self.equipment)-1))+'\n'
        self.info+=self.equipment.pop(random.randint(0, len(self.equipment)-1))+'\n'
        
    def exists(self,name):
        for index in range(0,self.count_players):
            if self.players[index].name==name:
                return index
        return None
    
    #Функция замены карточек между игроками
    def swap(self,player1,indx_pl2,field):
        indx_pl1=self.exists(player1)
        self.players[indx_pl1].Cards[field],self.players[indx_pl2].Cards[field]=self.players[indx_pl2].Cards[field],self.players[indx_pl1].Cards[field]
        if not self.players[indx_pl1].ShowedCards[field]=='Скрыто':
            self.players[indx_pl1].ShowedCards[field]=self.players[indx_pl1].Cards[field]
        if not self.players[indx_pl2].ShowedCards[field]=='Скрыто':
            self.players[indx_pl2].ShowedCards[field]=self.players[indx_pl2].Cards[field]
    
    #Функция смещения карточки на STEPS игроков
    def shift(self,field, steps=1):
        temp=[]
        for pl in self.players:
            temp.append(pl.Cards[field])
        if steps < 0:
            steps = abs(steps)
            for i in range(steps):
                temp.append(temp.pop(0))
        else:
            for i in range(steps):
                temp.insert(0, temp.pop())
        for i in range(0,self.count_players):
            self.players[i].Cards[field]=temp[i]
            if not self.players[i].ShowedCards[field]=='Скрыто':
                self.players[i].ShowedCards[field]=temp[i]
        
    def kick_player(self,name):
        for pl in self.players:
            if pl.name==name:
                self.players.remove(pl)
                self.count_players-=1
    
    #Функция получения БИОГРАФИИ
    def gen_bio(self):
        gender=['Мужчина','Женщина']
        orientations=['Гетеросексуал','Гетеросексуал(Чайлдфри)','Гетеросексуал','Асексуал','Гетеросексуал','Бисексуал','Гетеросексуал','Гомосексуал']
        bioString=f"{random.choice(gender)}, {str(random.randint(16, 65))} лет ({random.choice(orientations)})"
        return bioString

    #Функция получения Профессии
    def gen_prof(self):
        temp=copy.copy(random.choice(self.prof))
        self.prof.remove(temp)
        return temp
    
    #Функция получения Фобии    
    def gen_fear(self):
        temp=copy.copy(random.choice(self.fear))
        self.fear.remove(temp)
        return temp

    #Функция получения Хобби
    def gen_hobby(self):
        temp=copy.copy(random.choice(self.hobby))
        self.hobby.remove(temp)
        return temp

    #Функция получения Здоровья
    def gen_health(self):
        temp=copy.copy(random.choice(self.health))
        self.health.remove(temp)
        return temp

    #Функция получения Дополнительной информации
    def gen_addons(self):
        temp=copy.copy(random.choice(self.addons))
        self.addons.remove(temp)
        return temp
    
    #Функция получения Характера    
    def gen_character(self):
        temp=copy.copy(random.choice(self.character))
        self.character.remove(temp)
        return temp

    #Функция получения Багажа
    def gen_baggage(self):
        temp=copy.copy(random.choice(self.baggage))
        self.baggage.remove(temp)
        return temp

    #Функция получения КАРТОЧКИ СПЕЦИАЛЬНОГО УСЛОВИЯ
    def gen_gold_card(self):
        temp=copy.copy(random.choice(self.goldCard))
        self.goldCard.remove(temp)
        return temp
    
    #Функция генерации всех карточек для игрока
    def gen_cards(self):
        temp=[self.gen_prof(),self.gen_bio(),self.gen_health(),self.gen_character(),self.gen_fear(),self.gen_hobby(),self.gen_baggage(),self.gen_addons(),self.gen_gold_card(),self.gen_gold_card()]
        return temp
    
    #Собрать карточку персонажа    
    def create_txt(self):      
        for index in range(0,self.count_players):
            with(open(f"{self.PATH_GAME}{self.players[index].name}.txt", 'w', encoding='utf8')) as file:
                file.write(self.info)
                file.write("=======================================================================\n\n")
                file.write(self.players[index].print_cards())
                file.write("=======================================================================\n\n")
                for i in range(0,self.count_players):
                    if i==index:
                        file.write(f"Игрок {i+1}:{self.players[i].name} <-- Твои открытые карточки\n")
                    else:
                        file.write(f"Игрок {i+1}:{self.players[i].name}\n")
                    file.write(self.players[i].print_showed_cards())
                    file.write("=======================================================================\n\n")

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