# Trip Extraction

There are 5 roles to extract the trips from waypoints:
- A vehicle may occasionally sends GPS updates, even if it not moving
- The precision of GPS positioning is not accurate on meter-level. Distances 
between waypoints < 15 meters should be ignored
- Especially within cities, the GPS position might "jump", due to bad reception
caused by tunnels, underground garages or reflections on houses etc.
- A trip should be considered as started, as soon as the vehicle starts moving 
- A trip should be considered as ended, if the vehicle does not move for 
longer than 3 minutes


#Run

To run the project, in the root of projects, call:

    python extract_trips.py file_name
   
where file_name is the name of the file which contains waypoints.
The file should be placed at the root of project.
   
   