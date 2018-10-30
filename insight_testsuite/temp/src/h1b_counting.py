"""
Calculates top 10 occupations and top 10 states for which visas are awarded.
"""
from __future__ import division #For decimal division.
import csv #For reading and writing of csv files.
import time #Check time of computation.
from copy import deepcopy #For creating copies of lists.
import argparse  #For entering path of input and output files using command line
from alphabetical import ordering #Self defined function for alphabetical sorting.


# -------------------------------- Header/ metadata --------------------------------------------------------
__author__ = "Siddharth Satpathy"
__date__ = "30 October 2018"
__version__ = "1.0.0"
__email__ = "siddharthsatpathy@gmail.com"
__status__ = "Complete"


# -------------------------------- Input arguments ---------------------------------------------------------
"""
Uses argparse to give input and output filepaths to python program in command line.

Usage: python path to h1b_counting.py -input input_filepath -out1 output_top_occupations_filepath -out2 output_top_states_filepath
Example: python ./src/h1b_counting.py -input ./input/h1b_input.csv -out1 ./output/top_10_occupations.txt -out2 ./output/top_10_states.txt

Uses
----------
args.input : string type
args.out1 : string type
args.out2 : string type

"""
parser = argparse.ArgumentParser(description='Calculates top occupations and states for certified visa applicants.')
parser.add_argument('-input', default='./input/h1b_input.csv', help='Enter path of input file.')
parser.add_argument('-out1', default='./output/top_10_occupations.txt', help='Enter path of output file of top 10 occupations.')
parser.add_argument('-out2', default='./output/top_10_states.txt', help='Enter path of output file of top 10 states.')


args = parser.parse_args()
input_file = args.input
out_file1 = args.out1
out_file2 = args.out2

start_time = time.time()


# -------------------------------- Unique values of columns ------------------------------------------------
"""
Reads input file and finds unique values of CASE STATUSES, SOC NAMES and WORK STATES.

Important parameters
----------
col_socname : set data type
col_state : set data type
socname_unq : list data type (contains unique entries of SOC NAMES.)
state_unq : list data type (contains unique entries of WORK STATES.)
socname_count : list data type (contains counts of certified applications of SOC NAMES.)
state_count : list data type (contains counts of certified applications of WORK STATES.)
"""
col_socname, col_state = set(), set()
rownum = 0

with open(input_file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=';')

	for row in csv_reader:
		if (rownum==0):
			header = row		

			status_indx = ( [ i for i, s in enumerate(header) if 'STATUS' in s ] )[0]
			soc_name_indx = ( [ i for i, s in enumerate(header) if ( ('SOC' in s) and ('NAME' in s) ) ] )[0]
			state_indx = ( [ i for i, s in enumerate(header) if ( ('WORK' in s) and ('STATE' in s) ) ] )[0]		

		if (rownum>0):
			col_socname.add(row[soc_name_indx])	
			col_state.add(row[state_indx])


		rownum += 1


socname_unq, state_unq = list(col_socname), list(col_state)


socname_count = [0]*len(socname_unq)
state_count = [0]*len(state_unq)


# -------------------------------- Count -------------------------------------------------------------------
"""
Counts the number of certified applications of SOC NAMES and WORK STATES.
"""
cert = 0
rownum = 0

with open(input_file) as csv_file:
	csv_reader = csv.reader(csv_file, delimiter=';')

	for row in csv_reader:
		if (rownum>0):
			if (row[status_indx]=='CERTIFIED'): 
				cert = cert + 1

				row_socname_indx = socname_unq.index(row[soc_name_indx])
				row_state_indx = state_unq.index(row[state_indx])

				socname_count[row_socname_indx] += 1
				state_count[row_state_indx] += 1


		rownum += 1


# -------------------------------- Final Processing (TOP OCCUPATIONS) --------------------------------------
"""
Sorts data in desired format and saves output file for top occupations.

Important parameters
----------
topnum_soc : takes the number 10, or the number of unique values of SOC NAME (if the latter is less than 10.) 

socname_count_sorted : list data type (socname_count sorted in descending order.)
socname_unq_sorted : list data type (unique entries of SOC NAME rerranged in the same pattern as the indices of 
                                    socname_count during sorting.) 
socname_count_sorted_cp : list data type (Python deep copy of socname_count_sorted.)
socname_unq_sorted_cp  : list data type (Python deep copy of socname_unq_sorted.)

top_occs_col1 : list data type (Top occupations gotten after sorting. Alphabetically sorted in case of ties.)
top_occs_col2 : list data type (Number of applications that have been certified for occupations given in top_occs_col1.)
top_occs_col3 : list data type (% of applications that have been certified for occupations given in top_occs_col1.) 
"""
topnum_soc = min( 10, len(socname_unq) ) 

zip_socname = sorted( zip(socname_count, socname_unq), key=lambda t:-t[0] )
socname_count_sorted = [b[0] for b in zip_socname]
socname_unq_sorted = [b[1] for b in zip_socname]

socname_count_sorted_cp = deepcopy(socname_count_sorted)
socname_unq_sorted_cp = deepcopy(socname_unq_sorted)

top_occs_col1 = ordering( col1=socname_unq_sorted_cp, col2=socname_count_sorted_cp, num=topnum_soc )
top_occs_col2 = socname_count_sorted[:topnum_soc]
top_occs_col3 = [ round( ( (x*100)/(cert) ) , 1 ) for x in top_occs_col2 ]

header_soc = ['TOP_OCCUPATIONS', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE'] 

with open(out_file1, 'w') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(header_soc)
    for row in zip(top_occs_col1, top_occs_col2, (str(x)+'%' for x in top_occs_col3)):
        w.writerow(row)


# -------------------------------- Final Processing (TOP STATES) -------------------------------------------
"""
Sorts data in desired format and saves output file for top occupations.

Important parameters
----------
topnum_state : takes the number 10, or the number of unique values of WORK STATES (if the latter is less than 10.) 

state_count_sorted : list data type (state_count sorted in descending order.)
state_unq_sorted : list data type (unique entries of WORK STATES rerranged in the same pattern as the indices of 
                                    state_count during sorting.) 
state_count_sorted_cp : list data type (Python deep copy of state_count_sorted.)
state_unq_sorted_cp  : list data type (Python deep copy of state_unq_sorted.)

top_states_col1 : list data type (Top states for jobs gotten after sorting. Alphabetically sorted in case of ties.)
top_states_col2 : list data type (Number of applications that have been certified for occupations given in top_states_col1.)
top_states_col3 : list data type (% of applications that have been certified for occupations given in top_states_col1.) 
"""
topnum_state = min( 10, len(state_unq) )

zip_state = sorted( zip(state_count, state_unq), key=lambda t:-t[0] )
state_count_sorted = [b[0] for b in zip_state]
state_unq_sorted = [b[1] for b in zip_state]

state_count_sorted_cp = deepcopy(state_count_sorted)
state_unq_sorted_cp = deepcopy(state_unq_sorted)

top_states_col1 = ordering( col1=state_unq_sorted_cp, col2=state_count_sorted_cp, num=topnum_state )
top_states_col2 = state_count_sorted[:topnum_state]
top_states_col3 = [ round( ( (x*100)/(cert) ) , 1 ) for x in top_states_col2 ]

header_states = ['TOP_STATES', 'NUMBER_CERTIFIED_APPLICATIONS', 'PERCENTAGE']

with open(out_file2, 'w') as f:
    w = csv.writer(f, delimiter=';')
    w.writerow(header_states)
    for row in zip(top_states_col1, top_states_col2, (str(x)+'%' for x in top_states_col3)):
        w.writerow(row)

end_time = time.time()    
print("--- Analysis of immigration data finished in %s seconds o_o ---" % (end_time - start_time))    
