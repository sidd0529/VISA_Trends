from __future__ import division
from copy import deepcopy


#----------------------------- Sorting  --------------------------------------------------------------------
def sort_group(indx, column1, column2):
	"""
	Parameters
	----------	
	indx : integer
	column1 : list data type (contains strings of SOC NAMES / WORK STATES which need to be ordered.)
	column2 : list data type (contains integers which denote numbers of of certified applications.)    

	Returns
	------- 
	sort_group : list 
			Returns a list where the entry at index 'indx' of column1 has been put in its proper 
			place as per alphabetical ordering. 

	Examples
	--------
	>>> t1 = ['aaa', 'a', 'az', 'ay', 'ab', 'aa', 'ac', 'd', 'b', 'c']
	>>> t2 = [7,6,5,5,5,5,5,4,3,3] 

	>>> Bu = sort_group(2, t1, t2)
	>>> Bu

	['aaa', 'a', 'aa', 'az', 'ay', 'ab', 'ac', 'd', 'b', 'c']   

	The returned result is always a list of the same length as column1.    		   
	"""
	j = indx+1
	check = True
	while ( (check) and (j<len(column2)) ):
		if ( column2[indx] == column2[j] ):
			if ( column1[indx] > column1[j] ):
				dum = column1[indx]
				column1[indx] = column1[j]
				column1[j] = dum

		if ( column2[indx] > column2[j] ):	
			check = False	

		j += 1		

	return column1	


#----------------------------- Alphabetical ordering of columns ----------------------------------------
def ordering(col1, col2, num):
	"""
	Parameters
	----------	
	col1 : list data type (contains strings of SOC NAMES / WORK STATES which need to be ordered.)
	col2 : list data type (contains integers which denote numbers of of certified applications.) 
	num : integer (number of rows that the output file will contain.)   

	Returns
	------- 
	ordering : list 
			Returns a list where all entries in col1 are alphabetically sorted (when their corresponding
			entries in col2 have same values.) 

	Examples
	--------
	>>> t1 = ['aaa', 'a', 'az', 'ay', 'ab', 'aa', 'ac', 'd', 'b', 'c']
	>>> t2 = [7,6,5,5,5,5,5,4,3,3] 

	>>> y = sort_group(t1, t2, 5)
	>>> y	

	['aaa', 'a', 'aa', 'ab', 'ac']

	The returned result is always a list of length 'num'.		   
	"""	
	col1_cp = deepcopy(col1)

	col1_processed = ['']*num

	i = 0
	while ( i < num-1 ):
		if ( col2[i] > col2[i+1] ):
			col1_processed[i] = col1_cp[i]

		else:
			col1_cp = sort_group(indx=i, column1=col1, column2=col2)
			col1_processed[i] = col1_cp[i]

		i += 1


	col1_processed[i] = col1[i]	

	return col1_processed 
