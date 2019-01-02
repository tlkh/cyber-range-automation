import hashlib
import subprocess
import csv


class Proxmox(object):

    def __init__(self, target_node=None, salt="nosalt"):
        self.salt = salt
        self.target_node = target_node

    def run_cmd(self, bash_command):
        print("[INFO  ] Running:", bash_command)
        with open("stdout.log", "wb") as out, open("stderr.log", "wb") as err:
            process = subprocess.Popen(
                bash_command.split(), stdout=out, stderr=err)
            process.wait()
            output, error = process.communicate()
        return output

    def deploy_vm(self, row):
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
        self.set_ci(target_id, user_displayname, ci_ip_addr, windows_vm=windows_vm)

        print("[INFO  ] Deployed:", target_id)
        return target_id

    def del_vm(self, target_id):
        target_id = str(int(target_id))
        command = "qm destroy "+target_id
        self.run_cmd(command)

    def start_vm(self, target_id):
        target_id = str(int(target_id))
        command = "qm start "+target_id
        self.run_cmd(command)

    def stop_vm(self, target_id):
        target_id = str(int(target_id))
        command = "qm stop "+target_id
        self.run_cmd(command)
    
    def clone_vm(self, template_id, target_id, target_name=None):
        template_id = str(int(template_id))
        target_id = str(int(target_id))
        if target_name is not None:
            target_name = str(target_name)
        else:
            target_name = str(template_id)+"_clone"

        command = "qm clone "+template_id+" "+target_id+" --name "+target_name
        if self.target_node is not None:
            command = command + " --target " + self.target_node
        self.run_cmd(command)

    def set_ci(self, target_vm, display_name, ip_addr, windows_vm=False):
        target_vm = str(int(target_vm))
        display_name = str(display_name)
        ip_addr = str(ip_addr)
        if len(ip_addr.split(".")) != 4:
            raise ValueError("[ERROR ] Invalid IP address provided: "+ip_addr)

        if windows_vm:
            citype = "configdrive2"
        else:
            citype = "nocloud"

        username = display_name.lower().replace(" ", "").replace(",", "")

        h = hashlib.new('ripemd160')
        h.update(bytes(display_name+self.salt))
        password = str(h.hexdigest())

        commands = []
        commands.append("qm set "+target_vm+"--citype "+citype)
        commands.append("qm set "+target_vm+"--ciuser "+username)
        commands.append("qm set "+target_vm+"--cipassword "+password)
        commands.append("qm set "+target_vm+"--ipconfig0 ip= "+ip_addr+"/16")

        for command in commands:
            self.run_cmd(command)
