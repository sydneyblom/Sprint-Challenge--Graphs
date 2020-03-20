from room import Room
from player import Player
from world import World

import random
#evalutes python expression
from ast import literal_eval
world = World()


map_file = "maps/main_maze.txt"
# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)
#initialize visited with world.starting_room
player = Player(world.starting_room)
 # final result path
traversal_path = []
# for back-tracking
# traversal is the complete path of the player, reverse_path is more flexible and will be used to help player return to an active room after a dead end.
reverse_path = []
#create a visited dictionary to track which rooms have been hit already.
#will have key of room id and value of exits array
visited = {}
#map opposite directions for easy reuse.
opposite = {
    'n': 's',
    's': 'n',
    'e': 'w',
    'w': 'e'
    }
# init visited dict with format {room.id: [exits dictions]}
visited[player.current_room.id] = player.current_room.get_exits()               
#while the length of the visited dictionary is less than the length of the provided room_graph:                                       
 # while we haven't visited ALL the rooms: ERROR -- need len(room_graph) - 1 ?
while len(visited) < len(room_graph) - 1:                                      

# if the current room hasn't yet been added to visited:
    if player.current_room.id not in visited:
        #add it to the dictionary by id with a value of an array of all exits - not a set bc needs to be able to be modified
        # add the id as a key and add the exits as an array for the value.
        visited[player.current_room.id] = player.current_room.get_exits()
        # grab the opposite of the last traveled direction - the path back
        prev = reverse_path[-1]
        # and remove the path back from the exits to the current room so we don't revisit it
        visited[player.current_room.id].remove(prev)
        # shuffle the exits for current room - this will make it run differently every time.
        random.shuffle(visited[player.current_room.id])

# while there are no exits remaining to explore for a room - deadend
    while len(visited[player.current_room.id]) == 0:
        # pop the path back from path and set to prev
        prev = reverse_path.pop()
        # add that direction to the final traversal path bc this is part of players path as they move backwards
        traversal_path.append(prev)
         # and then move the player in the direction - back to the last room that still has exits left to explore
        player.travel(prev)
# grab that first random direction from the current room in visited
    move_direction = visited[player.current_room.id].pop(0)
    # add it to traversal path
    traversal_path.append(move_direction)
    # add the OPPOSITE of it to the path
    reverse_path.append(opposite[move_direction])
# then move in that direction
    player.travel(move_direction)                                                   

# TRAVERSAL TEST 
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)
for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print()
    print(len(traversal_path))
    print()
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")
