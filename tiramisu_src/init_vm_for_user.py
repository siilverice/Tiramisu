import os
import subprocess

name = raw_input("# vm name?\n>> ")
command = "rbd cp storage1/default storage1/" + name
print(command)
os.system(command)

command = "cp default.xml " + name + ".xml"
print(command)
os.system(command)

command = "sed -i -e 's/<name>default<\/name>/<name>" + name + "<\/name>/g' " + name + ".xml"
print(command)
os.system(command)

command = "sed -i -e 's/storage1\/default/storage1\/" + name + "/g' " + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh define " + name + ".xml"
print(command)
os.system(command)

command = "sudo virsh start " + name
print(command)
os.system(command)

print "########## COMPLEATE ##########"

while True:
        p = subprocess.Popen(['sudo', './kvm_findip', name], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        ip, err = p.communicate()
        if ip != "":
                print "Your IP : "
                print(ip)
                break

print "Default username : centos7\nDefault password : root"
