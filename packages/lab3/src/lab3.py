#!/usr/bin/env python3

import rospy
from std_msgs.msg import Float32, String
from duckietown_msgs.msg import LanePose, Twist2DStamped, FSMState
from pid import PID

class Lab3:
    def __init__(self):

        # homework 5 publishes to the control input for vehicle_dynamics to read
        self.pub = rospy.Publisher("car_cmd_switch_node/cmd", Twist2DStamped, queue_size=10)

        # tune pid values below
        self.pid_1 = PID(p=0, i=0, d=0)
        self.pid_2 = PID(p=0, i=0, d=0)
        self.my_msg = Twist2DStamped()
        self.my_msg.v = 0.15 # velocity

        # receive the phi and d to update PID controller and movement
        rospy.Subscriber("lane_filter_node/lane_pose", LanePose, self.get_new_update)

        # receive command from joystick
        rospy.Subscriber("fsm_node/mode", FSMState, self.callbackFSM)


    # call PID class control calculation when receiving error message
    def get_new_update(self, pose):
        # use first PID controller on d
        omega_1 = self.pid_1.calc_control(pose.d, 0.001)

        # use second PID controller on phi
        omega_2 = self.pid_2.calc_control(pose.phi, 0.001)


        # add up omega values
        self.my_msg.omega = omega_1 + omega_2
        rospy.logwarn("Final Omega: %f", self.my_msg.omega)

        # sends new controller message to system 
        self.pub.publish(self.my_msg)
    def callbackFSM(self, keypressed):
        if (keypressed.state == "LANE_FOLLOWING"):
            rospy.logwarn("Key pressed: %s", keypressed.state)



if __name__ == '__main__':

    rospy.init_node('lab3_node')
    # sleep allows user to run rqt_plot
    rospy.sleep(5)
    Lab3()

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

