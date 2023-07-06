from mecode import G

g = G()

#g.arc(x=0, y=1, radius=1, direction='CW')
g.meander_arc(5, 7, spacing=0.50, start='UL', orientation='x')
#g.meander(5, 7, spacing=1, start='LL', orientation='y')
#g.better_arc(10, 20, 5, 10)
'''
g.move(11,0)  # move 11 mm in x and 0mm in y

g.arc(x=10, y=5, radius=12, direction='CCW')  # counterclockwise arc with a radius of 20

g.meander(5, 7, spacing=1)  # trace a rectangle meander with length 5mm, 7 fingers, with 1mm spacing between passes

g.move(-1,0) # move -1 mm in x

g.abs_move(x=10, y=0)  # move the tool head to position (10, 0)

# g.home()  # move the tool head to the origin (0, 0)
'''