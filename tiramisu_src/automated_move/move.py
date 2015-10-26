import os
import sqlite3
import subprocess


conn = sqlite3.connect('../tiramisu.db')
c = conn.cursor()

name = raw_input("# VM name\n>> ")

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

c.execute("select pool from vm where name=?",(name,))
data = c.fetchone()
old_pool = data[0]
new_pool = raw_input("# new pool\n>> ")
command = "rbd cp " + old_pool + "/" + name + " " + new_pool + "/" + name
print(command)
os.system(command)

command = "rbd rm " + old_pool + "/" + name
print(command)
os.system(command)

command = "sed -i -e 's/" + old_pool + "\/" + name + "/" + new_pool + "\/" + name + "/g' ../config/" + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh define ../config/" + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh start " + name
print(command)
os.system(command)

c.execute("update vm set pool=?,status=1 where name=?",(new_pool,name,))
conn.commit()
c.close()
