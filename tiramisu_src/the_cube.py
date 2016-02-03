import ipdb


#########################################################################################
# data recieve from outside

def requirements():
	# create requirement table to store all of this (column by column)
	# this function will read data from table and store in dictionary
	# edit value when user change requirement
	
	# latency = input("latency = ")
	# latency_max = input("latency_max = ")
	# percentl = input("% = ")

	# iops_min = input("iops_min = ")
	# iops = input("iops = ")
	# percenti = input("% = ")

	# cost = input("cost = ")
	# cost_max = input("cost_max = ")
	# percentc = input("% = ")

	# app_type = input("app type\n1 is website\n2 is database\n3 is batch job\n: ")

	latency = 4
	latency_max = 10
	percentl = 5
	iops_min = 400
	iops = 500
	percenti = 10
	cost = 50
	cost_max = 100
	percentc = 10
	app_type = 1

	return { 	"latency" 		: latency,
				"latency_max" 	: latency_max,
				"percentl" 		: percentl,
				"iops_min" 		: iops_min,
				"iops" 			: iops,
				"percenti" 		: percenti,
				"cost"			: cost,
				"cost_max" 		: cost_max,
				"percentc"		: percentc,
				"app_type"		: app_type }

def cube():
	# create cube table to store all of this (column by column) (copy from requirement at first)
	# this function will read data from table and store in dictionary
	# edit value when squeeze or puff

	latency = 4
	latency_max = 10
	percentl = 5
	iops_min = 400
	iops = 500
	percenti = 10
	cost = 50
	cost_max = 100
	percentc = 10
	app_type = 1

	return { 	"latency" 		: latency,
				"latency_max" 	: latency_max,
				"percentl" 		: percentl,
				"iops_min" 		: iops_min,
				"iops" 			: iops,
				"percenti" 		: percenti,
				"cost"			: cost,
				"cost_max" 		: cost_max,
				"percentc"		: percentc,
				"app_type"		: app_type }

def storage_status():
	# recieve from systemtap
	# systemtap will exec this code

	# latency_hdd = input("latency from HDD = ")
	# latency_ssd = input("latency from SSD = ")

	# iops_hdd = input("IOPS from HDD = ")
	# iops_ssd = input("IOPS from SSD = ")

	latency_hdd = 6
	latency_ssd = 2
	iops_hdd = 300
	iops_ssd = 800

	return {	"latency_hdd" 	: latency_hdd,
				"latency_ssd" 	: latency_ssd,
				"iops_hdd"		: iops_hdd,
				"iops_ssd"		: iops_ssd }
	
def get_size_vm():
	# receive from outside
	# size = input("image size = ")
	size = 1000
	return size

def read_current_storage():
	# read from DB
	return 'HDD'

#########################################################################################

def cal_percent(pc, data):
	return (data * pc) / 100.00

def cal_cost(cost_mb, size):
	return cost_mb * size

def increase_size(cube):
	cube["percentl"] = cube["percentl"] + cube["percentl"]
	cube["percenti"] = cube["percenti"] + cube["percenti"]
	cube["percentc"] = cube["percentc"] + cube["percentc"]
	return cube

def decrease_size(cube):
	if cube["percentl"] > 0:
		cube["percentl"] = cube["percentl"] - cube["percentl"]
	if cube["percenti"] > 0:
		cube["percenti"] = cube["percenti"] - cube["percenti"]
	if cube["percentc"] > 0:
		cube["percentc"] = cube["percentc"] - cube["percentc"]
	return cube

def is_in_cube(cube, point):
	l_min = cube["latency"] - cal_percent(cube["percentl"], cube["latency"])
	i_max = cube["iops"] + cal_percent(cube["percenti"], cube["iops"])
	c_min = cube["cost"] - cal_percent(cube["percentc"], cube["cost"])

	if 	(l_min <= cube["latency"] and cube["latency"] <= cube["latency_max"] and 
		cube["iops_min"] <= cube["iops"] and cube["iops"] <= i_max and 
		c_min <= cube["cost"] and cube["cost"] <= cube["cost_max"]) :
		return 1
	else:
		return 0

def find_other_storage_in_cube(point_storage, cube, current_point, current):
	first = 1
	found = 0
	for storage in point_storage:
		if storage != current:
			other_point = point_storage[storage]
			if is_in_cube(cube, other_point):
				if not found:
					found = 1
				if first:
					current_point = point_storage[storage]
					first = 0
				else:
					if app_type == 1: 
						# website care low latency
						if other_point[0] < current_point[0]:
							current_point = other_point
							current = storage
					elif app_type == 2:
						# database care high iops
						if other_point[1] > current_point[1]:
							current_point = other_point
							current = storage
					else:
						# batch job care low cost
						if other_point[2] < current_point[2]:
							current_point = other_point
							current = storage
	if found:
		return [1, current_point, current]
	else:
		return [0, [], 0]

def squeeze(point_storage, cube, current_point, current):
	while 1:
		cube = decrease_size(cube)
		if not is_in_cube(cube, current_point) :
			result = find_other_storage_in_cube(point_storage, cube, current_point, current)
			if result[0] == 1:
				current_point = result[1]
				current = result[2]
			else:
				return current
		elif cube["percentc"] <= 0 and cube["percenti"] <= 0 and cube["percentl"] <= 0:
			return current

def puff(point_storage, cube):
	while 1:
		cube = increase_size(cube)
		first = 1
		found = 0
		for storage in point_storage:
			other_point = point_storage[storage]
			if is_in_cube(cube, other_point):
				if not found:
					found = 1
				if first:
					current_point = point_storage[storage]
					first = 0
				else:
					if app_type == 1: 
						# website care low latency
						if other_point[0] < current_point[0]:
							current_point = other_point
							current = storage
					elif app_type == 2:
						# database care high iops
						if other_point[1] > current_point[1]:
							current_point = other_point
							current = storage
					else:
						# batch job care low cost
						if other_point[2] < current_point[2]:
							current_point = other_point
							current = storage
		if found:
			return current		

if __name__ == "__main__":
	cost_mb_SSD = 0.094
	cost_mb_HDD = 0.031

	cube = requirements()
	get_size_vm = get_size_vm()
	cost_SSD = cal_cost(cost_mb_SSD, get_size_vm)
	cost_HDD = cal_cost(cost_mb_HDD, get_size_vm)

	storage_status = storage_status()

	point_storage = { 	"SSD" : [storage_status["latency_ssd"], storage_status["iops_ssd"], cost_SSD],
						"HDD" : [storage_status["latency_hdd"], storage_status["iops_hdd"], cost_HDD] }

	current = read_current_storage()
	current_point = point_storage[current]
	if is_in_cube(cube, current_point):
		print squeeze(point_storage, cube, current_point, current)
	else:
		# current storage not meet requirement
		result = find_other_storage_in_cube(point_storage, cube, current_point, current)
		if result[0] == 1:
			# still have other point in requirement
			current_point = result[1]
			current = result[2]
			print squeeze(point_storage, cube, current_point, current)
		else:
			# not have any point in requirement
			print puff(point_storage, cube)