import simpleVehicle
import numpy as np
import scipy.optimize as op


class vehicleGeneral:
    def __init__(self, upper_max_speed=100, min_curvature=1e-2):
        self.upper_max_speed = upper_max_speed
        self.min_curvature = min_curvature
        self.vehicle = simpleVehicle.Vehicle()
        self.state = None
        self.dstate = None
        self.curvature = None
        sr = -0.01
        self.xi = np.array([[5, 0.0, -.01,
                            0, 0, 0,
                            sr, sr, sr, sr]])
        sr_b = (-.075, .075)
        self.bounds = ((3, 50), (-1, 1), (-1, 1),
                       (-0.1, 0.1), (-0.1, 0.1), (-0.15, 0.15),
                       sr_b, sr_b, sr_b, sr_b)
        self.speed = None
        self.sim_dir = None
        self.ds = None

    def create_state(self, ls):
        n = ls.trackmap.curvature.shape[0]
        return State(n, maxspeed=self.upper_max_speed)

    def max_speed_calc(self, ls):
        self.state = State(1, maxspeed=self.upper_max_speed)
        self.dstate = State(1, maxspeed=self.upper_max_speed)
        k = np.fabs(ls.trackmap.curvature)
        sorted_index = np.argsort(-k)
        xi = self.xi

        for i in range(sorted_index.size):
            si = sorted_index[i]
            if k[si] > self.min_curvature:
                xi = self.solve_lim(xi, k[si])
                self.eval_state(xi)
                long_accel, lat_accel = self.accel_vel(xi)
            else:
                self.state.speed[:] = self.upper_max_speed
                self.state.AccelX[:] = 0
                ls.state_max[sorted_index[i:]] = self.state
                break

            if xi[0] < self.upper_max_speed:
                self.state.speed[:] = xi[0]
                self.state.AccelX[:] = long_accel
                ls.state_max[si] = self.state
            else:
                self.state.speed[:] = self.upper_max_speed
                self.state.AccelX[:] = 0
                ls.state_max[sorted_index[i:]] = self.state
                break

    def lim_accel(self, ls, state):
        k = ls.trackmap.curvature[[ls.counter + ls.dir]]
        self.state = state
        self.sim_dir = ls.dir
        self.ds = ls.trackmap.ds
        xi = self.eval_x()
        xi, ls.run = self.solve_max(xi, k)
        self.eval_state(xi)
        self.state.speed = xi[0]
        return self.state

    def opt_speed(self, x):
        return -x[0]

    def eval_state(self, x):
        self.state.pos_vel[:] = np.array((x[0]*np.cos(x[5]), x[0]*np.sin(x[5])))
        self.state.steer[:] = x[1]
        self.state.throttle[:] = x[2]
        self.state.angle[:] = np.hstack((x[3:5], 0))
        self.state.angle_vel[:, 2] = x[0]*self.curvature

        x_vel = self.state.pos_vel[:, 0] - self.state.angle_vel[:, 2] * self.vehicle.Y
        y_vel = self.state.pos_vel[:, 1] + self.state.angle_vel[:, 2] * self.vehicle.X
        front = np.hstack((self.state.steer, self.state.steer))
        rear = np.zeros(front.shape)
        theta = np.hstack((front, rear))
        x_dir_t = np.cos(theta)
        y_dir_t = np.sin(theta)
        self.state.wheel_speed[:] = (1 + x[6:]) * (x_vel * x_dir_t + y_vel * y_dir_t) / 0.25
        self.dstate = self.vehicle.state_derivative(self.state, self.dstate)

    def eval_x(self):
        # x = [speed, steer, throttle,
        #      angle(3),
        #      wheel_speed(4)]
        front = np.hstack((self.state.steer, self.state.steer))
        rear = np.zeros(front.shape)
        theta = np.hstack((front, rear))
        speed = np.sqrt(np.sum(self.state.pos_vel**2, axis=1, keepdims=True))
        x_vel = self.state.pos_vel[:, 0] - self.state.angle_vel[:, 2] * self.vehicle.Y
        y_vel = self.state.pos_vel[:, 1] + self.state.angle_vel[:, 2] * self.vehicle.X
        x_vel_t = 0.25 * self.state.wheel_speed * np.cos(theta)
        y_vel_t = 0.25 * self.state.wheel_speed * np.sin(theta)
        slip_ratio = (x_vel_t * x_vel_t + y_vel_t * y_vel_t) /\
                     (x_vel_t * x_vel + y_vel_t * y_vel) - 1
        beta = np.arctan2(self.state.pos_vel[:, [1]], self.state.pos_vel[:, [0]])
        return np.hstack((speed, self.state.steer, self.state.throttle, self.state.angle[:, 0:2], beta, slip_ratio))

    def accel_vel(self, x):
        vel_tangent = self.state.pos_vel/x[0]
        vel_normal = np.hstack((-vel_tangent[:, [1]], vel_tangent[:, [0]]))
        accel_tangent = np.sum(self.dstate.pos_vel * vel_tangent)
        accel_normal = np.sum(self.dstate.pos_vel * vel_normal)
        return accel_tangent, accel_normal

    def const_lim(self, x):
        self.eval_state(x)
        long_accel, lat_accel = self.accel_vel(x)
        lat_accel_const = self.curvature * x[0] ** 2 - lat_accel
        return np.hstack((lat_accel_const,
                          self.dstate.angle_vel[0, :],
                          self.dstate.wheel_speed[0, :]))

    def solve_lim(self, xi, k):
        self.curvature = k
        cons = ({'type': 'eq',
                 'fun': self.const_lim,
                 'jac': None})
        tol = 1e-12
        res = op.minimize(self.opt_speed, xi,
                          jac=None,
                          bounds=self.bounds,
                          constraints=cons,
                          tol=tol,
                          method='SLSQP',
                          options={'disp': False})
        return res.x

    def const_max(self, x):
        self.eval_state(x)
        long_accel, lat_accel = self.accel_vel(x)
        long_accel_const = self.sim_dir * (x[0] ** 2 - self.speed[0] ** 2) / (2 * self.ds) - long_accel
        lat_accel_const = self.curvature * x[0] ** 2 - lat_accel
        return np.hstack((long_accel_const,
                          lat_accel_const,
                          self.dstate.angle_vel[0, :],
                          self.dstate.wheel_speed[0, :]))

    def solve_max(self, xi, k):
        self.curvature = k
        # self.speed = xi[:, 0]
        self.speed = xi[:, [0]]
        xi[:, [1]] *= 0.75
        xi[:, 6:] = 0.0
        tol = 1e-8
        cons = ({'type': 'eq',
                 'fun': self.const_max,
                 'jac': None})
        res = op.minimize(self.opt_speed, xi,
                          jac=None,
                          bounds=self.bounds,
                          constraints=cons,
                          tol=tol,
                          method='SLSQP',
                          options={'disp': False,
                                   'eps': 2e-7})
        run = res.success & (np.max(np.abs(self.const_max(res.x)))<tol)
        return res.x, run


class State(simpleVehicle.State):
    def __init__(self, n, maxspeed=100):
        super(State, self).__init__(n)
        self.speed = np.ones((n, 1)) * maxspeed
        self.AccelX = np.zeros((n, 1))
