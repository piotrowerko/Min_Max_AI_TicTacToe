import random

#  print the board:
def print_grid(grid):
    print(9 * "-")
    for i in range(0, 9, 3):
        print("|", *grid[i:i+3], "|")      # OR: print("|", " ".join(grid[i:i+3]), "|")
    print(9 * "-")


# return the list with empy spots:
def list_empty_spots(grid):
    indeksy_pustych_w_stringu = []
    for i in range(0, len(grid), 1):
        if grid[i] == '_':
            indeksy_pustych_w_stringu += [i]
    return indeksy_pustych_w_stringu

def state_of_the_game(sum_string, grid_list):
    empty_count = 0
    for char in sum_string:
        if char == "_":
            empty_count += 1
    # Is there a 3 in a row or column or diagonal ?
    true_false1_XXX = [True if "".join(grid_list[i]) == 'XXX' else False for i in range(3)]
    true_false1_OOO = [True if "".join(grid_list[i]) == 'OOO' else False for i in range(3)]
    true_false2_XXX = [True if grid_list[0][j]+grid_list[1][j]+grid_list[2][j] == 'XXX' else False for j in range(3)]
    true_false2_OOO = [True if grid_list[0][j]+grid_list[1][j]+grid_list[2][j] == 'OOO' else False for j in range(3)]
    true_false3_XXX = [True if grid_list[0][0]+grid_list[1][1]+grid_list[2][2] == 'XXX' else False]
    true_false3_OOO = [True if grid_list[0][0]+grid_list[1][1]+grid_list[2][2] == 'OOO' else False]
    true_false4_XXX = [True if grid_list[0][2]+grid_list[1][1]+grid_list[2][0] == 'XXX' else False]
    true_false4_OOO = [True if grid_list[0][2]+grid_list[1][1]+grid_list[2][0] == 'OOO' else False]
    X_wins = true_false1_XXX+true_false2_XXX+true_false3_XXX+true_false4_XXX
    O_wins = true_false1_OOO+true_false2_OOO+true_false3_OOO+true_false4_OOO
    X_wins_warning = any(X_wins)
    O_wins_warning = any(O_wins)
    Any_one_wins_warning = any(X_wins + O_wins)
    # State of the game assessment - information return:
    if empty_count >= 0 and Any_one_wins_warning:
        if X_wins_warning:
            cc = "X wins"
            score = 10
        if O_wins_warning:
            cc = "O wins"
            score = -10
    elif empty_count == 0 and Any_one_wins_warning == False:
        cc = "Draw"
        score = 0
    elif empty_count > 0 and Any_one_wins_warning == False:
        cc = "notfinished"
        score = None
    return cc, score


#  input function for hard computer move (min max brutal algorihtm):
def min_max_pio(grid, sign):
    i = 0
    local_list = []
    for zz in list_empty_spots(grid):
        i += 1
        sum_string_temp = grid[:zz] + grid[zz].replace("_", sign) + grid[zz + 1:]
        grid_list_temp = [[sum_string_temp[j + 3 * i] for j in range(3)] for i in range(3)]
        sss = state_of_the_game(sum_string_temp, grid_list_temp)[1]
        sss_ = state_of_the_game(sum_string_temp, grid_list_temp)[0]
        if sss == None: #  nie znaleziono lokalnego końca gry
            tester = True
            if sign == "X":
                sign2 = "O"
            elif sign == "O":
                sign2 = "X"
            local_list.append(min_max_pio(sum_string_temp, sign2)[0])
        else:
            tester = False
        if i == len(list_empty_spots(grid)): #  jestem na końcu danego poziomu (na końcu pętli)
            if tester == False: # #  znaleziono lokalny koniec gry na końcu pętli dzięki temu że pogrzebałem niżej
                local_list.append(sss)
            if sign == "O":
                return  [min(local_list), local_list]
            elif sign == "X":
                return  [max(local_list), local_list]
        if tester == False and i < len(list_empty_spots(grid)): #znaleziono lokalny koniec koniec gry ale nie na końcu pętli
            local_list.append(sss)


def user_move(grid, sign):
    grid_list = [[grid[j + 3 * i] for j in range(3)] for i in range(3)]
    while True:
        user_move = input("Enter the coordinates:").strip()
        if user_move[0].isnumeric() == False or user_move[2].isnumeric() == False:
            print("You should enter numbers!")
            continue
        X_user = int(user_move[0])
        Y_user = int(user_move[2])
        if X_user > 3 or X_user < 1 or Y_user > 3 or Y_user < 1:
            print("Coordinates should be from 1 to 3!")
            continue
        if grid_list[abs(Y_user-3)][X_user-1] == 'X' or grid_list[abs(Y_user-3)][X_user-1] == 'O':
            print("This cell is occupied! Choose another one!")
            continue
        else:
            break
    grid_list[abs(Y_user-3)][X_user-1] = sign
    sum_string = "".join(grid_list[0]) + "".join(grid_list[1]) + "".join(grid_list[2])
    print_grid(sum_string.replace("_", " "))  # Printing new grid
    cc1 = state_of_the_game(sum_string, grid_list)[0]
    if cc1 != "notfinished":
        print(cc1) # Printing state of the game
        return False
    else: return sum_string


def easy_comp_move(grid, sign):
    while True:
        if '_' in grid:
            while True:
                zz = random.randint(0, 8)
                if grid[zz] == "_":
                    sum_string = grid[:zz] + grid[zz].replace("_", sign) + grid[zz + 1:]
                    break
            grid_list_NEW = [[sum_string[j + 3 * i] for j in range(3)] for i in range(3)]
            print('Making move level "easy"')
            print_grid(sum_string.replace("_", " "))  # Printing newer grid
            cc2 = state_of_the_game(sum_string, grid_list_NEW)[0]
            if cc2 != "notfinished":
                print(cc2) # Printing state of the game
                return False
            else: return sum_string
        break


def medium_comp_move(grid, sign):
    stoper = False
    if '_' in grid:
        #  ruch po wygraną (o ile możliwa)
        for i in range(1000):
            zz = random.randint(0, 8)
            if grid[zz] == "_":
                sum_string = grid[:zz] + grid[zz].replace("_", sign) + grid[zz + 1:]
                grid_list_NEW = [[sum_string[j + 3 * i] for j in range(3)] for i in range(3)]
                cc2 = state_of_the_game(sum_string, grid_list_NEW)[0]
                if cc2 != "notfinished":
                    print('Making move level "medium"')
                    print_grid(sum_string.replace("_", " "))  # Printing newer grid
                    print(cc2) # Printing state of the game
                    stoper = True
                    return False
                    break
                else:
                    sum_string = grid
                    grid_list_NEW = [[grid[j + 3 * i] for j in range(3)] for i in range(3)]

        if sign == "X":
            sign2 = "O"
        else: 
            sign2 ="X"
        print(sign2)
        print(stoper)
        #  ruch blokujący
        if stoper == False:
            for i in range(1000): # to jest dramat - do optymalizacji :) - funkcja list_empty_spots
                zz = random.randint(0, 8)
                if grid[zz] == "_":
                    sum_string = grid[:zz] + grid[zz].replace("_", sign2) + grid[zz + 1:]
                    grid_list_NEW = [[sum_string[j + 3 * i] for j in range(3)] for i in range(3)]
                    cc2 = state_of_the_game(sum_string, grid_list_NEW)[0]
                    if cc2 != "notfinished":
                        sum_string = grid[:zz] + grid[zz].replace("_", sign) + grid[zz + 1:]
                        grid_list_NEW = [[sum_string[j + 3 * i] for j in range(3)] for i in range(3)]
                        print('Making move level "medium"')
                        print_grid(sum_string.replace("_", " "))  # Printing newer grid
                        print(cc2) # Printing state of the game
                        stoper = True
                        return sum_string
                        break
                    else:
                        sum_string = grid
                        grid_list_NEW = [[grid[j + 3 * i] for j in range(3)] for i in range(3)]
        #  zwykły ruch losowy
        if stoper == False:          
            while True:
                if '_' in grid:
                    while True:
                        zz = random.randint(0, 8)
                        if grid[zz] == "_":
                            sum_string = grid[:zz] + grid[zz].replace("_", sign) + grid[zz + 1:]
                            break
                    grid_list_NEW = [[sum_string[j + 3 * i] for j in range(3)] for i in range(3)]
                    print('Making move level "medium"')
                    print_grid(sum_string.replace("_", " "))  # Printing newer grid
                    cc2 = state_of_the_game(sum_string, grid_list_NEW)[0]
                    if cc2 != "notfinished":
                        print(cc2) # Printing state of the game
                        return False
                    else: return sum_string
                break


# narazie zróbmy, że hard musi zacząć i jest X-em
def hard_comp_move(grid, sign):
    if '_' in grid:
        if grid == '_________': # to daje gdyż serwer jet_brains miał problem z czekaniem na min_max w pierwszym ruchu
            sum_string = 'X________'
            print('Making move level "hard"')
            print_grid(sum_string.replace("_", " "))  # Printing newer grid
            return sum_string
        else:
            les = list_empty_spots(grid)
            scores__ = min_max_pio(grid, sign)
            best_score__ = scores__[0]
            list_of_scores__ = scores__[1]
            best_res_index = list_of_scores__.index(best_score__)
            zz = les[best_res_index]
            sum_string = grid[:zz] + grid[zz].replace("_", sign) + grid[zz + 1:]  
            grid_list_NEW = [[sum_string[j + 3 * i] for j in range(3)] for i in range(3)]
            print('Making move level "hard"')
            print_grid(sum_string.replace("_", " "))  # Printing newer grid
            cc2 = state_of_the_game(sum_string, grid_list_NEW)[0]
            if cc2 != "notfinished":
                print(cc2) # Printing state of the game
                return False
            else: return sum_string


def start_any_game(grid, player1, player2):
    print_grid(grid.replace("_", " "))
    while True:
        if player1 == "user":
            cc3 = user_move(grid, "X")
            if cc3 == False:
                break
        elif player1 == "easy":
            cc3 = easy_comp_move(grid, "X")
            if cc3 == False:
                break
        elif player1 == "medium":
            cc3 = medium_comp_move(grid, "X")
            if cc3 == False:
                break
        elif player1 == "hard":
            cc3 = hard_comp_move(grid, "X")
            if cc3 == False:
                break
        grid = cc3
        if player2 == "user":
            cc4 = user_move(grid, "O")
            if cc4 == False:
                break
        elif player2 == "easy":
            cc4 = easy_comp_move(grid, "O")
            if cc4 == False:
                break
        elif player2 == "medium":
            cc4 = medium_comp_move(grid, "O")
            if cc4 == False:
                break
        elif player2 == "hard":
            cc4 = hard_comp_move(grid, "O")
            if cc4 == False:
                break
        grid = cc4


grid = 9 * '_'
while True:
    who_plays = input().strip().split()
    command = who_plays[0]
    if len(who_plays) == 3:
        player1 = who_plays[1]
        player2 = who_plays[2]
    if command == "exit" and len(who_plays) == 1:
        break
    elif command != "start":
        print("Bad parameters!")
        continue
    elif player1 not in ["easy", "medium", "hard", "user"]:
        print("Bad parameters!")
        continue
    elif player2 not in ["easy", "medium", "hard", "user"]:
        print("Bad parameters!")
        continue
    else:
        start_any_game(grid, player1, player2)
        break

