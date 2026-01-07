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
