import sys
import subprocess

procs = []
for i in range(1, 6):
    proc = subprocess.Popen([sys.executable, 'src/main.py', '{}'.format(i)])
    procs.append(proc)

for proc in procs:
    proc.wait()
