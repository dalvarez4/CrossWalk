#this file will be used to write the functions of the car and its characteristics
blockLength=330
crosswalkWidth=24
streetWidth=46
crosswalkPosition=1281#330*3+46*3+330/2-24/2

class car:

    #car charecteristics:
    carLength = 9
    carAccel = 10
    carPosition=0
    carBirth=0
    carTime=0
    carMaxSpeed=0
    speed=0
    delayed=False
    carExit=0
    stoppingDistance=0
    yellowTimer=0
    gb=0
    ej=0
    hj=0
    tj=0

    def __init__(self,speed,birthTime):
        self.carBirth=birthTime
        self.speed=speed*5280/3600
        self.carMaxSpeed=self.speed
        self.carIdealExitTime=(7*330+46*6)/speed+self.carBirth
        self.ej-self.carBirth
        self.stoppingDistance=1/2*self.speed**2/self.carAccel
        self.tj=self.speed/self.carAccel
    def runsRedLight(self,time):
        redLightStart=time-18

        if self.speed*(redLightStart-self.carBirth)<crosswalkPosition+crosswalkWidth+self.carLength and self.speed*(time-self.carBirth)>crosswalkPosition:
            self.delayed=True
            self.gb=time


    def checkDelay(self):
        if self.delayed:
            self.hj=self.carBirth+(7/2*blockLength+3*streetWidth-crosswalkWidth/2-self.stoppingDistance)/self.carMaxSpeed+(self.carMaxSpeed/self.carAccel)
            return self.gb-self.hj+self.tj
        else:
            return 0

    def getExitTime(self):
        return self.carIdealExitTime
