from classes.game import person, bcolors
from classes.magic import spell
from classes.inventory import item
import random


# create black magic
fire = spell('Fire', 10, 100, 'black')
thunder = spell('Thunder', 10, 100, 'black')
blizzard = spell('Blizzard', 10, 100, 'black')
meteor = spell('Meteor', 20, 200, 'black')
quake = spell('Quake', 14, 140, 'black')


# create white magic
cure = spell('cure', 12, 120, 'white')
cura = spell('cura', 18, 200, 'white')


# create items
potion = item('Potion', 'potion', 'heals 50 hp', 50)
hipotion = item('Hi-Potion', 'potion', 'heals 100 hp', 100)
superpotion = item('Super-Potion', 'potion', 'heals 500 hp', 500)
elixer = item('Elixer', 'elixer', 'Fully restores HP/MP of one party member', 9999)
hielixer = item('Mega-Elixer', 'elxir', 'Fully restores HP/MP of a party', 9999)

granade = item('Granande', 'attack', 'deals 500 damage', 500)

# player variables
player_spells = [fire, thunder, blizzard, meteor, cure, cura]
player_items = [{'item': potion, 'quantity': 15}, {'item': hipotion, 'quantity': 5}, 
                {'item': superpotion, 'quantity': 5}, {'item': elixer, 'quantity': 5},
                {'item': hielixer, 'quantity': 5}, {'item': granade, 'quantity': 5}]

# enemy variables
enemy_spells = [fire, meteor, cure]

# People
player1 = person('Eena:', 460, 65, 60, 34, player_spells, player_items)
player2 = person('Mina:', 460, 65, 60, 34, player_spells, player_items)
player3 = person('Dika:', 460, 65, 60, 34, player_spells, player_items)

enemy1 = person('Thanos', 1200, 65, 45, 25, enemy_spells,  [])
enemy2 = person('Ultron  ', 800, 40, 30, 15, enemy_spells, [])
enemy3 = person('Ronan ', 1000, 45, 40, 20, enemy_spells, [])

players = [player1, player2, player3]
enemies = [enemy1, enemy2, enemy3]

running = True
i = 0

print(bcolors.FAIL + bcolors.BOLD + 'An enemy attacks!' + bcolors.ENDC)

while running:
    print("============================================================================================================")
    print('\n')
    for player in players:
        player.get_stats()
    print('\n')
    for enemy in enemies:
        enemy.get_enemy_stats()
    print('\n')

    for player in players:
        player.choose_action()
        choice = input('    Choose action:')
        index = int(choice) - 1

        if index == 0:
            dmg = player.generate_damage()
            enemy = player.choose_target(enemies)

            enemies[enemy].take_damage(dmg)
            print('You attacked ' + enemies[enemy].name + ' for', dmg, 'points of damage.')

            if enemies[enemy].get_hp() == 0:
                print(bcolors.OKGREEN + enemies[enemy].name + ' has died' + bcolors.ENDC)
                del enemies[enemy]

        elif index == 1:
            player.choose_magic()
            magic_choice = int(input('    Choose Magic: ')) - 1

            spell = player.magic[magic_choice]
            magic_dmg = spell.generate_damage()

            '''
            # old code(before magic.py was introduced into action)
            magic_dmg = player.generate_spell_damage(magic_choice)
            spell = player.get_spell_name(magic_choice)
            cost = player.get_spell_mp_cost(magic_choice)
            '''
            
            current_mp = player.get_mp()

            if spell.cost > current_mp:
                print(bcolors.FAIL + "\nNOT ENOUGH MP\n" + bcolors.ENDC)
                continue

            if magic_choice == -1:
                continue

            player.reduce_mp(spell.cost)

            if spell.type == 'white':
                player.heal(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name + ' heals for ' + str(magic_dmg) + ' points' + bcolors.ENDC)

            elif spell.type == 'black':
                enemy = player.choose_target(enemies)

                enemies[enemy].take_damage(magic_dmg)
                print(bcolors.OKBLUE + '\n' + spell.name + " deals", str(magic_dmg), 'points of damage to '+ enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.OKGREEN + enemies[enemy].name + ' has died' + bcolors.ENDC)
                    del enemies[enemy]

        elif index == 2:
            player.choose_item()
            item_choice = int(input('    Choose item: ')) - 1

            if item_choice == -1:
                continue
            
            item = player.items[item_choice]['item']

            if player.items[item_choice]['quantity'] == 0:
                print(bcolors.FAIL + '\n' + 'None left.....' + bcolors.ENDC)

            player.items[item_choice]['quantity'] -= 1

            if item.type == 'potion':
                player.heal(item.prop)
                print(bcolors.OKGREEN + '\n' + item.name + ' heals for', str(item.prop), 'HP', bcolors.ENDC)

            elif item.type == 'elixer':

                if item.name == 'Mega-Elixer':
                    for i in players:
                        i.hp = i.maxhp
                        i.mp = i.maxmp
                else:
                    player.hp = player.maxhp
                    player.mp = player.maxmp
                print(bcolors.OKGREEN + '\n' + item.name + ' fully restored HP/MP' + bcolors.ENDC)

            elif item.type == 'attack':
                enemy = player.choose_target(enemies)
                enemies[enemy].take_damage(item.prop)
                print(bcolors.FAIL + '\n' + item.name + ' deals', str(item.prop), 'points of damage to '+ enemies[enemy].name + bcolors.ENDC)

                if enemies[enemy].get_hp() == 0:
                    print(bcolors.OKGREEN + enemies[enemy].name + ' has died' + bcolors.ENDC)
                    del enemies[enemy]

# checks if battle is over
    defeated_enemies = 0
    defeated_players = 0
    for enemy in enemies:
        if enemy.get_hp() == 0:
            defeated_enemies += 1

    for player in players:
        if player.get_hp() == 0:
            defeated_players += 1
# player won
    if defeated_enemies == 2:
        print(bcolors.OKGREEN + 'You Win!' + bcolors.ENDC)
        running = False
# enemy won
    elif defeated_players == 2:
        print(bcolors.FAIL + 'You Lost!' + bcolors.ENDC)
        running = False

# enemy attacks
    for enemy in enemies:
        enemy_choice = random.randrange(0, 2)

        if enemy_choice == 0:
            # choose attack
            target = random.randrange(0, 3)
            enemy_dmg = enemy.generate_damage()

            players[target].take_damage(enemy_dmg)
            print(bcolors.FAIL + '\n' + enemy.name + ' attacked '+ players[target].name.replace(':', ' ') + 'for', enemy_dmg, 'points of damage.' + bcolors.ENDC)

        elif enemy_choice == 1:
            spell, magic_dmg = enemy.choose_enemy_spell()
            enemy.reduce_mp(spell.cost)

            if spell.type == 'white':
                enemy.heal(magic_dmg)
                print(bcolors.FAIL + '\n' + spell.name + ' heals'+ enemy.name + 'for ' + str(magic_dmg) + ' points' + bcolors.ENDC)

            elif spell.type == 'black':
                target = random.randrange(0, 3)

                players[target].take_damage(magic_dmg)
                print(bcolors.FAIL + '\n' + enemy.name + "'s "+ spell.name + " deals", str(magic_dmg), 'points of damage to '+ players[target].name + bcolors.ENDC)

                if players[target].get_hp() == 0:
                    print(bcolors.FAIL + players[target].name + ' has died' + bcolors.ENDC)
                    del players[player]
           # print(bcolors.FAIL + enemy.name + 'chose ' + spell.name + ' damage is ' + str(magic_dmg) + bcolors.ENDC)

    print('------------------------------------------------------------------------------------------------------------')
    print(bcolors.WARNING + 'Next turn' + bcolors.ENDC)

    