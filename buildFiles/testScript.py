import os

f = open('Res.txt', 'w')
f.close()

for _ in range(50):
	#os.system("python ScrabGUI_CVC.py 0 2 >/dev/null")
	os.system("python ScrabGUI_MontyVMidas.py >/dev/null")

k = open('Res.txt', 'r')

Monty = 0
Midas = 0
for line in k:
	if "WON" in line:
		if line.strip().split()[0] == "MONTY": Monty += 1; continue
		elif line.strip().split()[0] == "MIDAS": Midas += 1; continue
		else: print "This was weird: "+line
	if "TIE" in line: Monty += 1; Midas += 1
k.close()

print "MONTY COUNT:", Monty
print "MIDAS COUNT:", Midas

print "MONTY WINS:", (Monty*100.0)/(Monty+Midas)
print "MIDAS WINS:", (Midas*100.0)/(Monty+Midas)