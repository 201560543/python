import math
import scipy as sp
from scipy import *
al = []	
l = ['A','B','C']								
for i in range(0,3):								
	print "Enter the (x,y,z) co-ordinates of",l[i],":",
	a = (raw_input())
	a = a.split(' ')
	for i in range(0,3):
		a[i] = float(a[i])
		al.append(a[i])

mat = sp.array([[al[0],al[1],al[2]],[al[3],al[4],al[5]],[al[6],al[7],al[8]]])	
angval = float(raw_input("Enter the angle BCD : "))				
bond_l = float(raw_input("Enter the bond length of CD : "))			
dihe = float(raw_input("Enter the dihedral angle ABCD : "))			

AB_x = al[3]-al[0]								
AB_y = al[4]-al[1]
AB_z = al[5]-al[2]	
AB = sp.array([AB_x,AB_y,AB_z])


BC_x = al[6]-al[3]								
BC_y = al[7]-al[4]
BC_z = al[8]-al[5]
BC = sp.array([BC_x,BC_y,BC_z])


n = cross(AB,BC)								

n_sq = math.sqrt(math.pow(n[[0][0]],2) + math.pow(n[[1][0]],2) + math.pow(n[[2][0]],2))

n_dir = sp.array([n[[0][0]]/n_sq,n[[1][0]]/n_sq,n[[2][0]]/n_sq])


unit_BC_sq = math.sqrt(math.pow(BC_x,2)+math.pow(BC_y,2)+math.pow(BC_z,2))	
unit_BC = sp.array([BC_x/unit_BC_sq,BC_y/unit_BC_sq,BC_z/unit_BC_sq])

v2 = bond_l * unit_BC							#V2 has the magnitude of bond CD and its direction is not correct (has direction of BC). So, we need to rotate vector CD along the angles
#print v2
p1 = unit_BC[[0][0]]							# p1,q1,r1 are direction cosines of unit vector BC
#print p1
q1 = unit_BC[[1][0]]
#print q1
r1 = unit_BC[[2][0]]
#print r1

ct = math.cos(dihe)								
st = math.sin(dihe)								
c1 = 1 - math.cos(dihe)


matrix1 = sp.array([[ct+(p1*p1*c1), (p1*q1*c1)-(r1*st), (p1*r1*c1)+(q1*st)],[(p1*q1*c1)+(r1*st),ct+(q1*q1*c1),(q1*r1*c1)-(p1*st)],[(p1*r1*c1)-(q1*st),(q1*r1*c1)+(p1*st),ct+(r1*r1*c1)]])


angle = 180 - angval								

cost = math.cos(angle)
sint = math.cos(angle)
cos1 = 1 - math.cos(angle)

p2 = n_dir[[0][0]]
q2 = n_dir[[1][0]]
r2 = n_dir[[2][0]]


matrix2 = sp.array([[cost+(p2*p2*cos1), (p2*q2*cos1)-(r2*sint), (p2*r2*cos1)+(q2*sint)],
[(p2*q2*cos1)+(r2*sint),cost+(q2*q2*cos1),(q2*r2*cos1)-(p2*sint)],
[(p2*r2*cos1)-(q2*sint),(q2*r2*cos1)+(p2*sint),cost+(r2*r2*cos1)]])

multiply = sp.dot(matrix1,matrix2)
C = sp.array([al[6],al[7],al[8]])



D = C + (sp.dot(multiply,v2))							
print "The (x,y,z) Co-ordinates of atom D are : ", D

