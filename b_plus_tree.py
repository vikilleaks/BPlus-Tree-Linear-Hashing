from __future__ import print_function
import sys, time, os
import numpy as np
import bisect

def split_node(node):
	newNode = Tree_Node()
	p = len(node.keys)
	q = len(node.child)
	newNode.is_leaf = node.is_leaf
	mid = p//2
	mid_value = node.keys[mid]
	if node.is_leaf == 1:
		newNode.keys = node.keys[mid:p]
		newNode.child = node.child[mid:q]
		newNode.next = node.next
		node.keys = node.keys[0:mid]
		node.child = node.child[0:mid]
		node.next = newNode
	else:
		newNode.keys = node.keys[mid+1:p]
		newNode.child = node.child[mid+1:q]
		node.keys = node.keys[0:mid]
		node.child = node.child[0:mid+1]
	
	return mid_value, newNode 

def range_query(tree, min_val, max_val):
	cnt = 0
	leaf = get_query_leaf(min_val, tree.root)
	while leaf is not None:
		leaf, cnt_leaf  = get_keys(min_val, max_val, leaf)
		cnt += cnt_leaf
	return cnt

def get_query_leaf(key_val, node):
	p = len(node.keys)-1
	if node.is_leaf == 0:
		if node.keys[0] >= key_val:
			return get_query_leaf(key_val, node.child[0])
		if node.keys[p] < key_val:
			return get_query_leaf(key_val, node.child[p])
		for idx in range(p):
			if key_val <= node.keys[idx+1]:
				if key_val > node.keys[idx]:
					return get_query_leaf(key_val, node.child[idx+1])
	elif node.is_leaf == 1:
		return node

def check_mid(node, mid, newNode, p):
	if mid is None:
		return None, None
	else:
		idx = bisect.bisect(node.keys, mid)
		node.keys.insert(idx, mid)
		node.child.insert(idx+1, newNode)
		if len(node.keys) <= p:
			return None, None
		else:
			return split_node(node)

def get_keys(min_val, max_val, node):
	cnt=0
	p = len(node.keys)-1
	if(p+1 == 0):
		return None, 0

	for i in range(p+1):
		temp = node.keys[i]
		if temp <= max_val and temp >= min_val:
				cnt += 1

	if node.keys[p-1] <= max_val:
		return node.next, cnt 
	if node.keys[p-1] > max_val:
		return None, cnt

def idx_query(tree, val):
	cnt = 0
	leaf = get_query_leaf(val, tree.root)
	while leaf is not None:
		leaf, cnt_leaf  = get_keys(val, val, leaf)
		cnt += cnt_leaf
	return cnt

class Tree_Node:
	def __init__(self):
		self.next = None
		self.child = []
		self.keys = []
		self.is_leaf = 1

class B_Plus_Tree():
	def __init__(self, num_keys):
		self.num_keys = num_keys
		self.root = Tree_Node()
		self.next = None
		self.child = []
		self.keys = []
		self.is_leaf = 1
	
	def insert(self, key_val, node):
		p = len(node.keys)
		flag=0
		if not node.is_leaf:
			for i in range(p):
				if flag == 1:
					break;
				if key_val < node.keys[i] and i == 0:
					mid, newNode = self.insert(key_val, node.child[0])
					flag=1;
				elif key_val >= node.keys[i] and i == p-1:
					mid, newNode = self.insert(key_val, node.child[-1])
					flag=1;
				elif key_val < node.keys[i+1] and key_val >= node.keys[i]:
					mid, newNode = self.insert(key_val, node.child[i+1])
					flag=1;
		else:
			idx = bisect.bisect(node.keys, key_val)
			node.child.insert(idx, key_val)
			node.keys.insert(idx, key_val)
			if len(node.keys) <= self.num_keys:
				return None, None
			elif len(node.keys) > self.num_keys:
				return split_node(node)

		return check_mid(node, mid, newNode, self.num_keys)

def process_input(arg_str):
	global out_buf
	if len(arg_str)==2:
		p = int(arg_str[1])
	if len(arg_str)==3:
		p = int(arg_str[1])
		q = int(arg_str[2])

	if(arg_str[0] == "INSERT"):
		mid, newNode = tree.insert(p, tree.root)
		if mid is not None:
			new_root = Tree_Node()
			new_root.keys = [mid]
			new_root.is_leaf = False
			new_root.child = [tree.root, newNode]
			tree.root = new_root
	elif(arg_str[0] == "RANGE"):
		out = range_query(tree, p, q)
		out_buf.append(str(out))
	elif(arg_str[0] == "COUNT"):
		out = idx_query(tree, p)
		out_buf.append(str(out))
	elif(arg_str[0] == "FIND"):
		out = idx_query(tree, p)
		if out != 0:
			out_buf.append("YES")
		else:
			out_buf.append("NO")
	
	for out in out_buf:
		print(out)
	out_buf = []

def main():
	global out_buf
	with open(input_file, 'r') as file:
		in_buf = []
		for lines in file:
			line = lines.strip()
			line = line.split()
			in_buf.append(line)
		if len(in_buf) == 0:
			sys.exit("Enter input arguments in input_file")
		for arg_str in in_buf:
			process_input(arg_str)
	for i in out_buf:
		print(i)
	out_buf = []

out_buf = []

if len(sys.argv) != 2:
	sys.exit("Format: python3 bplus.py input_file")

input_file = sys.argv[1]
num_keys = 3
tree = B_Plus_Tree(num_keys)
main()