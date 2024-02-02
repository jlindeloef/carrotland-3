from random import randint
import os

"""
Carrot class
"""
class Carrot:
  def __init__(self, size, land, location):
    self.size = size

    if land == 'horizontal' or land == 'vertical':
      self.land = land
    else:
      raise ValueError("Value must be 'horizontal' or 'vertical'.")
    
    if land == 'horizontal':
      if location['row'] in range(row_size):
        self.placement = []
        for index in range(size):
          if location['col'] + index in range(col_size):
            self.placement.append({'row': location['row'], 'col': location['col'] + index})
          else:
            raise IndexError("Column is not in the land.")
      else:
        raise IndexError("Row is not in the land.")
    elif land == 'vertical':
      if location['col'] in range(col_size):
        self.placement = []
        for index in range(size):
          if location['row'] + index in range(row_size):
            self.placement.append({'row': location['row'] + index, 'col': location['col']})
          else:
            raise IndexError("Row is not in the land.")
      else:
        raise IndexError("Column is not in the land.")

    if self.filled():
      print_board(board)
      print(" ".join(str(place) for place in self.placement))
      raise IndexError("You searched there already")
    else:
      self.fillBoard()
  
  def filled(self):
    for place in self.placement:
      if board[place['row']][place['col']] == 1:
        return True
    return False
  
  def fillBoard(self):
    for place in self.placement:
      board[place['row']][place['col']] = 1

  def contains(self, location):
    for place in self.placement:
      if place == location:
        return True
    return False

  def found(self):
    for place in self.placement:
      if board_display[place['row']][place['col']] == 'O':
        return False
      elif board_display[place['row']][place['col']] == '*':
        raise RuntimeError("Board display inaccurate")
    return True

  
"""
Setting variables, number of rows, columns, turns and size.
""" 
row_size = 5 
col_size = 5 
num_carrots = 5
max_carrot_size = 1
min_carrot_size = 1
num_turns = 25

"""
Create the carrot list
""" 
carrot_list = []

board = [[0] * col_size for x in range(row_size)]

board_display = [["O"] * col_size for x in range(row_size)]

"""
The functions
""" 
def print_board_start(board_array):
  print('''
========================================================================
                        Welcome to Carrotland!
The rowdy rabbit has almost taken all of the carrots from the garden from
underground. He left the leaves sticking up so you don't know if there is
a carrot attached to it.
There are 5 carrots left! Find them before the rowdy rabbit does!

        X = Found a carrot!
        * = Only leaves!
                            Good Luck!
======================================================================
''') 
  print("\n  " + " ".join(str(x) for x in range(1, col_size + 1)))
  for r in range(row_size):
    print(str(r + 1) + " " + " ".join(str(c) for c in board_array[r]))
  print()

def print_board(board_array): 
  print("\n  " + " ".join(str(x) for x in range(1, col_size + 1)))
  for r in range(row_size):
    print(str(r + 1) + " " + " ".join(str(c) for c in board_array[r]))
  print()

def search_locations(size, land):
  locations = []

  if land != 'horizontal' and land != 'vertical':
    raise ValueError("land must have a value of either 'horizontal' or 'vertical'.")

  if land == 'horizontal':
    if size <= col_size:
      for r in range(row_size):
        for c in range(col_size - size + 1):
          if 1 not in board[r][c:c+size]:
            locations.append({'row': r, 'col': c})
  elif land == 'vertical':
    if size <= row_size:
      for c in range(col_size):
        for r in range(row_size - size + 1):
          if 1 not in [board[i][c] for i in range(r, r+size)]:
            locations.append({'row': r, 'col': c})

  if not locations:
    return 'None'
  else:
    return locations

def random_location():
  size = randint(min_carrot_size, max_carrot_size)
  land = 'horizontal' if randint(0, 1) == 0 else 'vertical'

  locations = search_locations(size, land)
  if locations == 'None':
    return 'None'
  else:
    return {'location': locations[randint(0, len(locations) - 1)], 'size': size,\
     'land': land}

def get_row():
  while True:
    try:
      guess = int(input("Look for carrot on row(1-5)...:"))
      if guess in range(1, row_size + 1):
        return guess - 1
      else:
        print("\nOops, that's not even in the land")
    except ValueError:
      print("Try again, look for carrot on row(1-5)...:")

def get_col():
  while True:
    try:
      guess = int(input("Choose a column(A-E):"))
      if guess in range(1, col_size + 1):
        return guess - 1
      else:
        print("\nOops, that's not even in the land.")
    except ValueError:
      print("\nPlease enter a number")

"""
Create the carrots
""" 
temp = 0
while temp < num_carrots:
  carrot_info = random_location()
  if carrot_info == 'None':
    continue
  else:
    carrot_list.append(Carrot(carrot_info['size'], carrot_info['land'], carrot_info['location']))
    temp += 1
del temp


def print_rules():
  print('''
========================================================================
                        Carrotland!
      Find the carrots before the rowdy rabbit does!

        X = Found a carrot!
        * = Only leaves!
                            Good Luck!
======================================================================
''')

os.system('clear')
print_board_start(board_display)


for turn in range(num_turns):
  print("Turn:", turn + 1, "of", num_turns)
  print("carrots left:", len(carrot_list))
  print()
  
  guess_place = {}
  while True:
    guess_place['row'] = get_row()
    guess_place['col'] = get_col()
    if board_display[guess_place['row']][guess_place['col']] == 'X' or \
     board_display[guess_place['row']][guess_place['col']] == '*':
      print("\nYou guessed that one already.")
    else:
      break

  os.system('clear')
  print_rules()
  carrot_hit = False
  for carrot in carrot_list:
    if carrot.contains(guess_place):
      print("YEAH!")
      carrot_hit = True
      board_display[guess_place['row']][guess_place['col']] = 'X'
      if carrot.found():
        print("You found a carrot!")
        carrot_list.remove(carrot)
      break
  if not carrot_hit:
    board_display[guess_place['row']][guess_place['col']] = '*'
    print("Sorry! No carrot!")

  print_board(board_display)
  
  if not carrot_list:
    break

"""
End game
""" 
if carrot_list:
  print("Sorry! The rabbit found the carrots before you did!")
else:
  print("CONGRATULATION! You found all 5 carrots! Yum! carrotcake!")
