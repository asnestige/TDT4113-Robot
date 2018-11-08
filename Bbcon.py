import time
from motob import *
from Sensob import *
from Arbitrator import *
from Behavior import *
from Sensob import *
from zumo_button import ZumoButton
from motors import *
class Bbcon:
    def __init__(self):
        self.sensobs = [Ultrasonic_sensob(), IRProximity_sensob(), Camera_sensob()]  # list of all sensory objects used by the bbcon
        self.behaviors = [Drive(), Dont_collide(self.sensobs[0], self.sensobs[1]), Stop(self.sensobs[2])]  #list of all the behavior objects used by the bbcon
        self.active_behaviors = [] # list of all behaviors that are currently active
        self.motobs = [Motob()] #list of all motor objects used by the bbcon
        self.arbitrator = Arbitrator() #the arbitrator object that will resolve actuator requests produced by the behaviors.

#Other instance variables, such as the current timestep, the inactive behaviors, and the controlled agent/robot
#may also prove useful in your implementation.
#The method set for BBCON should include the following simple procedures:

    def add_behavior(self, behaviors):  #append a newly-created behavior onto the behaviors list.
        self.behaviors.append(behaviors)

    def add_sensob(self, sensob): #append a newly-created sensob onto the sensobs list.
        self.sensobs.append(sensob)

    def activate_behaviour(self, behavior): #add an existing behavior onto the active-behaviors list.
        if behavior not in self.active_behaviors:
            self.active_behaviors.append(behavior)

    def deactive_behaviour(self, behavior): #remove an existing behavior from the active behaviors list.
        if behavior in self.active_behaviors:
            self.active_behaviors.remove(behavior)


    
    def run_one_timestep(self):
        # Update sensobs
        for sensob in self.sensobs:
            sensob.update()

        # Update behaviors
        for behavior in self.behaviors:
            behavior.update()
            if behavior.active_flag:
                self.activate_behaviour(behavior)
            else:
                self.deactive_behaviour(behavior)

        # Invoke the arbitrator by calling arbitrator.choose action
        # return an action to move the robot and boolean indicating whether or not the run should happen
        recommendations, stop = self.arbitrator.choose_action(self.active_behaviors)
        for i in range(len(self.motobs)):
            self.motobs[i].update(recommendations[i])

        # Allow motor sets to remain active for a short period
        time.sleep(0.5)

        # Reset the sensobs
        for sensob in self.sensobs:
            sensob.reset()
            
            
        
        ZumoButton().wait_for_press() # er nødt til å ha med denne tydeligvis
        m = Motors()
        i = 10
        while i > 0:
            m.set_value([0.2,-0.2], 1) # (speed,duration)
            #m.set_value([-0.2, 0.2], 1)
            m.forward(0.3, 1)
            i -= 1

    def controller(self):
        ZumoButton().wait_for_press()
        while True:
            self.run_one_timestep()

"""
In addition, BBCON must include a method named run one timestep, which constitutes the core BBCON
activity. It should perform (at least) the following actions on each call:
1. Update all sensobs - These updates will involve querying the relevant sensors for their values, along
with any pre-processing of those values (as described below)
2. Update all behaviors - These updates involve reading relevant sensob values and producing a motor
recommendation.

3. Invoke the arbitrator by calling arbitrator.choose action, which will choose a winning behavior and
return that behavior’s motor recommendations and halt request flag.
4. Update the motobs based on these motor recommendations. The motobs will then update the settings
of all motors.
5. Wait - This pause (in code execution) will allow the motor settings to remain active for a short period
of time, e.g., one half second, thus producing activity in the robot, such as moving forward or turning.
6. Reset the sensobs - Each sensob may need to reset itself, or its associated sensor(s), in some way.
"""
