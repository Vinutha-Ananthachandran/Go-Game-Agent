# Go-Game-Agent
Go-game agent that learns using Min-Max and Alpha-Beta pruning algorithms

1. Overview
The AI agent is based on Search, Game Playing, and Reinforcement Learning to play a small version of the Go game, called Go-5x5 or Little-Go, that has a reduced board size of 5x5. This agent can play this Little-Go game against some basic as well as more advanced AI agents. 

2. Game Description
Go is an abstract strategy board game for two players, in which the aim is to surround more territory than the opponent. The basic concepts of Go (Little-Go) are very simple:
- Players: Go is played by two players, called Black and White.
- Board: The Go board is a grid of horizontal and vertical lines. The standard size of the board is 19x19, but in this homework, the board size will be 5x5.
- Point: The lines of the board have intersections wherever they cross or touch each other. Each intersection is called a point. Intersections at the four corners and the edges of the board are also called points. Go is played on the points of the board, not on the squares.
- Stones: Black uses black stones. White uses white stones.

The basic process of playing the Go (Little-Go) game is also very simple:
- It starts with an empty board,
- Two players take turns placing stones on the board, one stone at a time,
- The players may choose any unoccupied point to play on (except for those forbidden by the “KO” and “no-suicide” rules).
- Once played, a stone can never be moved and can be taken off the board only if it is captured.

The entire game of Go (Little-Go) is played based on two simple rules: Liberty (No-Suicide) and KO.

3. Input and Output
Input: input.txt from the current (“work”) directory. The format is as follows:
- Line 1: A value of “1” or “2” indicating which color you play (Black=1, White=2)
- Line 2-6: Description of the previous state of the game board, with 5 lines of 5 values each.
This is the state after your last move. (Black=1, White=2, Unoccupied=0)
- Line 7-11: Description of the current state of the game board, with 5 lines of 5 values each.
This is the state after your opponent’s last move (Black=1, White=2, Unoccupied=0).
For example:
========input.txt========
2
00110
00210
00200
02000
00000
00110
00210
00200
02010
00000
=======================
At the beginning of a game, the default initial values from line 2 - 11 are 0.

Output: output.txt in the current (“work”) directory.
- The format of placing a stone should be two integers, indicating i and j as in Figure 2, separated
by a comma without whitespace. For example:
========output.txt=======
2,3
=======================
- If the agent waives the right to move, it writes “PASS” (all letters must be in uppercase)
in output.txt. For example:
========output.txt=======
PASS
=======================
