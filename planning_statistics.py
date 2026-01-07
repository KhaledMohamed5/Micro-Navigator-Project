class PlanningStatistics:
    def __init__(self, scenario_name, robot_size):
        self.scenario_name = scenario_name
        self.robot_size = robot_size
        self.planning_time_ms = 0
        self.path_length = 0
        self.num_steps = 0
        self.success = False

    def calculate_metrics(self, path, time_taken_sec):
        self.planning_time_ms = int(time_taken_sec * 1000)
        self.num_steps = len(path)
        self.success = len(path) > 0

        length = 0
        for i in range(len(path) - 1):
            p1 = path[i]
            p2 = path[i+1]
            dist = ((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)**0.5
            length += dist
        self.path_length = length

    def print_report(self):
        print("="*60)
        print(f"  PLANNING STATISTICS - {self.scenario_name}")
        print("="*60)
        print(f"Status:        {'SUCCESS' if self.success else 'FAILED'}")
        print(f"Time:          {self.planning_time_ms} ms")
        print(f"Path Length:   {self.path_length:.2f} units")
        print(f"Steps:         {self.num_steps}")
        print("="*60)
