import time
import csv
import pickle

from libproxmox import Proxmox

proxmox = Proxmox()

CSV_DIR = "./deployment.csv"
print("[INFO  ] Reading deployment from:", CSV_DIR)

print("[INFO  ] Deleting deployment")

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

            proxmox.stop_vm(target_id)
            time.sleep(1)
            proxmox.del_vm(target_id)

            print("[INFO  ] Cloned:", target_id)

        time.sleep(1)
        row_count += 1

print("[INFO  ] Deleted deployment")
