
Copyright **`(c)`** 2022 Enrico Magliano `<s295692@studenti.polito.it>`
# Lab 3: Policy Search

<h3>Task 1</h3>
<p>
  For the first task I have implemented the enrico strategy, in which simply checks if there is only one active row, if true takes all element and win, instead takes all element from the shortes row.<br/>
  This strategy lose agaist grabriele one, but perform better than pure random one.
</p>
<h3>Task 2</h3>
For the second task, I have implemented an hard coded strategy, that use 3 parameters (3 floating between 0 to 1):
<ul>
  <li>aggressive: more aggressive strategy has an higher probability to remove an entire line.</li>
  <li>pref_long: higher probability to work on a longest line.</li>
  <li>remove_perc: higher remove_perc, more element are removed in a line in a non aggresive ply.</li>
</ul>
<p>
   For evolving this hard coded strategy, I have used an Evolutionary Algorithm, where the genome is tuple of the 3 parameters, while fitness is the percentage of matchs won agains the opponent  (10 matches on which for an half of the games start the opponent and for the other half start the genome).</br>
   This algorithm works for 10 generation on which the offsprings are made by mutations.
</p>
<p>
  Results, percentage matchs won by my best genome against different opponents:
  <ul>
  <li>gabriele: 0.7</li>
    <li>enrico: 0.9</li>
    <li>optimal: 0.0</li>
    <li>pure random: 0.8</li>
  </ul>
  
</p>

<h3>Task 3</h3>
<p>
Work in progress...
</p>
<h3>Task 4</h3>
<p>
For the fourth task, I have implemented an agent using reinforcement learning.</br>
In particolar my agent during the training phase learning from the winning matches updating a dictionary, self.learned, where saves the relation between nim status (element per row) and the winning ply. 
Obviously use another dictionary, self.current_move, to keed track of the ply of the current match attending for the match's outcome.</br>
During the train phase the random_factor is decrease to encourage exploitation by moving forward with matches, and also the opponent is switched starting from the silliest one (pure random) to the optimal strategy.</br>
</p>
<h6>Results</h6>
<p> 
Depsite I think this is not a bad idea, the results are really bad this agent is little better than pure random strategy, but worse than all the others.</br>
I would really appreciate if someone could improve it.
</p>
<p>
 I based my solution on the Code developed in lab2 https://github.com/EnricoMagliano/computational-intelligence/edit/main/lab2 for the EA, and on the prof. Squilero code https://github.com/squillero/computational-intelligence/blob/master/2022-23/lab3_nim.ipynb for the Nim game structure.
</p>


