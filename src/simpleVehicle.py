import numpy as np
from simpleTire import Tire
from simpleEngine import Engine
from simpleBrakes import Brakes
from sliceable import Sliceable


class Vehicle:
    def __init__(self,
                 gravity=9.81,
                 mass=350,
                 rg=np.array([0.5, 0.5, 0.75]),
                 wheelbase=1.6,
                 track=np.array([1, 1]),
                 CGbal=.5,
                 CGz=0.3,
                 WTlat_bal=0.5,
                 Kroll=20.0e3,
                 Kpitch=30.0e3,
                 tireF=Tire(),
                 tireR=Tire(),
                 mass_t=5,
                 rg_t=.2,
                 aero=None,
                 engine=Engine(),
                 brakes=Brakes()):
        o = np.array([1, 1])
        os = np.array([1, -1])
        self.gravity = gravity
        self.mass = mass
        self.rg = rg
        self.wheelbase = wheelbase
        self.track = track
        self.CGbal = CGbal
        self.CGz = CGz
        self.X = self.wheelbase * np.concatenate(((1 - self.CGbal) * o, -self.CGbal * o))
        self.Y = np.concatenate((self.track[0] * os, self.track[1] * os)) / 2
        self.WTlat_bal = WTlat_bal
        self.Kroll = Kroll
        self.Kpitch = Kpitch

        WTlatDistFront = -self.WTlat_bal * os / self.track[0]
        WTlatGainRear = -(1 - self.WTlat_bal) * os / self.track[1]
        self.WTlatDist = np.concatenate((WTlatDistFront, WTlatGainRear))

        WTlongDistFront = o / self.wheelbase
        WTlongDistRear = -o / self.wheelbase
        self.WTlongDist = np.concatenate((WTlongDistFront, WTlongDistRear)) / 4

        self.fz_static = self.gravity * self.mass * np.concatenate((self.CGbal * o, (1 - self.CGbal) * o)) / 2

        self.tireF = tireF
        self.tireR = tireR
        self.mass_t = mass_t
        self.rg_t = rg_t
        self.aero = aero
        self.engine = engine
        self.brakes = brakes

    def create_state(self, n):
        return State(n)

    def state_derivative(self, state, dstate):
        wt_lat = state.angle[:, [0]] * self.WTlatDist * self.Kroll
        wt_long = state.angle[:, [1]] * self.WTlongDist * self.Kpitch
        fz = self.fz_static + wt_lat + wt_long

        theta = parallel_steer(state.steer)
        [sr, sa] = self.calculate_slip(theta, state)
        [fxf, fyf] = self.tireF.force(sr[:, :2], sa[:, :2], fz[:, :2])
        [fxr, fyr] = self.tireR.force(sr[:, 2:], sa[:, 2:], fz[:, 2:])
        fx_t = np.hstack((fxf, fxr))
        fy_t = np.hstack((fyf, fyr))

        rear_wheel_speed = state.wheel_speed[:, 2:].mean()
        if state.throttle >= 0:
            torque_engine = self.engine.torque(rear_wheel_speed * .25, state.throttle) * .25
            torque_brakes = 0
        else:
            torque_engine = 0
            torque_brakes = self.brakes.torque(state.throttle)

        [fx, fy, mx, my, mz] = tire2body(self.X, self.Y, fx_t, fy_t, fz, theta)
        longAccel = fx / self.mass
        latAccel = fy / self.mass
        rollAccel = (mx - (-1) * (latAccel * self.mass) * self.CGz) / (self.mass * self.rg[0] ** 2)
        pitchAccel = (my - (longAccel * self.mass) * self.CGz) / (self.mass * self.rg[1] ** 2)
        yawAccel = mz / (self.mass * self.rg[2] ** 2)
        wheelAccel = (-0.25 * fx_t + np.array([0, 0, 0.5, 0.5]) * torque_engine + torque_brakes) / \
                     (self.mass_t * self.rg_t ** 2)

        dstate.pos = state.pos_vel
        dstate.pos_vel = np.hstack((longAccel, latAccel))
        dstate.angle = state.angle_vel
        dstate.angle_vel = np.hstack((rollAccel, pitchAccel, yawAccel))
        dstate.wheel_speed = wheelAccel

        return dstate

    def calculate_slip(self, theta, state):
        x_vel = state.pos_vel[:, 0] - state.angle_vel[:, 2] * self.Y
        y_vel = state.pos_vel[:, 1] + state.angle_vel[:, 2] * self.X
        x_vel_t = 0.25 * state.wheel_speed * np.cos(theta)
        y_vel_t = 0.25 * state.wheel_speed * np.sin(theta)
        slip_angle = np.arctan2(y_vel, x_vel) - np.arctan2(y_vel_t, x_vel_t)
        slip_ratio = (x_vel_t * x_vel_t + y_vel_t * y_vel_t) /\
                     (x_vel_t * x_vel + y_vel_t * y_vel) - 1
        return [slip_ratio, slip_angle]

    def integrate_state(self, state, state_derivative, dt):
        state.pos = state.pos_vel * dt
        state.pos_vel = state_derivative.pos_accel * dt
        state.angle = state.angle_vel * dt
        state.angle_vel = state_derivative.angle_accel * dt


def tire2body(x, y, fx_t, fy_t, fz, theta):
    st = np.sin(theta)
    ct = np.cos(theta)
    fx_b = np.sum(fx_t * ct - fy_t * st, axis=1, keepdims=True)
    fy_b = np.sum(fx_t * st + fy_t * ct, axis=1, keepdims=True)
    mx_b = np.sum(y * fz, axis=1, keepdims=True)
    my_b = np.sum(-x * fz, axis=1, keepdims=True)
    mz_b = np.sum(x * fx_t * st - y * fx_t * ct + y * fy_t * st + x * fy_t * ct, axis=1, keepdims=True)
    return [fx_b, fy_b, mx_b, my_b, mz_b]


def parallel_steer(steer):
    front = np.hstack((steer, steer))
    rear = np.zeros(front.shape)
    theta = np.hstack((front, rear))
    return theta


# class Sliceable:
#     def __getitem__(self, key):
#         first = True
#         for v in vars(self):
#             if first is True:
#                 s = getattr(self, v)[key].shape
#                 if np.size(s) == 2:
#                     n = s[0]
#                 else:
#                     n = 1
#
#                 sliced_state = self.__class__(n)
#                 first = False
#
#             getattr(sliced_state, v)[:] = getattr(self, v)[key]
#
#         return sliced_state
#
#     def __setitem__(self, sliced, sliced_state):
#         for v in vars(self):
#             getattr(self, v)[sliced] = getattr(sliced_state, v)


class State(Sliceable):
    def __init__(self, n):
        self.steer = np.zeros((n, 1))
        self.throttle = np.zeros((n, 1))
        self.pos = np.zeros((n, 2))
        self.pos_vel = np.zeros((n, 2))
        self.angle = np.zeros((n, 3))
        self.angle_vel = np.zeros((n, 3))
        self.wheel_speed = np.zeros((n, 4))


def rotation2d(angle):
    s = np.sin(angle)
    c = np.cos(angle)
    return np.matrix([[c, -s], [s, c]])
