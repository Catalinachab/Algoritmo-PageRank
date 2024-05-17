from matricesRalas import *
W= MatrizRala(10,10)
#W[i,j]= 1 si pj cita a pi
# 0=A 1=B 2=C 3=D 4=E 5=F 6=G 7=H 8=I 9=J 10=K

W[0,2]= 1
W[0,3]=1
W[0,4]=1
W[1,0]=1
W[4,10]=1
W[5,0]=1
W[5,6]=1
W[6,7]=1
W[6,8]=1
W[6,0]=1
W[7,8]=1
W[8,5]=1
W[9,8]=1

D = MatrizRala(10,10)
D[0,0]= 1/3
D[2,2]=1
D[3,3]=1
D[4,4]=1
D[5,5]=1
D[6,6]=1
D[7,7]=1
D[8,8]=1/2
D[10,10]=1

I = MatrizRala(10,10)
I[0,0]= 1
I[1,1]=1
I[2,2]=1
I[3,3]=1
I[4,4]=1
I[5,5]=1
I[6,6]=1
I[7,7]=1
I[8,8]=1
I[9,9]=1
I[10,10]=1
I_2 = MatrizRala(10,1)
I[0,0]= 1
I[1,0]=1
I[2,0]=1
I[3,0]=1
I[4,0]=1
I[5,0]=1
I[6,0]=1
I[7,0]=1
I[8,0]=1
I[9,0]=1
I[10,0]=1


p_estrella_it = MatrizRala(10,1)
p_estrella_it[0,0]= 1/11
p_estrella_it[1,0]=1/11
p_estrella_it[2,0]=1/11
p_estrella_it[3,0]=1/11
p_estrella_it[4,0]=1/11
p_estrella_it[5,0]=1/11
p_estrella_it[6,0]=1/11
p_estrella_it[7,0]=1/11
p_estrella_it[8,0]=1/11
p_estrella_it[9,0]=1/11
p_estrella_it[10,0]=1/11

d=0.85

A =I- d*(W@D) 
b=((1-d)/11)*I
p_estrella = GaussJordan(A,b)
i=0
print(p_estrella)
t=10
while i<t:
    p_estrella_it = ((1-d)/11)*I_2 + d*W@D@p_estrella_it
    i+=1

print(p_estrella_it)    
