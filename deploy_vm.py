import csv

from libproxmox import Proxmox

proxmox = Proxmox(target_node="svr-corpnet03")

CSV_DIR = "./deployment.csv"
print("[INFO  ] Deploying from:", CSV_DIR)

deployed = []

with open(CSV_DIR, "r") as file:
    csvfile = csv.reader(file)
    for row in csvfile:
        print("[DEBUG ]:", row)
        deployed.append(proxmox.deploy_vm(row))

print("[INFO  ] VMs deployed:", deployed)

for vm_id in deployed:
    proxmox.start_vm(vm_id)

print("[INFO  ] VMs started:", deployed)
