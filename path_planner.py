import numpy as np
import random


class PathPlanner:
    def __init__(self, env, pf):
        self.env = env
        self.pf = pf

    def plan(self, start, goal, waypoints):
        path = [start]
        all_goals = waypoints + [goal]

        curr = np.array(start, dtype=float)
        prev_move = np.array([0.0, 0.0])
        momentum = 0.6  # Smoothness factor

        print("Starting path planning...")

        for target in all_goals:
            print(f"Targeting waypoint: {target}")
            self.pf.set_temp_goal(target)

            step_limit = 3000
            for _ in range(step_limit):
                dist = np.hypot(curr[0] - target[0], curr[1] - target[1])
                if dist < 3.0:
                    break

                # Get Force
                fx, fy = self.pf.get_gradient(curr[0], curr[1])

                # Normalize force
                mag = np.hypot(fx, fy)
                if mag > 0:
                    fx, fy = fx / mag, fy / mag

                # Calculate step with momentum
                step_val = 0.5
                tdx = fx * step_val
                tdy = fy * step_val

                fdx = (momentum * prev_move[0]) + ((1 - momentum) * tdx)
                fdy = (momentum * prev_move[1]) + ((1 - momentum) * tdy)

                nx = curr[0] + fdx
                ny = curr[1] + fdy

                # Collision check & Random walk if stuck
                if not self.env.is_valid_for_robot(nx, ny):
                    nx = curr[0] + (random.random() - 0.5)
                    ny = curr[1] + (random.random() - 0.5)

                curr = np.array([nx, ny])
                path.append(tuple(curr))
                prev_move = np.array([fdx, fdy])

        print(f"Planning complete. Total steps: {len(path)}")
        return path
