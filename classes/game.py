import random
from .magic import Spell


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Person:
    def __init__(self, name, hp, mp, atk, df, magic, items):
        self.name = name
        self.maxhp = hp
        self.hp = hp
        self.maxmp = mp
        self.mp = mp
        self.atkl = atk - 10
        self.atkh = atk + 10
        self.df = df
        self.magic = magic
        self.items = items
        self.actions = ['Attack', 'Magic', 'Items']

    def generate_damage(self):
        return random.randrange(self.atkl, self.atkh)

    # def generate_spell_damage(self, i):
    #     mgl = self.magic[i]["dmg"] - 5
    #     mgh = self.magic[i]["dmg"] + 5
    #     return random.randrange(mgl, mgh)

    def take_damage(self, dmg):
        self.hp -= dmg
        if self.hp < 0:
            self.hp = 0
        return self.hp

    def heal(self, dmg):
        self.hp += dmg
        if self.hp > self.maxhp:
            self.hp = self.maxhp

    def get_hp(self):
        return self.hp

    def get_max_hp(self):
        return self.maxhp

    def get_mp(self):
        return self.mp

    def get_max_mp(self):
        return self.maxmp

    def reduce_mp(self, cost):
        self.mp -= cost

    # def get_spell_mp_cost(self, i):
    #     return self.magic[i]["cost"]

    # def get_spell_name(self, i):
    #     return self.magic[i]["name"]

    def choose_action(self):
        i = 1
        print(bcolors.BOLD + "\n\t" + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "\tActions:" + bcolors.ENDC)

        for item in self.actions:
            print("\t\t" + str(i) + ":", item)
            i += 1

    def choose_magic(self):
        i = 1
        print(bcolors.BOLD + "\n\t" + self.name + bcolors.ENDC)
        print(bcolors.OKBLUE + bcolors.BOLD + "\n\tSpells:" + bcolors.ENDC)
        for spell in self.magic:
            print("\t\t" + str(i) + ".", spell.name, "Cost: " +
                  str(spell.cost), "MP: " + str(self.mp))
            i += 1

    def choose_item(self):
        i = 1
        print(bcolors.BOLD + "\n\t" + self.name + bcolors.ENDC)
        print(bcolors.OKGREEN + bcolors.BOLD + "\n\tItems:\n" + bcolors.ENDC)
        for item in self.items:
            print("\t\t" + str(i) + ".", item["item"].name, ":",
                  item["item"].description + " Quantity: " + str(item["quantity"]))
            i += 1

    def choose_target(self, enemies):
        print("\n" + bcolors.FAIL + bcolors.BOLD + "\tTARGETS:" + bcolors.ENDC)
        for i, enemy in enumerate(enemies):
            if enemy.get_hp() != 0:
                print("\t\t" + str(i+1) + ". " + enemy.name)
        choice = int(input("\n\tChoose target: ")) - 1
        return enemies[choice]

    def get_enemy_stats(self):
        hp_bar = ""
        hp_bar_ticks = (self.hp/self.maxhp) * 50

        for i in range(0, 50):
            if i < hp_bar_ticks:
                hp_bar += "█"
            else:
                hp_bar += " "

        max_hp_string = str(self.maxhp) + "/" + str(self.maxhp)
        max_hp_length = len(max_hp_string)
        current_hp_string = str(self.hp) + "/" + str(self.maxhp)

        while(len(current_hp_string) < 11):
            current_hp_string = " " + current_hp_string

        print("                      __________________________________________________")
        print(bcolors.BOLD + self.name + "    " + current_hp_string + " " + bcolors.FAIL +
              "[" + hp_bar + "]    " + bcolors.ENDC)

    def get_stats(self):

        hp_bar = ""
        mp_bar = ""
        hp_bar_ticks = (self.hp/self.maxhp) * 25
        mp_bar_ticks = (self.mp/self.maxmp) * 10

        for i in range(0, 25):
            if i < hp_bar_ticks:
                hp_bar += "█"
            else:
                hp_bar += " "

        for i in range(0, 10):
            if i < mp_bar_ticks:
                mp_bar += "█"
            else:
                mp_bar += " "

        max_hp_string = str(self.maxhp) + "/" + str(self.maxhp)
        max_hp_length = len(max_hp_string)
        current_hp_string = str(self.hp) + "/" + str(self.maxhp)

        while(len(current_hp_string) < 9):
            current_hp_string = " " + current_hp_string

        max_mp_string = str(self.maxmp) + "/" + str(self.maxmp)
        max_mp_length = len(max_mp_string)
        current_mp_string = str(self.mp) + "/" + str(self.maxmp)

        while(len(current_mp_string) < 7):
            current_mp_string = " " + current_mp_string

        print("                     _________________________              __________")
        print(bcolors.BOLD + self.name + "    " + current_hp_string + " " + bcolors.OKGREEN +
              "[" + hp_bar + "]    " + bcolors.ENDC + bcolors.BOLD + bcolors.OKBLUE + current_mp_string + " [" + mp_bar + "]   " + bcolors.ENDC)

    def choose_enemy_spell(self):
        magic_choice = random.randrange(0, len(self.magic))
        spell = self.magic[magic_choice]
        magic_dmg = spell.generate_damage()

        print(spell.name)
        print(magic_dmg)

        pct = self.hp/self.maxhp * 100

        if spell.cost > self.mp or (spell.type == "white" and pct >= 50):
            return self.choose_enemy_spell()
        else:
            return spell, magic_dmg
