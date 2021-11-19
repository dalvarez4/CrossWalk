#this file will be used to write the functions of the car and its characteristics
blockLength=330
crosswalkWidth=24
streetWidth=46

class car:

    #car charecteristics:
    carLength = 9
    carAccel = 10
    carPosition=0
    carBirth=0
    carTime=0
    carMaxSpeed=0
    crosswalkPosition=1181#330*3+46*3+330/2-24/2




    def __init__(self,speed,birthTime):
        self.carBirth=birthTime
        self.speed=speed*5280/3600

        self.speed=-1*self.speed
        self.carMaxSpeed=self.speed

    # methods
    def carStates(self,lightState,time):
        #this may need some editing for when the light is green but the car will need to stop to not run the red
        if lightState=="Green":
            if self.speed==self.carMaxSpeed:
                self.carPosition=self.carPosition+self.carMaxSpeed*(time-self.carTime)
            else:
                self.carPosition=self.carPosition+self.speed*(time-self.carTime)+(1/2*self.carAccel*(time-self.carTime)**2)
                self.speed=self.speed+(time-self.carTime)*self.carAccel
                if self.speed>self.carMaxSpeed:
                    self.speed=self.carMaxSpeed

        if lightState=="Yellow":

