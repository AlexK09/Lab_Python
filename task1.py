import fileinput
import re
from math import gcd
from functools import reduce



class Bag():
	def __init__(self, max_weight):
		self.m_weight = max_weight
		self.weight = 0
		self.cost = 0
		self.elements_in_bag = []	
		

	def put_in_bag(self,weight_cost):
		if len(weight_cost) == 0:
			return
		max_weight = self.m_weight
		NOD = find_NOD(max_weight, weight_cost)

		optimized_weights = optimize_weights(max_weight, weight_cost, NOD)
		max_weight, weight_cost = optimized_weights[0],optimized_weights[1]

		Table = create_table(len(weight_cost.keys()), max_weight)
		for i in range(len(weight_cost.keys())):
			if i == 0:
				continue
			for j in range(max_weight+1):
				if weight_cost[i][0] > j:
					Table[i][j] = Table[i-1][j]
				elif Table[i-1][j] >= weight_cost[i][1]+Table[i-1][j-weight_cost[i][0]]:
					Table[i][j] = Table[i-1][j]
				else:
					Table[i][j] = weight_cost[i][1]+Table[i-1][j-weight_cost[i][0]]

		self.cost = Table[len(weight_cost.keys())-1][max_weight]
		right_board = max_weight
		for i in range(len(weight_cost.keys()))[-1:0:-1]:
			if Table[i][right_board] == Table[i-1][right_board]:
				continue
			else:
				self.elements_in_bag.append(i)
				right_board = right_board - weight_cost[i][0]

		self.weight = 0
		for i in reversed(self.elements_in_bag):
			self.weight += weight_cost[i][0]
		self.weight *= NOD



def create_table(weight_cost_len,max_weight):
	Table = []
	for _ in range(weight_cost_len):
		Table.append([0]*(max_weight+1))
	return Table

def find_NOD(max_weight, weight_cost):
	weights = []
	for pair in weight_cost.values():
		if pair == None:
			continue
		weights.append(pair[0])
	weights.append(max_weight)
	return reduce(gcd, weights)

def optimize_weights(max_weight, weight_cost, NOD):
	max_weight = int(max_weight/NOD)
	for pair in weight_cost.values():
		if pair == None:
			continue
		pair[0] = int(pair[0]/NOD)
	return max_weight, weight_cost

def bag_printer(BAG):
	if BAG == None:
		print('error')
		return
	print(BAG.weight, BAG.cost)
	for i in BAG.elements_in_bag[-1::-1]:
		print(i)


def parse_file():
	flag = 0
	input_max_weight = 0
	count = 0
	input_diction = {}
	input_diction[0]= None
	for i in fileinput.input():
		if i=='\n':
			continue
		if flag == 0:
			if len(re.findall('^\d+$', i)) != 1:
				print('error')
				continue
			input_max_weight = int(re.findall('^\d+$', i)[0])
			count += 1
			flag = 1
			continue
		if len(re.findall('^\d+ \d+$', i)) != 1:
			print('error')
			continue
		input_diction[count] = re.findall('^\d+ \d+$', i)[0].split(' ')
		input_diction[count][0] = int(input_diction[count][0])
		input_diction[count][1] = int(input_diction[count][1])
		count+=1
	if count == 0:
		return 'error'
	return (input_max_weight, input_diction)

	
if __name__ == "__main__":
	input_data = parse_file()
	bag = None
	max_weight = None
	diction = None
	if input_data != 'error':
		max_weight, diction = input_data[0], input_data[1]
		bag = Bag(max_weight)

	bag.put_in_bag(diction)
	bag_printer(bag)
