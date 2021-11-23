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



    #helper methods
    def findTime2GetBack2Speed(self):
        newTime=(self.carMaxSpeed-self.speed)/self.carAccel
        return newTime
    #these states will need to be checked for when the car despawns this may be calculatable in carstates by checking
    #if the position is over and subtracting the time it took to go over
    def greenState(self,time):

        if self.speed==self.carMaxSpeed:
            self.carPosition=self.carPosition+self.speed*(time-self.carTime)
        else:
            accelTime=self.findTime2GetBack2Speed()
            self.carPosition=self.carPosition+self.speed*(accelTime)+(1/2*self.carAccel*(accelTime)**2)
            self.speed=self.carMaxSpeed
            self.carPosition+=(time-(accelTime+self.carTime))*self.speed

    def yellowState(self,time):
        deltaYellowTime=time-self.yellowTimer
        self.yellowTimer=time
        deltaPos=-deltaYellowTime*self.speed+crosswalkPosition+crosswalkWidth-self.carLength
        if self.carPosition>deltaPos:
            self.carPosition+=self.speed*(time-self.carTime)
        elif crosswalkPosition-self.stoppingDistance<self.carPosition<deltaPos:
            self.carPosition+=self.speed*(time-self.carTime)-1/2*self.carAccel*(time-self.carTime)**2
            self.speed=self.speed-self.carAccel*(time-self.carTime)
        elif self.carPosition<deltaPos:
            if self.carPosition+self.speed*(time-self.carTime)<self.stoppingDistance:
                self.carPosition+=self.speed*(time-self.carTime)
            else:
                newTime=(crosswalkPosition-self.stoppingDistance-self.carPosition)/self.speed+self.carTime
                self.carPosition=crosswalkPosition-self.stoppingDistance
                self.carPosition+=self.speed*(time-newTime)-1/2*self.carAccel*(time-newTime)**2
                self.speed=self.speed-self.carAccel*(time-newTime)
        else:
            self.carPosition+=self.speed*(time-self.carTime)


    def redState(self,time):



        if self.carPosition-self.carLength>crosswalkPosition+crosswalkWidth:
            self.carPosition+=self.speed*(time-self.carTime)
        elif self.carPosition+self.speed*(time-self.carTime)>crosswalkPosition:
            self.carPosition=crosswalkPosition
            self.speed=0
        #this can be negative but I think we were told to ignore this
        elif self.carPosition+self.speed*(time-self.carTime)>crosswalkPosition-self.stoppingDistance:
            if self.carPosition>crosswalkPosition-self.stoppingDistance:
                self.carPosition+=self.speed*(time-self.carTime)-1/2*self.carAccel*(time-self.carTime)**2
                self.speed=self.speed-self.carAccel*(time-self.carTime)
            else:
                newTime=(crosswalkPosition-self.stoppingDistance-self.carPosition)/self.speed+self.carTime
                self.carPosition=crosswalkPosition-self.stoppingDistance
                self.carPosition+=self.speed*(time-newTime)-1/2*self.carAccel*(time-newTime)**2
                self.speed=self.speed-self.carAccel*(time-newTime)
        else:
            self.carPosition+=self.speed*(time-self.carTime)


    # methods
    def carStates(self,lightState,time):

        if lightState=="Green":
            self.greenState(time)
        elif lightState=="Yellow":
            self.yellowState(time)
        elif lightState=="Red":
            self.redState(time)
        self.carTime=time

    def carExit(self,time):
        if self.carPosition>=7*330+46*6:
            newTime=(self.carPosition-7*330+46*6)/self.speed
            totalTime=time-newTime
            return totalTime
        else:
            return False

    def updateYellowTime(self,time):
        self.yellowTimer=time
