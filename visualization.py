import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.animation import FuncAnimation
import numpy as np


class Visualizer:
    def __init__(self, env, path, waypoints, stats):
        self.env = env
        self.path = path
        self.waypoints = waypoints
        self.stats = stats

        # Setup Figure with modern styling
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.fig.patch.set_facecolor('#F0F2F5')  # Background color outside
        self.ax.set_facecolor('#FFFFFF')        # Map background

        # Colors
        self.colors = {
            'wall': '#2C3E50',       # Dark Blue-Grey
            'grid': '#E1E5EB',       # Light Grey
            'path': '#FF8C00',       # Orange
            'robot': '#3498DB',      # Blue
            'waypoint': '#16A085',   # Teal
            'start': '#2ECC71',      # Green
            'goal': '#E74C3C'        # Red
        }

    def setup_plot(self):
        self.ax.set_xlim(0, self.env.width)
        # Invert Y to match Java coordinate system (0 is top)
        self.ax.set_ylim(self.env.height, 0)
        self.ax.set_aspect('equal')
        self.ax.set_title(
            f"Micronavigator - {self.stats.scenario_name}", fontsize=14, fontweight='bold', pad=15)

        # 1. Draw Grid
        self.ax.grid(color=self.colors['grid'], linestyle='-', linewidth=1)
        self.ax.set_xticks(np.arange(0, self.env.width, 10))
        self.ax.set_yticks(np.arange(0, self.env.height, 10))
        self.ax.set_xticklabels([])
        self.ax.set_yticklabels([])

        # 2. Draw Walls
        wall_y, wall_x = np.where(self.env.grid == 1)
        # Using scatter for walls is faster than drawing individual rectangles for Python
        self.ax.scatter(
            wall_x, wall_y, c=self.colors['wall'], marker='s', s=15, edgecolors='none')

        # 3. Draw Waypoints
        for wp in self.waypoints:
            circle = patches.Circle(
                wp, radius=1.5, color=self.colors['waypoint'], alpha=0.6)
            self.ax.add_patch(circle)

        # 4. Start & Goal
        if self.path:
            self.ax.text(self.path[0][0], self.path[0][1], 'S',
                         color=self.colors['start'], fontsize=12, fontweight='bold', ha='center')
            self.ax.text(self.path[-1][0], self.path[-1][1], 'G',
                         color=self.colors['goal'], fontsize=12, fontweight='bold', ha='center')

        # Elements to update in animation
        self.path_line, = self.ax.plot(
            [], [], color=self.colors['path'], linewidth=2.5, alpha=0.8)

        # Robot as a "Rounded" shape (FancyBboxPatch)
        self.robot_patch = patches.FancyBboxPatch(
            (0, 0), self.env.robot_radius*2, self.env.robot_radius*1.5,
            boxstyle="round,pad=0.2", fc=self.colors['robot'], ec='white', lw=1.5
        )
        self.ax.add_patch(self.robot_patch)

        # Footer Text
        self.info_text = self.ax.text(
            2, self.env.height - 2, "",
            fontsize=10, bbox=dict(facecolor='white', alpha=0.8, edgecolor='none')
        )

    def update(self, frame):
        # Speed up: Skip frames if path is long
        idx = min(frame * 5, len(self.path) - 1)

        # Update Path
        current_path = np.array(self.path[:idx+1])
        if len(current_path) > 0:
            self.path_line.set_data(current_path[:, 0], current_path[:, 1])

        # Update Robot Position
        pos = self.path[idx]
        # Center the patch
        self.robot_patch.set_x(pos[0] - self.env.robot_radius)
        self.robot_patch.set_y(pos[1] - self.env.robot_radius*0.75)

        # Update Text
        self.info_text.set_text(
            f"Step: {idx}/{len(self.path)} | Length: {self.stats.path_length:.1f}"
        )
        return self.path_line, self.robot_patch, self.info_text

    def show(self):
        self.setup_plot()
        anim = FuncAnimation(
            self.fig, self.update,
            frames=int(len(self.path)/5) + 5,
            interval=200, blit=True, repeat=False
        )
        plt.show()
