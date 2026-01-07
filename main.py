import time
from grid_environment import GridEnvironment
from potential_field import PotentialField
from path_planner import PathPlanner
from planning_statistics import PlanningStatistics
from visualization import Visualizer
from performance_evaluator import PerformanceEvaluator

# --- SCENARIO 1: Vertical Maze (The Big Zigzag) ---


def run_scenario_1():
    print("\n--- Running Scenario 1:  ---")
    env = GridEnvironment(100, 100)

    # Vertical Walls
    env.add_wall(-20, 0, 20, 70, 2)
    env.add_wall(40, 30, 40, 99, 2)
    env.add_wall(60, 0, 60, 70, 2)
    env.add_wall(80, 30, 80, 99, 2)

    start = (10, 10)
    goal = (90, 90)

    # Waypoints to navigate up and down
    waypoints = [
        (10, 80), (35, 80),  # Go down and cross 1st wall
        (35, 15), (55, 15),  # Go up and cross 2nd wall
        (55, 85), (75, 85),  # Go down and cross 3rd wall
        (75, 15), (95, 15),  # Go up and cross 4th wall
        (90, 90)             # Final Goal
    ]

    return execute_planning("Scenario 1", env, start, goal, waypoints)

# --- SCENARIO 2: Room Escape (Local Minima) ---


def run_scenario_2():
    print("\n--- Running Scenario 2:  ---")
    env = GridEnvironment(100, 100)

    # Room Walls (U-Shape)
    env.add_wall(30, 30, 70, 30, 2)  # Top
    env.add_wall(30, 70, 70, 70, 2)  # Bottom
    env.add_wall(30, 30, 30, 70, 2)  # Left (Closed)

    # Right Wall with Door
    env.add_wall(70, 30, 70, 45, 2)
    env.add_wall(70, 55, 70, 70, 2)

    start = (50, 50)  # Inside
    goal = (10, 50)  # Outside Left

    # Waypoints to force escape to the right
    waypoints = [
        (65, 50),
        (85, 50),  # Exit door
        (85, 80),  # Go down
        (10, 80),  # Go left
        (10, 50)  # Go up to goal
    ]

    return execute_planning("Scenario 2", env, start, goal, waypoints)

# --- SCENARIO 3: Central Zigzag (Precision) ---


def run_scenario_3():
    print("\n--- Running Scenario 3: ")
    env = GridEnvironment(100, 100)

    # Central Walls
    env.add_wall(30, 30, 60, 30, 2)
    env.add_wall(40, 50, 70, 50, 2)
    env.add_wall(30, 70, 60, 70, 2)

    start = (50, 10)  # Top Center
    goal = (50, 90)  # Bottom Center

    # Waypoints for tight maneuvering
    waypoints = [
        (70, 25), (65, 40),  # Dodge right
        (35, 45), (35, 60),  # Dodge left
        (73, 70), (65, 80),  # Dodge right
        (50, 90)            # Back to center
    ]

    return execute_planning("Scenario 3", env, start, goal, waypoints)

# --- EXECUTION HELPER ---


def execute_planning(name, env, start, goal, waypoints):
    pf = PotentialField(env)
    planner = PathPlanner(env, pf)
    stats = PlanningStatistics(name, env.robot_radius)

    start_time = time.time()
    path = planner.plan(start, goal, waypoints)
    end_time = time.time()

    stats.calculate_metrics(path, end_time - start_time)
    stats.print_report()

    # Visualize
    viz = Visualizer(env, path, waypoints, stats)
    viz.show()

    return stats


# --- MAIN ENTRY POINT ---
if __name__ == "__main__":
    all_stats = []

    print("\n" + "="*40)
    print("      SELECT SCENARIO TO RUN")
    print("="*40)
    print("1. Scenario 1 ")
    print("2. Scenario 2 ")
    print("3. Scenario 3 ")
    print("4. Run ALL (Sequential)")
    print("="*40)

    choice = input("Enter number (1-4): ").strip()

    if choice == '1':
        all_stats.append(run_scenario_1())

    elif choice == '2':
        all_stats.append(run_scenario_2())

    elif choice == '3':
        all_stats.append(run_scenario_3())

    elif choice == '4':
        all_stats.append(run_scenario_1())
        print("\n>> Close window to continue... <<")
        all_stats.append(run_scenario_2())
        print("\n>> Close window to continue... <<")
        all_stats.append(run_scenario_3())

    else:
        print("Invalid choice! Running Scenario 1 by default...")
        all_stats.append(run_scenario_1())

    PerformanceEvaluator.print_summary_table(all_stats)
