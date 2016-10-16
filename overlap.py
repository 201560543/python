from os import system
import sys
system('clear')
print 'OVERLAP GRAPH APPROACH \n(for finding the shortest superstring from its sub-strings)\n'

def overlap_suffix_to_prefix(s1, s2):
        len1 = len(s1)
        len2 = len(s2)
	pre1 = ()
	pre2 = ()
	v = ()
        if len1 != 0 and len2 != 0:
		for i in range(len(s1)-1, -1, -1):
			for j in range(len(s2)-1):
				a = s1[i:] 
				b = s2[:j+1]
				if a == b:
					v = (i, j) 
	if len(v) != 0:
		check = 'T'
	else:
		check = 'F'
	return (check, v)

substring  = ['gtacgt', 'tacgta', 'acgtac', 'cgtacg', 'gtacga', 'tacgat']
index = []
print "overlap-regions:"
for i in range(len(substring)):
	mx  = -1000
	for j in range(i+1, len(substring)):
		ol = overlap_suffix_to_prefix(substring[i], substring[j])
		if ol[0] == 'T':
			if mx < ol[1][-1]:
				mx = ol[1][-1]
				print substring[i], "(", ol[1][0]+1, '-', len(substring[i]), '), ', 
				print substring[j], "(", 1, '-', mx+1, ')' 
				index.append(ol[1][-1])
superstring = substring[0]
for j in range(1, len(substring)):
	superstring += substring[j][index[j-1]+1:]
print "\nSub-strings: "
for e in substring:
	print e, 
print "\n\nSmallest super-string: "
print superstring
