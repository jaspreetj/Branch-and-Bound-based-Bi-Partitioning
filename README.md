# Branch-and-Bound-based-Bi-Partitioning

 This is an implementation of a branch and bound method based bi-partitioning algorithm. 
 
### Objective

- To design a program to distribute nodes into two partitions while minimizing the number of nets that share both partitions. The size of the both partitions should be equal and can differ by at most 1 only if there are an odd number of nodes.

### Design Rules

 * If there are an even number of total nodes, the partition sizes of both partitions should be equal.
 * If there are an odd number of nodes, the partition sizes of both partitions can vary by 1.
 * If the nodes of a net share both partitions, then the net contributes +1 to the total cost. For example: In fig.1, the total cost is 3 as there are 3 nets who have their nodes crossing the partition line. In the circuit, the total number of nodes is 19 and the number of nodes assigned to the left and right partitions are 10 and 9, respectively.


### PseudoCode of Recursion based Solution
```
1: select circuit
2: Extract netlist data
3: set initial best cost and partition size
4: Use routine function recursively to obtain a solution
5: Show the final partition in a GUI.
```


### Pseudocode of Routine Function
```
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
```

### Pseudocode of Non-recursive solution

```
1: select circuit
2: Extract netlist data
3: set initial best cost and partition size
4: add initial job to the jobs list
5: While jobs list is not empty do:
6:		sort jobs list according to the cost
7:		select first item from the jobs list
8:		add it to the closed list
9:		remove it from the jobs list
10:		if (number of nodes in left partition and right partition equal to total nodes )
11:			if current solution has smaller cost than the best cost
12:				update best solution with current solution
13:		End if End if
14:		else:
15:			if temporary cost for the current assignment is less than best cost
16:			    if left partition is accepting nodes
17:				  get a temporary assignment by adding current_node to the left list
18:				  get next node to assign
19:				  if cost of temporary assignment is less than best cost
20:					add it to the jobs list
21:			    End if End if
22:                     repeat steps 16 - 21 for right partition
23:		End else
24: End while
25: show the best solution in GUI.
```
