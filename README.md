# A* Algorithm

## Description
This project contains a UI visualization of 2D heuristic pathfinding. The A* Algorithm then finds a path between user-set start and end points, balancing short path distance and quick calculations, all while avoiding obstacles.

## Installation & Use
1) Clone the repository by copying the HTTPS link into the IDE of your choice
2) Turn diagonal pathfinding on and off at the bottom of the enviroment.py file
3) Run the enviroment.py file
4) Edit key path points by selecting the start (red) and end (green) menu options
5) Add obstacles by selecting the obstacle (black) menu option
6) Choose to visualize either the final path, or the proccess, using the visualization toggle (white) menu option
7) Notice the computation time highlighted in the top right

## Heuristic Functions
This project uses two heuristic functions in order to pathfind.

For pathfinding with diagonal movement disabled, the algorithm uses manhattan distance in order to pathfinder (ie: abs(start_x - target_x) + abs(start_y - target_y)). This estimates the distance from the target from a particular point.

For pathfinding with diagonal movement enabled, the algorithm uses euclidian distance in order to pathfind (ie: sqrt((start_x - target_x)^2 + (start_y - target_y)^2)). This more accurately relfects the diagonal movement costs than the manhattan distance.

## Resources
- ChatGPT and JetBrains AI for occational code support and method documenation
- PyGame for algorithm visualization and path customization
