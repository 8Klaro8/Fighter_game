# Fighter_game

# About this project
 - This is a project inspired by a team project I did with
   my fellow teammates as a final exam under a big tech firm.

# Goal
 - The goal was to imporve myself and have insight into those parts
   I did not participate directly during the development phase.

# About the game
 - You will get automatically a fighter once you login/register,
   then you are able to choose action-event pairs to fight with in the arena.
 - Once you choosed your strategy you are able to send your fighter to fight
   and from that point you have no control over your fighter, only the strategy you implanted earlier.

# Features
 - Authentication
 - Able to choose from 3 different type of actions and 3 types of events.
 - Once your fighter dies you can select an other strategy and send it back to the arena.
 - The map changes size based on player number for better playing experience.

# Further development
 - Preserve killing/ survining points after each match/death.
 - Preserve points once the game ends/closed.
 - Add more action/event to the game.
 - Create better balance among the chosen strategies.
 - Limit strategies to be chosen.
 - Create secure password storage

# Bugs
 - No current bug is known

# Docker
 - 1.) Pull the server-app and cient-app images from this profile: https://hub.docker.com/u/robingerg
 - 2.) Clone this repository
 - 3.) Check the server_socket.py and scroll to the bottom. If local config is enabled/uncommented then comment it out and below it uncomment the docker config line
 - 4.) Check the client_socket.py and scroll to the bottom. If local config is enabled/uncommented then comment it out and below it uncomment the docker config line, after that in this line: client_socket = ClientSocket(port=port, host="172.17.0.2"), repalce host="..." with your ip.
 - 5.) Play!

# Available strategy options
 - Actions: Aggressive, Defend, Run
 - Events: 1on2, In corner, below 50% Hp

# Action description
 - Aggressive: It generates a random number(1-3), 60% chance of 1, 30% of 2 and 10% of 3. This number will be deducted from the defense and will added to the attack point.
 - Defend: Adds 1+ to the defense and -1 from attack.
 - Run: Sets miss chance to 90%, however attack will be 0 or 1.
