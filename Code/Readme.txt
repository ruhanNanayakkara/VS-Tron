MODES

Edit line 42, 43 to change modes.
mcts - PROGRAM uses Monte Carlo Tree Search.
minimax - PROGRAM uses Minimax.
user - USER.

----------------------------------------------------------------
RULES

Movements - W, S, A, D or Arrow Keys.
Can only change directionns in right-angles. (Agent moving
left can't turn right, agent moving up can't turn down)
Crashing into trails (opponent or yours) causes loss.
Crashing into walls causes loss.

----------------------------------------------------------------
DEPENDENCIES

Pyglet - pip install pyglet==1.5.27

----------------------------------------------------------------
ISSUES

Audio doesn't pllay too well when playing against AI (stutter).
Disable audio by commenting lines 51, 53.