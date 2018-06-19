# Branch-and-Bound-based-Bi-Partitioning

 This is an implementation of a branch and bound method based bi-partitioning algorithm. 
 
### Objective

- To design a program to distribute nodes into two partitions while minimizing the number of nets that share both partitions. The size of the both partitions should be equal and can differ by at most 1 only if there are an odd number of nodes.

### Design Rules

 * If there are an even number of total nodes, the partition sizes of both partitions should be equal.
 * If there are an odd number of nodes, the partition sizes of both partitions can vary by 1.
 * If the nodes of a net share both partitions, then the net contributes +1 to the total cost. For example: In fig.1, the total cost is 3 as there are 3 nets who have their nodes crossing the partition line. In the circuit, the total number of nodes is 19 and the number of nodes assigned to the left and right partitions are 10 and 9, respectively.


### PseudoCode of Implementation Framework
'''
1: select circuit
2: Extract netlist data
3: set initial best cost and partition size
4: Use routine function recursively to obtain a solution
5: Show the final partition in a GUI.
'''


### Pseudocode of Routine Function
'''
1: routine( current_assignments, current_node, best_cost){
2:	if we have no further nodes to explore or are at a leaf/solution
3:		if current solution has lesser cost than the best solution
4:			update the best cost with the current cost
5:	End if  End if
6: 	else:
7:		calculate label x
8:		if(x is less than the best cost)
9:			if (left partition is not full)
10:				get temporary assignment by adding current_node to the left partition
11:				get next node to assign
12:				if (cost of temporary assignment is less than the best cost)
13:					repeat routine with parameters (temporary assignment, next node and best cost)
14:			End if End if
15:			if (right partition is not full)
16:				get temporary assignment by adding current_node to theright partition
17:				get next node to assign
18:				if (cost of temporary assignment is less than the best cost)
19:					repeat routine with parameters (temporary assignment, next node and best cost)
20:		End if  End if   End if
'''


