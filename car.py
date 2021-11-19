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





    def __init__(self,speed,birthTime):
        self.carBirth=birthTime
        self.speed=speed*5280/3600
        self.carTime=self.carBirth
        self.speed=-1*self.speed
        self.carMaxSpeed=self.speed
        self.carIdealExitTime=(7*330+46*6)/speed



    #helper methods
    def findTime2GetBack2Speed(self):
        newTime=(self.carMaxSpeed-self.speed)/self.carAccel
        return newTime
    #these states will need to be checked for when the car despawns this may be calculatable in carstates by checking
    #if the position is over and subtracting the time it took to go over
    def greenState(self,time):

        if self.speed==self.carMaxSpeed:
            self.carPosition=self.carPosition+self.carMaxSpeed*(time-self.carTime)
        else:
            accelTime=self.findTime2GetBack2Speed(time)
            self.carPosition=self.carPosition+self.speed*(accelTime)+(1/2*self.carAccel*(accelTime)**2)
            self.speed=self.carMaxSpeed
            self.carPosition+=(time-(accelTime+self.carTime))*self.speed

    def yellowState(self,time):
        #the yellow light will end at the given time
        #check if the car will be pass the crosswalk by the time the yellow light turns yellow or if it won't
        #reach the crosswalk by the time the light turns green
        if (self.carPosition-self.carLength+8*self.speed-(crosswalkPosition+crosswalkWidth))>0 or(self.carPosition+26*self.speed)<crosswalkPosition:
            self.carPosition+=self.speed*(time-self.carTime)

        #check if the car needs to slow down but not stop
        #elif (self.carPosition+self.speed*26)>crosswalkPosition and\
        #        (self.carPosition-self.carLength+self.speed*26)<crosswalkPosition+crosswalkWidth:
        elif (self.carPosition-self.carLength)+car.speed*(time-self.carTime):
            pass

    def redState(self,time):
        # the red light will end at the given time

        #check if the car is far behind the crosswalk and will not need to stop at all or
        #if it is passed the crosswalk
        if self.carPosition+self.speed*(time-self.time)<crosswalkPosition or self.carPosition-self.carLength>crosswalkPosition+crosswalkWidth:
            if self.speed==self.carMaxSpeed:
                self.carPosition=self.carPosition+self.carMaxSpeed*(time-self.carTime)
            else:
                accelTime=self.findTime2GetBack2Speed(time)
                self.carPosition=self.carPosition+self.speed*(accelTime)+(1/2*self.carAccel*(accelTime)**2)
                self.speed=self.carMaxSpeed
                self.carPosition+=(time-(accelTime+self.carTime))*self.speed
        elif 
    # methods
    def carStates(self,lightState,time):

        if lightState=="Green":
            self.greenState(time)
        elif lightState=="Yellow":
            self.yellowState(time)
        elif lightState=="Red":
            self.redState(time)
        self.carTime=time


