import fileinput
import sys

files = sys.argv[1:]

last = None
backup = []

for line in fileinput.input(files, inplace=True):
    number = line.rstrip().split(";")[0]

    if number != last:
        last = number
        for i in backup: print i.rstrip()
        backup = []
    backup.append(line)

# for line in fileinput.input(files, inplace=True):
#     if line.rstrip():
#         print line.rstrip()

