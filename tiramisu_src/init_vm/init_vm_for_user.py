import os
import subprocess
import psycopg2

def get_requirement():
	name 		= raw_input("# vm name?\n>> ")
	latency 	= input("# latency\n>> ")
	latency_max = input("# latency_max\n>> ")
	percentl 	= input("# percentl\n>> ")
	iops_min 	= input("# iops_min\n>> ")
	iops 		= input("# iops\n>> ")
	percenti 	= input("# percenti\n>> ")
	cost 		= input("# cost\n>> ")
	cost_max 	= input("# cost_max\n>> ")
	percentc 	= input("# percentc\n>> ")
	app_type 	= input("# app_type\n>> ")
	return { 	"name"			: name,
				"latency" 		: latency,
				"latency_max" 	: latency_max,
				"percentl" 		: percentl,
				"iops_min" 		: iops_min,
				"iops" 			: iops,
				"percenti" 		: percenti,
				"cost"			: cost,
				"cost_max" 		: cost_max,
				"percentc"		: percentc,
				"app_type"		: app_type }

def cal_percent(pc, data):
	return (data * pc) / 100.00

def create_cube(requirements):
	latency_min	= requirements["latency"] - cal_percent(requirements["percentl"], requirements["latency"])
	latency 	= requirements["latency"]
	latency_max = requirements["latency_max"]
	percentl 	= requirements["percentl"]
	iops_min 	= requirements["iops_min"]
	iops 		= requirements["iops"]
	iops_max 	= requirements["iops"] + cal_percent(requirements["percenti"], requirements["iops"])
	percenti 	= requirements["percenti"]
	cost_min 	= requirements["cost"] - cal_percent(requirements["percentc"], requirements["cost"])
	cost 		= requirements["cost"]
	cost_max 	= requirements["cost_max"]
	percentc 	= requirements["percentc"]
	app_type 	= requirements["app_type"]
	return { 	"latency_min"	: latency_min,
				"latency" 		: latency,
				"latency_max" 	: latency_max,
				"percentl" 		: percentl,
				"iops_min" 		: iops_min,
				"iops" 			: iops,
				"iops_max"		: iops_max,
				"percenti" 		: percenti,
				"cost_min"		: cost_min,
				"cost"			: cost,
				"cost_max" 		: cost_max,
				"percentc"		: percentc,
				"app_type"		: app_type }

if __name__ == "__main__":
	try:
	    conn = psycopg2.connect(database='tiramisu', user='postgres', host='localhost', port='5432', password='12344321')
	except:
	    print "Nooooooooo"

	c = conn.cursor()

	requirements = get_requirement()

	command = "cp ../image/HDD/default ../image/HDD/" + requirements["name"]
	print(command)
	os.system(command)

	command = "cp ../image/config/default.xml ../image/config/" + requirements["name"] + ".xml"
	print(command)
	os.system(command)

	command = "sed -i -e 's/<name>default<\/name>/<name>" + requirements["name"] + "<\/name>/g' ../image/config/" + requirements["name"] + ".xml"
	print(command)
	os.system(command)

	command = "sed -i -e 's/\/image\/HDD\/default/\/image\/HDD\/" + requirements["name"] + "/g' ../image/config/" + requirements["name"] + ".xml"
	print(command)
	os.system(command)

	command = "sudo virsh define ../image/config/" + requirements["name"] + ".xml"
	print(command)
	os.system(command)

	command = "sudo virsh start " + requirements["name"]
	print(command)
	os.system(command)

	print "########## Preparing machine ##########"

	while True:
	        p = subprocess.Popen(['sudo', './kvm_findip', requirements["name"]], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	        ip, err = p.communicate()
	        if ip != "":
	                print "########## Complete ##########"
	                print "Your IP : "
	                print(ip)
	                break

	print "Default username : centos7\nDefault password : root"

	cube = create_cube(requirements)

	c.execute("insert into cube (vm_name,latency_min,latency,latency_max,percentl,iops_min,iops,iops_max,percenti,cost_min,cost,cost_max,percentc,app_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (requirements["name"],cube["latency_min"],cube["latency"],cube["latency_max"],cube["percentl"],cube["iops_min"],cube["iops"],cube["iops_max"],cube["percenti"],cube["cost_min"],cube["cost"],cube["cost_max"],cube["percentc"],cube["app_type"],))
	c.execute("insert into vm (name,ip,status) values (%s,%s,1)", (requirements["name"],ip,))
	c.execute("insert into storage (vm_name,current_pool,appropiate_pool) values (%s,'HDD','HDD')", (requirements["name"],))
	c.execute("insert into requirements (vm_name,latency,latency_max,percentl,iops_min,iops,percenti,cost,cost_max,percentc,app_type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (requirements["name"],requirements['latency'],requirements['latency_max'],requirements['percentl'],requirements['iops_min'],requirements['iops'],requirements['percenti'],requirements['cost'],requirements['cost_max'],requirements['percentc'],requirements['app_type'],))
	conn.commit()
	c.close()
