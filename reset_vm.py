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
    next(csvfile, None)  # skip the headers
    for row in csvfile:
        print("[DEBUG ]:", row)
        vm_id = row[0]

        proxmox.stop_vm(vm_id)
        time.sleep(1)
        proxmox.del_vm(vm_id)

        print("[INFO  ] Deleted:", vm_id)

        time.sleep(1)
        row_count += 1

print("[INFO  ] Deleted deployment")
