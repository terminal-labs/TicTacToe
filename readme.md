I've been looking for an excuse for a while to do something with genetic algorithms. I've never written one, but I find something attractive about them. So, the first thing I thought of when I saw this problem was to try to write a genetic algorithm for it. I realized shortly there after that it is sort of silly to write a genetic algorithm for something that is bruteforceable. A genetic algorithm might make sense for Tic Tac Toe if for example you wanted the computer to win as often as possible, but this was not a requirement and time was a constraint. So, I instead sought to find a way to bruteforce the game. I made an engine for the game and then ran all possible games against that engine, storing a hash for their state and the outcome of the particular game. The idea here was that I would be able to look up the possible outcomes from my current state and choose a move that was shown to lead to favorable outcomes. This sort of worked, but getting this method to work in trivial cases was proving difficult. So, at the expense of purity, I added in a few simple tests like, "Can I win now?" now and "Can I block now?". With these everything was going (mostly) well, and I had a system for the computer that would not lose.

The typical approach to this problem is to follow a procedure such as: "Can I win? No. Can I block? No Can I fork / block a fork?. The difficult logic in this approach deals with forks. What happened for me is that the data set of game states seemed to handle the issue of forks. I had to use logic for the more trivial cases, but for the more advanced problems, the precomputed game state was able to point to computer towards a win / draw. Not what I was expecting.

If you want to run this project yourself, in addition to the normal django requirements, you will need to compute the "rainbow table" of game state. It is about 30 MB and takes about 30 seconds to generate. To do this just run simulator.py from the command line