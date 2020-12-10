import fileinput
import re
	
def tab(letter1, letter2):
	if letter1.lower() == letter2.lower():
		return 0
	return 1

def Dab(word1, word2):
	Table = []
	for _ in range(len(word1)):
		Table.append([0]*len(word2))
	
	Table[0][0] = tab(word1[0],word2[0]) 
	
	same_letters = Table[0][0]
	
	for i in range(len(word2))[1:]:
		if same_letters:
			same_letters = tab(word1[0],word2[i])
			Table[0][i] = Table[0][i-1] + same_letters
		else:
			Table[0][i] = Table[0][i-1] + 1
	
	same_letters = Table[0][0]
	
	for i in range(len(word1))[1:]:
		if same_letters:
			same_letters = tab(word1[i],word2[0])
			Table[i][0] = Table[i-1][0] + same_letters
		else:
			Table[i][0] = Table[i-1][0] + 1
	

	
	for i in range(len(word1))[1:]:
		for j in range(len(word2))[1:]:		
			Table[i][j] = min(Table[i-1][j]+1,
					Table[i][j-1]+1,
					Table[i-1][j-1]+tab(word1[i],word2[j]))


	if Table[len(word1)-1][len(word2)-1] == 2:
		if len(word1) == len(word2):
			for k in range(len(word1)-1):
				if Table[k][k] == 1:
					if Table[k][k+1] == 1 and Table[k+1][k] == 1:
						Table[len(word1)-1][len(word1)-1] = 1
			
		
	return Table[len(word1)-1][len(word2)-1]


class Node:
	def __init__(self, name):
		self.name = name
		self.children = dict()

	def __str__(self):
		return (self.name)


	def find_word(self, checking_word):
		answer_list = set()
		local_root = self
		dam_lev_dist = Dab(checking_word, local_root.name)
		left_board = dam_lev_dist - 1
		right_board = dam_lev_dist + 1		
		if dam_lev_dist == 0:
			answer_list.update([local_root.name])
			return answer_list

		if len(local_root.children) != 0:
			for distance in range(left_board-1, right_board+1, 1):
				if distance in local_root.children:
					answer_list.update(local_root.children[distance].find_word(checking_word))
		
		if dam_lev_dist == 1:
			answer_list.update([local_root.name])

		return answer_list


class BK_tree:
	def __init__(self, root):
		self.root = Node(root)
	
	def add_node(self, node):
		local_root = self.root
		while True:
			dam_lev_dest = Dab(node, local_root.name)
			if dam_lev_dest in local_root.children:
				local_root = local_root.children[dam_lev_dest]
			else:
				local_root.children[dam_lev_dest] = Node(node)
				break
								
	def check_word(self, checking_word):
		return self.root.find_word(checking_word)

		
					
		
def printer(checking, mistake_report):
	if len(mistake_report) == 0:
		print(checking, '-?')
	elif checking.lower() in mistake_report:
		print(checking, '- ok')
	else:
		mistake_report = list(mistake_report)
		print(checking, '->',', '.join(map(str,sorted(mistake_report))))
		

def parse_input():
	flag = 0
	dict_size = 0
	word_list = []
	for i in fileinput.input():
		if i=='\n':
			continue
		if flag == 0:
			if len(re.findall('^\d+$', i)) != 1:
				continue
			flag = 1
			dict_size = int(re.findall('^\d+$', i)[0])
			continue
		if dict_size == 0:
			word_list.append(None)
			dict_size = -1
		if dict_size > 0:
			word_list.append(i.split('\n')[0].lower())
			dict_size-= 1
			continue
		else:
			word_list.append(i.split('\n')[0])
	flag = 0
	dictionary_out = []
	words_for_check = []

	for i in word_list:
		if flag == 0:
			if i == None:
				flag = 1
				continue
			dictionary_out.append(i)
		else:	
			words_for_check.append(i)
		
	return (dictionary_out, words_for_check)

input_list = parse_input()

dictionary, words_for_check = input_list[0],input_list[1]

TREE = BK_tree(dictionary[0])
for i in dictionary[1:]:
	TREE.add_node(i)


for word_for_check in words_for_check: 
	mistakes = TREE.check_word(word_for_check)
	printer(word_for_check, mistakes)