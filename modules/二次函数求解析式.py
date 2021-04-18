x1 = float(input("First x: "))
y1 = float(input("First y: "))
x2 = float(input("Second x: "))
y2 = float(input("Second y: "))
x3 = float(input("Third x: "))
y3 = float(input("Third y: "))
try:
    a_f = (y1-y2)/((x1-x2)*(x1-x3))-(y2-y3)/((x2-x3)*(x1-x3))
    b_f = (y1-y2)/(x1-x2)-a_f*(x1+x2)
    c_f = y1-a_f*x1*x1-b_f*x1
    print("二次项系数为:", a_f)
    print("一次项系数为:", b_f)
    print("常数项为:", c_f)
except Exception:
    print("不存在。")