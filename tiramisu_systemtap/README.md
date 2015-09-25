# SystemTap script

### Install SystemTap

```
sudo yum install systemtap systemtap-runtime
```

Get kernel version

```
uname -r
``` 

```
wget http://debuginfo.centos.org/7/x86_64/kernel-debuginfo-(kernel_version).rpm
```
```
sudo rpm -ihv kernel-debuginfo-(kernel_version).rpm
```
```
sudo yum install kernel-devel-(kernel_version)
```
```
stap-prep
```


### Run script

```
sudo stap name.stp
```


### Create module

Create .ko module for run at another (same kernel_version) machine

```
stap -r kernel_version script -m module_name
```
after run this command it will generate **mudule_name.ko**

### Run module at another machine

```
staprun module_name.ko
```
