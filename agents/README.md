# GWU - CSCI 6511 AI Algorithms Project
### Authors:
- Keith Zhang
- Anvay Paralikar
- Alex Frolov
- Ari Majumdar

### Setup:
Setup instructions in README.md at root level


### Milestone 1: State Space Calculation
Carcassone is a turn-based tile-placement game. Though the game allows for 2-5 players and game expansions, we will be focusing on 2 player games with a base set of landscape tiles and non-farmer meeples.

On each player’s turn, they will first expand a board by drawing a square tile from a set of 72 tiles, and placing it on the existing board such that at least one edge is adjacent to a previous tile, and all adjacent edges match in type. The player will then optionally place a Meeple which, along with completed features, affect scoring. A game ends once all 72 tiles are placed.

The state space is the set of unique boards that can be produced in a game of Carcassonne. 
Computing the exact state space is complicated due to the following:
- After the starting tile (`S`), each tile `t` is drawn from a non-uniformly distributed set `T` of 71 tiles. 
- Tile placement must follow a set of constraints (st. they "continue a landscape"), which is dependent on the current board shape 
- Meeple placement is also dependent on the current board shape and prior meeple placements

<!-- The Starting Tiles:
(https://wikicarpedia.com/car/Base_game)
2x Monastery
4x Monastery (F;D;2x-) -->


Based on [Heyden's masters thesis](https://project.dke.maastrichtuniversity.nl/games/files/msc/MasterThesisCarcassonne.pdf), a lower limit can be approximated based on board shapes (called polyominoes in her work).

Board starts with 1x (S) tile
Next tile is placed from remaining 71 tiles
Next tile is placed from remaining 70 tiles
...
Next tile is placed from remaining 2 tiles
Next tile is placed from remaining 1 tile








A Lower limit can be computed by estimating the number of board shapes:





