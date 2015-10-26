import os
import subprocess
import sqlite3


conn = sqlite3.connect('tiramisu')
c = conn.cursor()

name = raw_input("# vm name?\n>> ")
command = "rbd cp storage1/default storage1/" + name
print(command)
os.system(command)

command = "cp config/default.xml config/" + name + ".xml"
print(command)
os.system(command)

command = "sed -i -e 's/<name>default<\/name>/<name>" + name + "<\/name>/g' config/" + name + ".xml"
print(command)
os.system(command)

command = "sed -i -e 's/storage1\/default/storage1\/" + name + "/g' config/" + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh define config/" + name + ".xml"
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

c.execute("insert into vm (name,ip,status,pool) values (?,?,1,'storage1')", (name,ip,))
conn.commit()
c.close()
