import os
import sqlite3
import subprocess
import sys

conn = sqlite3.connect('../tiramisu.db')
c = conn.cursor()

arg = sys.argv
name = arg[1]

c.execute("select status from vm where name=?", (name,))
status = c.fetchone()
if status[0] == 1:
        command = "sudo virsh shutdown " + name
        os.system(command)
        print(command)
        print "########## shutting down ##########"
        while True:
                p = subprocess.Popen(['sudo', './check_shutdown_vm', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                status, err = p.communicate()
                if status == "shut":
                        print "########## shut down complete ##########"
                        c.execute("update vm set status=0 where name=?", (name,))
                        break

else:
        print "already shut down"

os.system("sudo virsh list --all")

command = "sudo virsh undefine " + name
print(command)
os.system(command)

c.execute("select * from storage where vm_name=?",(name,))
data = c.fetchone()
old_pool = data[2]
new_pool = data[3]
command1 = "sudo cp ../image/" + old_pool + "/" + name + " ../image/" + new_pool + "/" + name
command2 = "sudo rm -f ../image/" + old_pool + "/" + name
command = command1 + " && " + command2
print(command)
os.system(command)

command = "sed -i -e 's/\/image\/" + old_pool + "\/" + name + "/\/image\/" + new_pool + "\/" + name + "/g' ../image/config/" + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh define ../image/config/" + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh start " + name
print(command)
os.system(command)

c.execute("update vm set status=1 where name=?",(name,))
c.execute("update storage set current_pool=? where vm_name=?",(new_pool,name,))
conn.commit()
c.close()
