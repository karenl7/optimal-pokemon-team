
# optimal-pokemon-team
To run the code, you should run the notebook "playPOKEMON.ipynb".


To use the small Pokemon set, go to line 30 in pokemonMDP.py and change it to "pd = small_pd". Otherwise use "pd = full_pd" to use the full set of Pokemon.
Also go to line 542 in pokemon_data.py and change "pokemon_moves_assignment = small_pokemon_moves_assignment" if you want to use the small Pokemon set or "pokemon_moves_assignment = full_pokemon_moves_assignment" if oyu want to use the full moves assignment.

1. Model-Based Monte-Carlo. This code which requires the small subset, otherwise it will take a really long time to run.

2. Q-learning. This section will run q-learning twice to get the 1 and 2-level policy. This can use either the small or full Pokemon subset.

3. Genetic algorith. This part will select an optimal team based on the learned policies. It will run several times for different team size.

4. Interactive battling. This is when a human can enter their moves and play against a opponent that is using a learned policy.

5. Extra code used to generate the numbers in the tables in our paper. This requires the small subset version.
