# A* Algorithm

## Description
This project contains a UI visualization of 2D heuristic pathfinding. The A* Algorithm finds a path between user-set start and end points, balancing short path distance and quick calculations, all while avoiding obstacles.

## Installation & Use
1. Clone the repository by copying the HTTPS link into the IDE of your choice.
2. Turn diagonal pathfinding on or off at the bottom of the `environment.py` file.
3. Run the `environment.py` file.
4. Edit key path points by selecting the start (red) and end (green) menu options.
5. Add obstacles by selecting the obstacle (black) menu option.
6. Choose to visualize either the final path or the process using the visualization toggle (white) menu option.
7. Note the computation time displayed in the top right.

## Heuristic Functions
This project uses two heuristic functions for pathfinding:

- **Manhattan Distance**:
  
![Manhattan Formula](https://latex.codecogs.com/svg.latex?\text{abs}(start_x%20-%20target_x)%20+%20\text{abs}(start_y%20-%20target_y))

- **Euclidean Distance**:
   
![Euclidean Formula](https://latex.codecogs.com/svg.latex?\sqrt{(start_x%20-%20target_x)^2%20+%20(start_y%20-%20target_y)^2})

These heuristic functions are used to estimate the distance from a given point to the target:

1. Manhattan Distance is used when diagonal movement is **disabled**, providing an estimation of the distance from the target.
2. Euclidean Distance is used when diagonal movement is **enabled**, offering a more accurate calculation for diagonal movement costs.

## Resources
- ChatGPT and JetBrains AI for occasional code support and method documentation.
- PyGame for algorithm visualization and path customization.

*This README is edited by AI*
