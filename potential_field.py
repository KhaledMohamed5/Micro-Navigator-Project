import numpy as np


class PotentialField:
    def __init__(self, env):
        self.env = env
        self.attr_gain = 1.0
        self.rep_gain = 100.0
        self.rep_range = 5.0
        self.current_goal = None
        self.obstacles = []
        self._cache_obstacles()

    def set_parameters(self, attr, rep, rng):
        self.attr_gain = attr
        self.rep_gain = rep
        self.rep_range = rng

    def set_temp_goal(self, goal):
        self.current_goal = goal

    def _cache_obstacles(self):
        """Find all wall pixels once to speed up calculation."""
        ys, xs = np.where(self.env.grid == 1)
        self.obstacles = np.column_stack((xs, ys))

    def get_gradient(self, x, y):
        """Calculates the force vector at position (x,y)."""
        if self.current_goal is None:
            return 0, 0

        # 1. Attractive Force
        dx = self.current_goal[0] - x
        dy = self.current_goal[1] - y
        dist_goal = np.hypot(dx, dy)

        fx = self.attr_gain * dx / (dist_goal if dist_goal > 0 else 1)
        fy = self.attr_gain * dy / (dist_goal if dist_goal > 0 else 1)

        # 2. Repulsive Force (Local calculation for speed)
        # Only check obstacles close to the robot to save time
        if len(self.obstacles) > 0:
            # Calculate distances to all obstacle points
            dists = np.hypot(
                self.obstacles[:, 0] - x, self.obstacles[:, 1] - y)

            # Filter relevant obstacles within range
            mask = (dists <= self.rep_range) & (dists > 0)
            nearby_obs = self.obstacles[mask]
            nearby_dists = dists[mask]

            if len(nearby_obs) > 0:
                rep_factor = self.rep_gain * \
                    ((1.0 / nearby_dists) - (1.0 / self.rep_range)) * \
                    (1.0 / nearby_dists**2)
                rep_dx = (x - nearby_obs[:, 0]) / nearby_dists
                rep_dy = (y - nearby_obs[:, 1]) / nearby_dists

                fx += np.sum(rep_factor * rep_dx)
                fy += np.sum(rep_factor * rep_dy)

        return fx, fy
