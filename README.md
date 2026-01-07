# 🧭 Micronavigator: Hybrid Path Planning System

**Autonomous Mobile Robot Navigation using Artificial Potential Fields (APF) & Global Waypoints.**

## 📝 Overview
**Micronavigator** is a Python-based simulation for autonomous robot navigation in a 2D grid environment ($100 \times 100$). It implements a **Hybrid Approach** combining:
1.  **Artificial Potential Fields (APF):** For reactive obstacle avoidance.
2.  **Global Waypoint Planner:** To solve the "Local Minima" problem common in standard APF.

The system ensures smooth, collision-free paths using momentum-based gradient descent and visualizes the results in real-time.

## ✨ Key Features
* **🚫 Obstacle Avoidance:** Uses repulsive potential forces to keep the robot away from walls.
* **✅ Solves Local Minima:** Uses a sequence of global waypoints to guide the robot out of traps (e.g., U-shaped obstacles).
* **🌊 Smooth Movement:** Implements a momentum factor (0.1) to prevent jerky movements and oscillations.
* **📊 Real-time Visualization:** Animated path planning using Matplotlib.
* **⚡ High Performance:** Planning time < 150ms with 100% success rate across test scenarios.

## 🛠️ Technology Stack
* **Language:** Python 3.11
* **Libraries:**
    * `NumPy`: For vectorization and mathematical computations.
    * `Matplotlib`: For rendering and animation.
    * `Time`: For performance tracking.

## 📂 Project Structure
```text
micronavigator/
├── main.py                   # Entry point of the application
├── grid_environment.py       # Manages occupancy grid & collision detection
├── potential_field.py        # Calculates Attractive & Repulsive forces
├── path_planner.py           # Executes gradient descent with momentum
├── visualization.py          # Animation and rendering
├── planning_statistics.py    # Performance tracking
└── performance_evaluator.py  # Multi-scenario testing


Installation & Usage
1. Clone the repository:
git clone [https://github.com/yourusername/micronavigator.git](https://github.com/yourusername/micronavigator.git)
cd micronavigator
2.Install dependencies: The project requires NumPy for calculations and Matplotlib for visualization.
pip install numpy matplotlib
3. Run the simulation: Start the main application entry point.

 Algorithm Details1.
1. Artificial Potential Fields (APF)The robot moves based on the resultant force vector $F_{total} = F_{att} + F_{rep}$.
   Attractive Force: Pulls the robot towards the goal using the equation $U_{att} = k_{att} \times distance$ with a gain of $k_{att} = 1.5$.
   Repulsive Force: Pushes the robot away from obstacles using a repulsive gain $k_{rep} = 50.0$ and an influence range of $d_0 = 5.0$.2.
2. Waypoint Navigation (Hybrid Approach)
   To escape "Local Minima" (where attractive and repulsive forces cancel out), the Global Planner breaks the path into sub-goals (waypoints). The robot pursues one waypoint at a time until       the final goal is reached.

📈 ResultsThe
system was tested on 3 complex scenarios with a 100% Success Rate.
ScenarioPath LengthPlanning TimeStatus1. Narrow Gaps892.45145 ms✅ SUCCESS
2. U-Shape Trap 645.3298 ms
✅ SUCCESS3. Staggered Walls723.18112 ms✅ SUCCESS
