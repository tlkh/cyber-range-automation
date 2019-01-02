import time
import csv
import pickle

from libproxmox import Proxmox

pve = Proxmox()

CSV_DIR = "./deployment.csv"
print("[INFO  ] Deploying from:", CSV_DIR)
print("[MESSAG] Please remember to save this output!!")

templates = {
    "centos7": "9004",
    "ubuntu18": "9001"
}

print("[INFO  ] Beginning clone process")

with open(CSV_DIR, "r") as file:
    csvfile = csv.reader(file)
    next(csvfile, None)  # skip the headers
    for row in csvfile:
        print("[DEBUG ]:", row)

        vm_id, user_displayname = row[0], row[1]
        ci_ip_addr, vm_os, vm_type = row[2], row[3], row[4]

        target_name = str(user_displayname).replace(" ", "").split(",")
        target_name = target_name[1] + target_name[0].upper()
        target_name = target_name+"-"+vm_os+"-"+vm_type

        template_id = templates[vm_os]

        pve.clone_vm(template_id, vm_id, target_name)

        print("[INFO  ] Cloned:", vm_id)
        time.sleep(1)

print("[INFO  ] Beginning cloud-init process")

deployed = []

with open(CSV_DIR, "r") as file:
    csvfile = csv.reader(file)
    next(csvfile, None)  # skip the headers
    for row in csvfile:
        print("[DEBUG ]:", row)
        
        vm_id, user_displayname = row[0], row[1]
        ci_ip_addr, vm_os, vm_type = row[2], row[3], row[4]

        if "windows" in vm_os.lower():
            windows_vm = True
        else:
            windows_vm = False
            
        deployment = pve.set_ci(vm_id, user_displayname, ci_ip_addr, windows_vm=windows_vm)
        deployed.append(deployment)
            
        time.sleep(1)

print("[INFO  ] VMs deployed:", len(deployed))

for deployment in deployed:
    print(deployment)

print("[MESSAG] Please remember to save this output!!")

"""
print("[INFO  ] Starting all VMs deployed")

for vm_id in deployed:
    proxmox.start_vm(vm_id)
    time.sleep(1)

print("[INFO  ] VMs started:", deployed)
"""
