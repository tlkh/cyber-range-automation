from libproxmox import Proxmox

proxmox = new Proxmox(target_node="svr-corpnet03")

CSV_DIR = "./deployment.csv"
print("[IFO  ] Deploying from:", CSV_DIR)

deployed = []

with open(CSV_DIR, "rb") as file:
    csvfile = csv.reader(file)
    for row in csvfile[1:]:
        print("[DEBUG ]:", row)
        deployed.append(proxmox.deploy_vm(row))

print("[IFO  ] VMs deployed:", deployed)

for vm_id in deployed:
    proxmox.start_vm(vm_id)

print("[IFO  ] VMs started:", deployed)
