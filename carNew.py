#this file will be used to write the functions of the car and its characteristics
blockLength=330
crosswalkWidth=24
streetWidth=46
crosswalkPosition=1181#330*3+46*3+330/2-24/2

class car:

    #car charecteristics:
    carLength = 9
    carAccel = 10
    carPosition=0
    carBirth=0
    carTime=0
    carMaxSpeed=0
    speed=0
    delayAutomobile=0
    carExit=0
    stoppingDistance=0
    yellowTimer=0

    def __init__(self,speed,birthTime):
        self.carBirth=birthTime
        self.speed=speed*5280/3600
        self.carTime=self.carBirth
        self.speed=self.speed
        self.carMaxSpeed=self.speed
        self.carIdealExitTime=(7*330+46*6)/speed+self.carTime
        self.stoppingDistance=1/2*self.speed**2/self.carAccel
