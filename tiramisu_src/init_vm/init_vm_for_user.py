import os
import subprocess
import sqlite3


conn = sqlite3.connect('../tiramisu.db')
c = conn.cursor()

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

command = "cp ../image/HDD/default ../image/HDD/" + name
print(command)
os.system(command)

command = "cp ../image/config/default.xml ../image/config/" + name + ".xml"
print(command)
os.system(command)

command = "sed -i -e 's/<name>default<\/name>/<name>" + name + "<\/name>/g' ../image/config/" + name + ".xml"
print(command)
os.system(command)

command = "sed -i -e 's/\/image\/HDD\/default/\/image\/HDD\/" + name + "/g' ../image/config/" + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh define ../image/config/" + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh start " + name
print(command)
os.system(command)

print "########## Preparing machine ##########"

while True:
        p = subprocess.Popen(['sudo', './kvm_findip', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ip, err = p.communicate()
        if ip != "":
                print "########## Complete ##########"
                print "Your IP : "
                print(ip)
                break

print "Default username : centos7\nDefault password : root"

c.execute("insert into vm (name,ip,status) values (?,?,1)", (name,ip,))
c.execute("insert into storage (vm_name,current_pool,appropiate_pool) values (?,'HDD','HDD')", (name,))
c.execute("insert into requirements (latency,latency_max,percentl,iops_min,iops,percenti,cost,cost_max,percentc,app_type) values (?,?,?,?,?,?,?,?,?,?)", (latency,latency_max,percentl,iops_min,iops,percenti,cost,cost_max,percentc,app_type,))
conn.commit()
c.close()