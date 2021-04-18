xa=float(input("First x:"))
ya=float(input("First y:"))
xb=float(input("Second x:"))
yb=float(input("Second y:"))
k=(ya-yb)/(xa-xb)
b=ya-k*xa
if k==1:
    if b==0:
        print("y=x")
    else:
        print("y=x+",b,sep="")
elif b>0:
    print("y=",k,"x+",b,sep="")
elif b<0:
    print("y=",k,"x",b,sep="")
elif b==0:
    print("y=",k,"x",sep="")
