import numpy as np

class GridEnvironment:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # 0 = Free, 1 = Wall
        self.grid = np.zeros((height, width), dtype=int)
        self.robot_radius = 2.5

    def add_wall(self, x1, y1, x2, y2, thickness):
        """Draws a wall using a simple line algorithm."""
        points = self._get_line_points(x1, y1, x2, y2)
        for px, py in points:
            # Add thickness
            for dx in range(-thickness // 2, thickness // 2 + 1):
                for dy in range(-thickness // 2, thickness // 2 + 1):
                    nx, ny = px + dx, py + dy
                    if 0 <= nx < self.width and 0 <= ny < self.height:
                        self.grid[ny, nx] = 1

    def _get_line_points(self, x1, y1, x2, y2):
        """Bresenham's line algorithm implementation."""
        points = []
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        sx = 1 if x1 < x2 else -1
        sy = 1 if y1 < y2 else -1
        err = dx - dy

        while True:
            points.append((x1, y1))
            if x1 == x2 and y1 == y2:
                break
            e2 = 2 * err
            if e2 > -dy:
                err -= dy
                x1 += sx
            if e2 < dx:
                err += dx
                y1 += sy
        return points

    def is_valid_for_robot(self, x, y):
        """Checks collision taking robot size into account."""
        margin_x = int(self.robot_radius * 1.5)
        margin_y = int(self.robot_radius * 1.5)
        
        # Check boundaries
        if not (0 <= x < self.width and 0 <= y < self.height):
            return False
            
        # Check collision with walls around the robot center
        y_min = max(0, int(y) - margin_y)
        y_max = min(self.height, int(y) + margin_y)
        x_min = max(0, int(x) - margin_x)
        x_max = min(self.width, int(x) + margin_x)

        # Efficient numpy check: if any pixel in the area is 1, return False
        if np.any(self.grid[y_min:y_max, x_min:x_max] == 1):
            return False
            
        return True