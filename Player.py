# -*- coding: utf-8 -*-
import copy

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