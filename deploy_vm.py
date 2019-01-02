import csv

from libproxmox import Proxmox

proxmox = Proxmox(target_node="svr-corpnet03")

CSV_DIR = "./deployment.csv"
print("[INFO  ] Deploying from:", CSV_DIR)

deployed = []

row_count = 0

with open(CSV_DIR, "r") as file:
    csvfile = csv.reader(file)
    for row in csvfile:
        if row_count==0:
            pass
        else:
            print("[DEBUG ]:", row)
            deployed.append(proxmox.deploy_vm(row))
        time.sleep(1)
        row_count += 1

print("[INFO  ] VMs deployed:", deployed)

for vm_id in deployed:
    proxmox.start_vm(vm_id)

print("[INFO  ] VMs started:", deployed)
