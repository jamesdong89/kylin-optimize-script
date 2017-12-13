import sys

module = sys.argv[1]

f = open("log.txt","r")


commits = []
commit = ""

for line in f:
    if line.startswith("commit "):
        commits.append(commit)
        commit = ""
    commit += line

commits.pop(0)

count = 0
for c in commits:
    if module in c:
        count += 1
print count