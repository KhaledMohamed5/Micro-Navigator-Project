import matplotlib.pyplot as plt
import matplotlib.patches as patches
import matplotlib.animation as animation


class Animator:
    def __init__(self, env, path, robot_radius, waypoints):
        self.env = env
        self.path = path
        self.waypoints = waypoints
        # Speed up animation if path is long
        if len(path) > 600:
            self.path = path[::3]

        self.r_width = robot_radius * 2.8
        self.r_height = robot_radius * 1.4
        self.fig, self.ax = plt.subplots(figsize=(9, 9))
        self.robot_patch = None
        self.path_line = None

    def update(self, frame):
        if frame < len(self.path):
            pos = self.path[frame]
            cx = pos[0] - (self.r_width/2)
            cy = pos[1] - (self.r_height/2)
            self.robot_patch.set_xy((cx, cy))

            px = [p[0] for p in self.path[:frame+1]]
            py = [p[1] for p in self.path[:frame+1]]
            self.path_line.set_data(px, py)
        return self.robot_patch, self.path_line

    def animate(self):
        self.ax.set_xlim(0, self.env.width)
        self.ax.set_ylim(0, self.env.height)
        self.ax.invert_yaxis()
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.3)
        self.ax.set_title("Micro_Navigator")

        # Draw walls
        g = self.env.get_grid()
        for i in range(self.env.height):
            for j in range(self.env.width):
                if g[i, j] == 1:
                    self.ax.add_patch(patches.Rectangle(
                        (j, i), 1, 1, fc='#2c3e50'))

        # Draw waypoints (light blue)
        for wp in self.waypoints:
            self.ax.add_patch(patches.Circle(wp, 0.8, fc='#3498db', alpha=0.5))

        # Start and End
        s, e = self.path[0], self.path[-1]
        self.ax.add_patch(patches.Circle(s, 1.5, fc='#27ae60'))
        self.ax.text(s[0], s[1], "S", color='white', ha='center')
        self.ax.add_patch(patches.Circle(e, 1.5, fc='#e74c3c'))
        self.ax.text(e[0], e[1], "G", color='white', ha='center')

        start_pos = self.path[0]
        self.robot_patch = patches.Rectangle(
            (start_pos[0]-self.r_width/2, start_pos[1]-self.r_height/2),
            self.r_width, self.r_height, fc='#2980b9', ec='white'
        )
        self.ax.add_patch(self.robot_patch)
        self.path_line, = self.ax.plot([], [], color='orange', lw=2)

        anim = animation.FuncAnimation(
            self.fig, self.update, frames=len(self.path), interval=100, blit=True)
        plt.show()
