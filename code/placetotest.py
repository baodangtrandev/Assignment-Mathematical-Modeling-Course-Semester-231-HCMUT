import gamspy import Container,Set,Parameter,Variable,Equation,Model,Sum,Sense
import numpy as np

m=Container()
i=Set(container=m,name="i",records=["i1","i2","i3","i4","i5","i6","i7","i8"])
j=Set(container=m,name="j",records=["j1","j2","j3","j4","j5"])

#Preorder cost per unit before demand
b_input=input("b=")
b_list=b_input.split()
b=Parameter(container=m,name="b",domain=j,records=np.array(b_list,dtype=int))

#Cost
l_input=input("l=")
l_list=l_input.split()
l=Parameter(container=m,name="l",domain=i,records=np.array(l_list,dtype=int))

#Price
q_input=input("q=")
q_list=q_input.split()
q=Parameter(container=m,name="q",domain=i,records=np.array(q_list,dtype=int))

#Preoder cost per unit after demand
s_input=input("s=")
s_list=s_input.split()
s=Parameter(container=m,name="s",domain=j,records=np.array(s_list,dtype=int))

#Requirement
A_matrix=[]
for k in range (8):
    row_values=input(f"A{k+1}j=")
    A_matrix.append(row_values.split())
A=Parameter(container=m,name="A",domain=[i,j],records=np.array(A_matrix,dtype=int))

#First demand
d1=Parameter(container=m,name='d1',domain=[i],records=np.random.binomial(10,0.5,8))


#Second demand
d2=Parameter(container=m,name='d2',domain=[i],records=np.random.binomial(10,0.5,8))


#Variables
#The number of parts to be ordered before production
x=Variable(container=m,name="x",domain=[j],type="integer")
#The number of units produced
z1=Variable(container=m,name="z1",domain=[i],type="integer")
#Partleft
y1=Variable(container=m,name="y1",domain=[j],type="integer")
#The number of units produced
z2=Variable(container=m,name="z2",domain=[i],type="integer")
#Partleft
y2=Variable(container=m,name="y2",domain=[j],type="integer")

#Equation
Y1_eq=Equation(container=m,name="Y1_eq",domain=[j])
z1_bound=Equation(container=m,name="z1_bound",domain=[i])
Y2_eq=Equation(container=m,name="Y2_eq",domain=[j])
z2_bound=Equation(container=m,name="z2_bound",domain=[i])

#Scenario 1:
#y1=x-A^T.z1
Y1_eq[j]=y1[j]==x[j]-Sum(i,A[i,j]*z1[i])
#0<=z1<=d1
z1_bound[i]=z1[i]<=d1[i]

#Scenario 2:
#y2=x-A^T.z2
Y2_eq[j]=y2[j]==x[j]-Sum(i,A[i,j]*z2[i])
#0<=z2<=d2
z2_bound[i]=z2[i]<=d2[i]

#obj=min(b^T*x + 0.5*[(l-q)^T*z1 - s^T*y1] + 0.5*[(l-q)^T*z2 - s^T*y2])
obj=Sum(j,b[j]*x[j]) + 0.5*(Sum(i,(l[i]-q[i])*z1[i])-Sum(j,s[j]*y1[j])) + 0.5*(Sum(i,(l[i]-q[i])*z2[i])-Sum(j,s[j]*y2[j]))

model1 = Model(container=m,
               name="model1",
               equations=[Y1_eq,z1_bound,Y2_eq,z2_bound],
               sense=Sense.MIN,
               objective=obj,   
               problem="MIP")

model1.solve()
print("> Optimal Result: ",model1.objective_value)
print("> Parts Ordered")
print(x.records)

print ("---------Scenerio 1-----------------")
print ("- First demand")  
print(d1.records)
print ("- The number of units produced")
print(z1.records)


print ("---------Scenerio 2-----------------")
print ("- Second demand")
print(d2.records)
print ("- The number of units produced")
print(z2.records)
