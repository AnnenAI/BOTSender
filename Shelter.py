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