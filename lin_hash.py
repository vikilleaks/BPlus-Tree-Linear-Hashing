import sys
split_idx = 0		
total_rec = 0		
mod = 1				
new_mod = 2
bucket_cnt = 2
lin_hash = {}		
bucket_blocks = {}
bucket_blocks[0] = 1
bucket_blocks[1] = 1
total_blocks = 2

def insert_val (num):
	global total_rec
	global total_blocks
	global out_buf
	global mod

	hash_val = num % (1 << mod)
	flag = 0

	if hash_val < split_idx:
		hash_val = num % (1 << new_mod)
	if hash_val not in lin_hash:
		lin_hash[hash_val] = []
		lin_hash[hash_val].append([])

	for i in range(0, bucket_blocks[hash_val]):
		if num in lin_hash[hash_val][i]:
			return 1

	total_rec += 1
	temp = bucket_blocks[hash_val] - 1
	if len(lin_hash[hash_val][temp])*4 >= buff_size:
		total_blocks += 1
		temp += 1
		bucket_blocks[hash_val] += 1
		lin_hash[hash_val].append([])

	lin_hash[hash_val][temp].append(num)
	out_buf.append(num)
	
	if len(out_buf)*4 >= buff_size:
		for val in out_buf:
			print(str(val))
		out_buf = []

	if ((total_rec*4) / (total_blocks*buff_size)) > 0.75:
		create_bucket() 

def lin_init(num):
	global total_blocks

	lin_hash[num] = []
	lin_hash[num].append([])
	bucket_blocks[num] = 1
	total_blocks += 1

def create_bucket():
	global bucket_cnt
	global split_idx
	global mod
	global new_mod
	global total_blocks

	bucket_cnt += 1
	update_arr = []

	for i in range(0, bucket_blocks[split_idx]):
		for value in lin_hash[split_idx][i]:
			update_arr.append(value)
			total_blocks -= 1

	lin_init(split_idx)
	lin_init(bucket_cnt - 1)

	for value in update_arr:
		hash_val = value % (1 << new_mod)
		if hash_val not in lin_hash:
			lin_init(hash_val)

		flag = 0
		for j in range(0, bucket_blocks[hash_val]):
			if value in lin_hash[hash_val][j]:
				return 1

		temp = bucket_blocks[hash_val] - 1
		if len(lin_hash[hash_val][temp])*4 >= buff_size:
			temp += 1
			total_blocks += 1
			lin_hash[hash_val].append([])
			bucket_blocks[hash_val] += 1
		lin_hash[hash_val][temp].append(value)
	split_idx += 1

	if bucket_cnt == (1 << new_mod):
		mod += 1
		new_mod += 1
		split_idx = 0

	return 1

def main():
	global out_buf
	in_buf = []
	with open(filename, 'r') as fh:
		for line in fh:
			num = int(line.strip())
			in_buf.append(num)
			if len(in_buf) * 4 >= ((num_buff-1) * buff_size):
				for val in in_buf:
					insert_val(val)
				in_buf = []

	for val in in_buf:
		insert_val(val)
	in_buf = []

	for val in out_buf:
		print(str(val))
	out_buf = []

out_buf = []

if len(sys.argv) != 2:
	sys.exit("Format: python3 lin_hash.py input_file")
filename = sys.argv[1]
num_buff = 2		
buff_size = 4		
main()