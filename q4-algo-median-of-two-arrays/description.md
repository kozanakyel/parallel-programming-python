**Question**

Median is the middle number in a sorted list of numbers. To determine the median value in a sequence of numbers, the numbers must first be sorted, or arranged, in value order from lowest to highest or highest to lowest. If the array has even number of elements the median would be the average of two numbers in the middle.

1. Write a python script that takes two sorted arrays and returns the median of the concatenated arrays. Please do not use built-in *sort* and *median* functions from any Python package. You should implement the merge operation of the two arrays and calculation of median on your own functions.

2. Also please comment on the space and time complexity of your solution.

**Input Format**

- The first line contains a valid sorted array given as space separated numbers **input1:**. 
- The second line contains a valid sorted array given as space separated numbers **input2:**

**Output Format**
- The output should be displayed after **median:**

Expected input and output:
```
$ python3 solution.py
input1: 1 5 10
input2: 2 6
output: 5
<the merged array would be [1 2 5 6 10], the median would be 5>

$ python3 solution.py
input1: 1 5 10
input2: 2 7 10
output: 6
<the merged array would be [1 2 5 7 10 10], the median would be (5+7)/2=6>

$ python3 solution.py
input1: 1.5 1.5 2.4 3.6
input2: 2.40
output: 2.4
<the merged array would be [1.5 1.5 2.4 2.4 3.6], the median would be 2.4>