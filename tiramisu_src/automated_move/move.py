import os
import time

name = raw_input("# VM name\n>> ")
command = "sudo virsh shutdown " + name
os.system(command)
print(command)
time.sleep(15)

os.system("sudo virsh list --all")

command = "sudo virsh undefine " + name
print(command)
os.system(command)

old_pool = raw_input("# old pool\n>> ")
new_pool = raw_input("# new pool\n>> ")
img_name = raw_input("# image name\n>> ")
command = "rbd cp " + old_pool + "/" + img_name + " " + new_pool + "/" + img_name
print(command)
os.system(command)

command = "rbd rm " + old_pool + "/" + img_name
print(command)
os.system(command)

filename = raw_input("# path to config xml filename (filename **without** .xml)\n>> ")
command = "sed -i -e 's/" + old_pool + "\/" + img_name + "/" + new_pool + "\/" + img_name + "/g' " + filename + ".xml"
print(command)
os.system(command)

command = "sudo virsh define " + filename + ".xml"
print(command)
os.system(command)

command = "sudo virsh start " + filename
print(command)
os.system(command)
