import subprocess
import re
import fileinput
import time

import re
fstab_path = "/etc/fstab"
with open(fstab_path, "r") as f:
    for line in f:
        if "/boot/efi" in line and "vfat" in line:
            match = re.search(r"UUID=(\S+)\s+/boot/efi", line)
            if match:
                old_uuid = match.group(1)
                break

print("Old UUID:", old_uuid)


# Step 1: Get UUID of swap partition
blkid_output = subprocess.check_output(['sudo', 'blkid'])
for line in blkid_output.splitlines():
    line = line.decode('utf-8')
    if '/dev/sdb2: UUID="' in line:
        new_uuid = line.split()[1].split('=')[1].strip('"')
print("New UUID: ",new_uuid)


# Define the search pattern using regular expression
search_pattern = "^UUID={}\s+/boot/efi\s+vfat.*".format(old_uuid)

# Loop through each line of the file
for line in fileinput.input('/etc/fstab', inplace=True):
    # Check if the line matches the search pattern
    if re.match(search_pattern, line):
        # Replace the old UUID with the new one
        line = re.sub(old_uuid, new_uuid, line)
    # Print the line to the file (with or without changes)
    print(line.rstrip())
print("Rebootingggggggggggg...")
time.sleep(6)
print("Nowwwwwwwwwwwwwwwwww...")
# Step 4: Reboot
subprocess.run(['sudo', 'reboot'])

