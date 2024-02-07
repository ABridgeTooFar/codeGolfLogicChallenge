Sussing It Out (The Core Part)
==============================

How good is your logical reasoning?  In this challenge, you'll rewrite an existing program that solves simple logic puzzles like those published in Dell, Penny Press, and other magazines. 

The Details
-----------

In a logic puzzle, a finite, countable set of attributes is used to identify individuals within a group. 

For example, out of 5 individuals there might be a group of 2 associated with a specific colour or type of apparel.  You'd identify them as the person with the brown shoes,or the girl with the tan bandana.

With that information and enough clues, you'll be able to solve the puzzle.  In the solution, the complete set of attributes belonging to all individuals are identified in whatever groups they belong to.

To solve the puzzle, you'll write a program that exhaustively applies three rules (more about them later) to rows and columns of a table.  

The diagram here shows the input and output. The table on the left is input to the program; the table on the right is the corresponding solution.


```
======================================           ======================================
|1    |1    |     |??|???|     |     | 1         |1    |1    |1    |1 |000| 2   |1    | 1
| 2   | 2   |     |??|???|     |     | 2         | 2   | 2   | 2   | 2|000|   4 | 2   | 2
|  3  |  3  |     |??|???|     |     | 3         |  3  |  3  |    5|00|  3|1    |    5| 3
|   4 |   4 |     |??|???|     |     | 4         |   4 |   4 |  3  |00|1  |  3  |   4 | 4
|    5|    5|     |??|???|     |     | 5         |    5|    5|   4 |00| 2 |    5|  3  | 5
======================================           ======================================
|     |     |1    |1 |???|     |     | 6         |1    |1    |1    |1 |000| 2   |1    | 6
|     |     | 2   | 2|???|     |     | 7         | 2   | 2   | 2   | 2|000|   4 | 2   | 7
|     |     |  3  |??|1  |     |     | 8         |   4 |   4 |  3  |00|1  |  3  |   4 | 8
|     |     |   4 |??| 2 |     |     | 9         |    5|    5|   4 |00| 2 |    5|  3  | 9
|     |     |    5|??|  3|     |     | 10        |  3  |  3  |    5|00|  3|1    |    5| 10
======================================           ======================================
|     |     |     |??|???|1    |     | 11        |  3  |  3  |    5|00|  3|1    |    5| 11
|     |     |     |??|???| 2   |     | 12        |1    |1    |1    |1 |000| 2   |1    | 12
|     |     |     |??|???|  3  |     | 13        |   4 |   4 |  3  |00|1  |  3  |   4 | 13
|     |     |     |??|???|   4 |     | 14        | 2   | 2   | 2   | 2|000|   4 | 2   | 14
|     |     |     |??|???|    5|     | 15        |    5|    5|   4 |00| 2 |    5|  3  | 15
======================================           ======================================
|     |     |     |??|???|     |1    | 16        |1    |1    |1    |1 |000| 2   |1    | 16
|     |     |     |??|???|     | 2   | 17        | 2   | 2   | 2   | 2|000|   4 | 2   | 17
|     |     |     |??|???|     |  3  | 18        |    5|    5|   4 |00| 2 |    5|  3  | 18
|     |     |     |??|???|     |   4 | 19        |   4 |   4 |  3  |00|1  |  3  |   4 | 19
|     |     |     |??|???|     |    5| 20        |  3  |  3  |    5|00|  3|1    |    5| 20
======================================           ======================================
|     |     |     |00| 2 |     |     | 21        |    5|    5|   4 |00| 2 |    5|  3  | 21
|     |     |     |00|???|  3  |     | 22        |   4 |   4 |  3  |00|1  |  3  |   4 | 22
|     |     |     |??|???|     |    5| 23        |  3  |  3  |    5|00|  3|1    |    5| 23
======================================           ======================================
|     | 2   |     | 2|000|     |     | 24        | 2   | 2   | 2   | 2|000|   4 | 2   | 24
======================================           ======================================
|     |     |     |??|000|   4 | 2   | 25        | 2   | 2   | 2   | 2|000|   4 | 2   | 25
======================================           ======================================
|     |1    |     |??|000|     |     | 26        |1    |1    |1    |1 |000| 2   |1    | 26
======================================           ======================================
|     |     |     |1 |000|     |1    | 27        |1    |1    |1    |1 |000| 2   |1    | 27
======================================           ======================================
|     |     |     |00|  3|1    |     | 28        |  3  |  3  |    5|00|  3|1    |    5| 28
======================================           ======================================
|     |    5|     |??|???|    5|     | 29        |    5|    5|   4 |00| 2 |    5|  3  | 29
======================================           ======================================
|     |   4 |     |??|???|     |   4 | 30        |   4 |   4 |  3  |00|1  |  3  |   4 | 30
======================================           ======================================
```

Reading the Input
-----------------

The input is in table form and starts and end with a string of '=' characters. The same string of '=' characters also separates one group of individuals (i.e. the clue) from the next.

Any line that ends with a number denotes a description of an individual in the group.  Preceding the number, you'll find a row of columns delimited by the '|' character.  A column's width stays the same for all rows in the table. The number of columns stays the same too.

Inside the table, all column contents are sets that contain numbers ranging from 0 to w, where w is the width of the column. 

When reading the input, the actual values of the column content vary from case to case:

Case 1:  all spaces or all dashes
    In this case, the content is the set of integers from 1 to w

Case 2:  all question marks
    In this case, the content is the set of integers from 0 to w

Case 3:  all zeros
    In this case, the content is the set {0}

Case 4: a parseable integer from 0 to w
    Parse the integer and store the value in a set where it is the only member

**The portions of the code responsible for parsing the input as described are not counted in the code-golf score.**


Writing the Output
-----------------

On output, all columns consist of a set with exactly one member: a value from 0 to w, where w is the width of the column.  The value is printed anywhere inside the column as a parseable integer.  The exception is the case of zero, which may be a string of zeros filling the full column width.

The value of each column is generated using the algorithm described in the next section. 

**The portions of the code responsible for printing the output as described here are not counted in the code-golf score.**

Here's Where You Fit In
-----------------------

Here is the pseudo-code that solves puzzles expressible as described above:

```
    tryAgain = True
    while tryAgain:
        solver.assertDistinctWithinGroup()
        newKnowns = solver.assertQuotaWithinSubGroup()
        changed = solver.matchAndMate()
        if newKnowns < 1 and not changed:
            tryAgain = False

```

You'll need to apply code golf skills to the pseudo-code above and to the three algorithms described in more detail below:

1. assertDistinctWithinGroup

   - for any row within a group, if the contents of a column is a single value from 1 to w, then remove that value from corresponding column for any other row in the same group.  If after doing so, more rows than before have sets with a single value from 1 to w, then repeat until no longer the case.

2. assertQuotaWithinSubGroup

   - most columns will be identical width, which I'll call W. Any group of consecutive columns with width less than W is a subgroup. Subgroups are the only columns that may contain 0 in the set of values.  For a given row and a given subgroup, exactly one of the subgroup's columns will have a non-zero value in the solution.  Therefore, if all but one column in a subgroup are single value sets containing {0}, then the remaining column cannot have zero in its set.  Remove the zero from that column.
   - furthermore, if a column in a subgroup has width w, and there are already W-w rows in the group with the single-valued set {0} in that column, then the remaining rows cannot have 0 in the column. Remove the 0 from the column for those rows.
   - return a positive integer if any resulting set is reduced to a single value.

3. matchAndMate

   - for a given column, two rows in the table may have the same single-valued but non-zero set. You'll assume that these two rows  refer to the same individual. Replace the contents of all columns in the two rows with the intersection of the sets found in both rows. If the operation changes the value of any row, return true.

For Further Information
-----------------------

If you want to get a head start, fork the reference code which can be found on [my GitHub page](https://github.com/ABridgeTooFar/codeGolfLogicChallenge). The repo supports codespaces so you can use Visual Studio Code to try out the initial implementation in a sandboxed environment.  

Whatever environment you decide to use, run the default example using python3. 

The relevant code for this part of the code golf challenge is found in the file named solver.py of the main branch.  The default table for testing is stored in a file named PCgbWI.in.

    python3 ./solver.py

To try a second example (or your own when you get used to the syntax), pass clues in table format to the program. For example:

    python3 ./solver.py TCSA.in

Ignore the other branches: files there are from before I extracted this small, algorithmically-interesting core part and split it into its own challenge 