from controller import Robot
from controller import PositionSensor as PS
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

    def __init__(self, row, column, ContName):
        self.ContName = ContName
        self.Column = column
        self.Row = row
        Xvalues = np.arange(-0.4, 0.6, 0.2) # makes an array that starts in -0.4 and stops in 0.6(but will not include stop), and steps 0.2.
        Yvalues = np.arange(-0.6, 0.8, 0.2)
        self.xcord = Xvalues[self.Column] # from the generated array of X-values will the given colum input determine wich X-value the container gets.
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

    def Sens(self, SensAxis):
        """This function is to get the current value of the linear motor.

        Args:
            SensAxis (String): This desides the sensor to get a value from.

        Returns:
            Float: The value from the wanted sensor. 
        """
        if SensAxis == "X":
            return PS("Sensor_X").getValue() # uses the class PositionSensor to get the value of "Sensor_X" from the robot.  
        if SensAxis == "Y":
            return PS("Sensor_Y").getValue()
        if SensAxis == "Z":
            return PS("Sensor_Z").getValue()

    def ExtendZ(self, Z=bool):
        """Extends the gantry arm to pickup a container on the future shelf.
        Args:
            Z (bool, optional): If the bool is True, then the gantry extends the arm, and if False to opesite happens. Defaults to bool.
        """
        maxZ = 0 # this is the zero postition of the gantry arm.
        minZ = -0.35 #The gantry arm can only extend this far, else the arm will break. 
        if Z == True:
            self.zMotor.setPosition(minZ) # extends the arm

        if Z == False:
            self.zMotor.setPosition(maxZ) # retracts the arm

Frequency = 100 # the number of iterations before moving to the next command
Iteration = 0
Extendtime = 0 # this will be used for when to extend and when to retract. 

timestep = 32 # time step for the simulation. 
PS("Sensor_X").enable(timestep) # this starts the sensors at the first timestep 
PS("Sensor_Y").enable(timestep)
PS("Sensor_Z").enable(timestep)

containerList = [Container(0, 0, "havregryn"), Container(5, 4, "mel"), Container(2, 1, "kanel")] # here we instantiat the containers, and will use this to know what container to go to and where to go to. 
commands = ["havregryn", "mel", "kanel"]# this is the names of the containers we search for when the main loop is running.

while robot.step(timestep) != -1:#This is the main loop
    timeIndex = floor(Iteration/Frequency)
    Extendtime += 1

    if Extendtime == Frequency:
        Extendtime = 0
    
    for i in range(len(containerList)):
    
        if containerList[i].ContName == commands[timeIndex]:
            
            Gantry().MoveGanToXY(containerList[i])

            if containerList[i].xcord == Gantry().Sens("X") and containerList[i].ycord == Gantry().Sens("Y"):
                if 20 <= Extendtime <=40 :
                    Gantry().ExtendZ(True)

                if 60 <= Extendtime <= 70 :
                    Gantry().ExtendZ(False)
                
            
        
    Iteration += 1
    if Iteration >= (len(commands)*Frequency):
        Iteration = 0