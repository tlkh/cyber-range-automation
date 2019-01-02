import csv

from libproxmox import Proxmox

proxmox = Proxmox()

CSV_DIR = "./deployment.csv"
print("[INFO  ] Deploying from:", CSV_DIR)

deployed = []

row_count = 0

with open(CSV_DIR, "r") as file:
    csvfile = csv.reader(file)
    for row in csvfile:
        if row_count == 0:
            pass
        else:
            print("[DEBUG ]:", row)
            template_id, target_id, user_displayname = row[0], row[1], row[2]
            ci_ip_addr, vm_type = row[3], row[4]
            vm_type = str(vm_type)

            target_name = str(user_displayname).replace(" ", "").split(",")
            target_name = target_name[0] + target_name[1].upper()
            target_name = target_name + "-" + vm_type

            if "windows" in vm_type.lower():
                windows_vm = True
            else:
                windows_vm = False

            self.clone_vm(template_id, target_id, target_name)

            time.sleep(1)

            print("[INFO  ] Cloned:", target_id)
            deployed.append(target_id)

        time.sleep(1)
        row_count += 1

row_count = 0

with open(CSV_DIR, "r") as file:
    csvfile = csv.reader(file)
    for row in csvfile:
        if row_count == 0:
            pass
        else:
            print("[DEBUG ]:", row)
            template_id, target_id, user_displayname = row[0], row[1], row[2]
            ci_ip_addr, vm_type = row[3], row[4]
            vm_type = str(vm_type)
            self.set_ci(target_id, user_displayname,ci_ip_addr, windows_vm=windows_vm)
        time.sleep(1)
        row_count += 1

print("[INFO  ] VMs deployed:", deployed)

for vm_id in deployed:
    proxmox.start_vm(vm_id)
    time.sleep(1)

print("[INFO  ] VMs started:", deployed)
