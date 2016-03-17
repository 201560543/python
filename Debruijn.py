from os import system
import sys
system('clear')
print 'DE BRUIJN GRAPH APPROACH'

def get_k_mers(s, k):
	kmer = []
	for i in range(len(s)-k+1):
		part = s[i:k+i]
		kmer.append(part)
	return kmer

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
kmer = []
k = 5 
print "\nSub-strings: "
for e in substring:
	print e, 
print
print
for e in substring:
	km = get_k_mers(e, k-1)
	for v in km:
		if v not in kmer:
			kmer.append(v)
print "K-mers: (K= %s)" % (k)
for e in kmer:
	print e, 
print
print
index = []
print "overlap-regions:"
for i in range(len(kmer)):
        mx  = -1000
        for j in range(i+1, len(kmer)):
                ol = overlap_suffix_to_prefix(kmer[i], kmer[j])
                if ol[0] == 'T':
                        if mx < ol[1][-1]:
                                mx = ol[1][-1]
                                print kmer[i], "(", ol[1][0]+1, '-', len(kmer[i]), '), ',
                                print kmer[j], "(", 1, '-', mx+1, ')'
                                index.append(ol[1][-1])
superstring = kmer[0]
for j in range(1, len(kmer)):
        superstring += kmer[j][index[j-1]+1:]
print "\n\nSmallest super-string: "
print superstring
