from controller import Robot
from math import floor
import numpy as np

robot = Robot()

class Container():
    """Generates a container, and will make the x- and y-values for the container.
     Args:
        row (int): This has the range of [0,6].
        colum (int): This has the range of [0,4].
        ContName (string): This will be the name of the container.
    """
    def __init__(self, row, colum, ContName):
        self.ContName = ContName
        self.Colum = colum
        self.Row = row

        Xvalues = np.arange(-0.4, 0.6, 0.2) # makes an array that starts in -0.4 and stops in 0.6(but will not include stop), and steps 0.2.
        Yvalues = np.arange(-0.6, 0.8, 0.2)
        self.xcord = Xvalues[self.Colum] # from the generated array of X-values will the given colum input determine wich X-value the container gets.
        self.ycord = Yvalues[self.Row]


class Gantry():
    """It initializes the robots linear motors. And has functions to make the gantry move.
    """

    def __init__(self):
        self.xMotor = robot.getDevice("Motor_X")
        self.yMotor = robot.getDevice("Motor_Y")
        self.zMotor = robot.getDevice("Motor_Z")
        
    def MoveGanToXY(self, XY):
        """Moves the gantry in the X and Y plane, to a given set of corrodinates.

        Args:
            XY (Class): The input is the class Containter and from that class is retrived the xcord and ycord.
        """
        self.xMotor.setPosition(XY.xcord) #as the input is the Container class, we can say XY.xcord and it is the same as saying, Container().xcord of the instatyateed object. 
        self.yMotor.setPosition(XY.ycord)

    def ExtendZ(self, Z=bool):
        """Extends the gantry arm to pickup a container on the future shelf.
        Args:
            Z (bool, optional): If the bool is True, then the gantry extends the arm, and if False to opesite happens. Defaults to bool.
        """
        maxZ = 0 # this is the zero postition of the gantry arm.
        minZ = -0.35 #The gantry arm can only extend this far, else the arm will break. 
        if Z == True:
            self.zMotor.setPosition(minZ)
        if Z == False:
            self.zMotor.setPosition(maxZ)


extend = False
extTime = 0
F = 100
t = 0
timestep = 32

containerList = [Container(0, 0, "havregryn"), Container(5, 4, "mel"), Container(2, 1, "Kakao pulver")] # here we instantiat the containers, and will use this to know what container to go to and where to go to. 
commands = ["havregryn", "mel", "Kakao pulver"] # this is the names of the containers we search for when the main loop is running.


while robot.step(timestep) != -1: #This is the main loop
    timeIndex = floor(t/F)

    print((t-20) % F)

    for i in range(len(containerList)):
        if containerList[i].ContName == commands[timeIndex]:
            Gantry().MoveGanToXY(containerList[i])
            if (t-20) % F == 0:
                extend = True
                Gantry().ExtendZ(extend)
                extTime = 50

            if extTime == 0 and extend == True:
                extend = False
                Gantry().ExtendZ(extend)
            else:
                extTime -= 1

    t += 1
    if t >= (len(commands)*F):
        t = 0
