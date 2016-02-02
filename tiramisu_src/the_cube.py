

#########################################################################################
# data recieve from outside

def requirements():
	# create requirement table to store all of this (column by column)
	# this function will read data from table and store in dictionary
	# edit value when user change requirement
	latency = input("latency = ")
	latency_max = input("latency_max = ")
	percentl = input("% = ")

	iops_min = input("iops_min = ")
	iops = input("iops = ")
	percenti = input("% = ")

	cost = input("cost = ")
	cost_max = input("cost_max = ")
	percentc = input("% = ")

	app_type = input("app type\n1 is website\n2 is database\n3 is batch job\n: ")

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
	latency_hdd = input("latency from HDD = ")
	latency_ssd = input("latency from SSD = ")

	iops_hdd = input("IOPS from HDD = ")
	iops_ssd = input("IOPS from SSD = ")

	return {	"latency_hdd" 	: latency_hdd,
				"latency_ssd" 	: latency_ssd,
				"iops_hdd"		: iops_hdd,
				"iops_ssd"		: iops_ssd }
	
def get_vm_details():
	# receive from outside
	img_name = input("image name = ")
	size = input("image size = ")
	return {	"img_name" 	: img_name,
				"size"		: size }

#########################################################################################

def cal_percent(pc, data):
	return (data * pc) / 100

def read_current_storage():
	# read from DB
	return 'HHD1'

def increase_size(cube):
	cube["percentl"] = cube["percentl"] + cube["percentl"]
	cube["percenti"] = cube["percenti"] + cube["percenti"]
	cube["percentc"] = cube["percentc"] + cube["percentc"]
	return cube

def decrease_size(cube):
	cube["percentl"] = cube["percentl"] - cube["percentl"]
	cube["percenti"] = cube["percenti"] - cube["percenti"]
	cube["percentc"] = cube["percentc"] - cube["percentc"]

def is_in_cube(cube, point):
	l_min = cube["latency"] - cal_percent(cube["percentl"], cube["latency"])
	i_max = cube["iops"] + cal_percent(cube["percenti"], cube["iops"])
	c_min = cu

	if 	(l_min <= cube["latency"] and cube["latency"] <= cube["latency_max"] and 
		cube["iops_min"] <= cube["iops"] and cube["iops"] <= i_max and 
		c_min <= cube["cost"] and cube["cost"] <= cube["cost_max"]) :
		return 1
	else:
		return 0

def find_other_storage_in_cube(point_storage, cube, current_point):
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
		return [1, current_point, current]
	else:
		return [0, [], 0]

if __name__ == "__main__":
	cost_SSD = 0.031
	cost_HDD = 0.094

	requirements = requirements()
	storage_status = storage_status()

	point_storage = { 	"SSD" : [storage_status["latency_ssd"], storage_status["iops_ssd"], cost_SSD],
						"HDD" : [storage_status["latency_hdd"], storage_status["iops_hdd"], cost_HDD] }



	current = read_current_storage()
	current_point = point_storage[current]

	cube = requirements
	if is_in_cube(cube, current_point):
		while 1:
			cube = decrease_size(cube)
			if not is_in_cube(cube, current_point) :
				result = find_other_storage_in_cube(point_storage, cube, current_point)
				if result[0] == 1:
					current_point = result[1]
					current = result[2]
				else:
					print("not move")
					break
	else:
		# current storage not meet requirement
