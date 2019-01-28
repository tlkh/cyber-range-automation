import subprocess
import csv

def run_cmd(bash_command):
    print("[INFO  ] Running:", bash_command)
    with open("stdout.log", "wb") as out, open("stderr.log", "wb") as err:
        process = subprocess.Popen(
            bash_command.split(), stdout=out, stderr=err)
        process.wait()
        output, error = process.communicate()
        if output is not None:
            print("[DEBUG ] Ouput:", str(output))
        if error is not None:
            print("[ERROR ] Error:", str(error))
    return output

# start here

CSV_DIR = "./deployment.csv"
print("[INFO  ] Deploying from:", CSV_DIR)

with open(CSV_DIR, "r") as file:
    csvfile = csv.reader(file)
    next(csvfile, None)  # skip the headers
    for row in csvfile:
        print("[DEBUG ]:", row)

        vm_id, user_displayname = row[0].strip(), row[1].strip()
        ci_ip_addr, vm_os, vm_type = row[2].strip(), row[3].strip(), row[4].strip()
        meta_dept, meta_pos = row[5].strip(), row[6].strip()

        display_name = user_displayname.replace(","," ")
        appointment = meta_dept + " " + meta_pos
        display_name = display_name+"("+appointment+")"

        hostname = display_name.replace("  ", "").replace(" ", "-").lower()
        hostname = hostname + "-workstation"

        # ping
        command = "ansible all -i '" + ci_ip_addr +  ",' -m ping"
        run_cmd(command)

        # change user's meta data (GECOS/comment)
        command = "ansible all -i '" + ci_ip_addr +  ",' -m user -a "
        attributes = """ "comment='""" + display_name + """' " """
        run_cmd(command+attributes)

        # edit VM hostname
        command = "ansible all -i '" + ci_ip_addr +  ",' -m hostname -a "
        attributes = """ "name='""" + hostname + """' " """

        # add software packages
        # TODO: pending local mirror

        # reboot VM
        command = "ansible all -i '" + ci_ip_addr +  ",' -m reboot"
        run_cmd(command)

print("[INFO  ] Done!")
