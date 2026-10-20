from gturtle import*
makeTurtle()
speed(-2)
setPos(0,-100)
setLineWidth(1000)
setPenColor("red")
forward(3)
setPos(50,0)
setLineWidth(400)
setPenColor("white")
repeat 360:
    forward(1)
    left(1)
setPenColor("black")
setPos(-6,0)
setLineWidth(70)
left(45)
repeat 4:
    forward(190)
    right(90)
    forward(190)
    right(180)
    forward(190)
    left(90)
    forward(190)
    left(90)


