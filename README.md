# genus_g_minesweeper
 
## How to play
 
usage: python play_game.py [genus] [# tiles] [# mines]

Note: # tiles/(4 * genus) must be a perfect square

Here's a short demo playing the game:

https://user-images.githubusercontent.com/33708611/122474158-71ff7100-cf88-11eb-95ef-bff39b935f6e.mov

If you press any key, it will perform a single solve step.

## Problems I'm thinking about

 * Is it possible to implement graph neural networks to predict the probability a tile is a mine? What about other machine learning structures?
 * The idea of using machine learning here is to learn patterns to predict whether a tile contains a mine. Given the graph of a tile's neighborhood, is it possible to automatically classify the pattern required to predict the tile?