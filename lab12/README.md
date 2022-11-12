Copyright **`(c)`** 2022 Enrico Magliano `<s295692@studenti.polito.it>`
# Lab 1: Set Covering
<p>
  For this problem I have implemented a <b>Uniform Cost Search Algorithm</b>, in jupyter notebook is the function UCF().
</p>
<p>
In which the cost (weight) is the number of repeated element.</br>For example with N = 5 and solution = [ [0,2], [1,2,3,4] ] the cost is 1, due to the fact that the number 2 is reapeted.
</p> 
<p>
 I have also create a specific class MyNode for store all the data structures that I need to represent a node.
</p>
<p>
 I based my solution on the Pseudocode found in https://python.plainenglish.io/uniform-cost-search-ucs-algorithm-in-python-ec3ee03fca9f.
 </P>
 <p>
  Numbers of visited nodes for different N values:<br/>
   - N = 5 -> 122 nodes visited<br/>
   - N = 10 -> 874 nodes visited<br/>
   - N = 20 -> 23.416 nodes visited<br/>
   With bigger N is not feasible the execution.
  </p>
