import os
import subprocess
import sys
import psycopg2

try:
    conn = psycopg2.connect(database='tiramisu', user='postgres', host='localhost', port='5432', password='12344321')
except:
    print "Nooooooooo"

c = conn.cursor()

arg = sys.argv
name = arg[1]

c.execute("select status from tiramisu_vm where name=%s", (name,))
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
            c.execute("update tiramisu_vm set status=0 where name=%s", (name,))
            break

else:
    print "already shut down"

os.system("sudo virsh list --all")

command = "sudo virsh undefine " + name
print(command)
os.system(command)

c.execute("select * from tiramisu_storage where vm_name=%s",(name,))
data = c.fetchone()
old_pool = data[1]
new_pool = data[2]
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

c.execute("update tiramisu_vm set status=1 where name=%s",(name,))
c.execute("update tiramisu_storage set current_pool=%s,notice=0 where vm_name=%s",(new_pool,name,))
conn.commit()
c.close()
