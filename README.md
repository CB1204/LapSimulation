# LapSimulation
Lap Simulation Tools for Motorsports

Run "example.py" to see the sim work. There are four different vehicle models.  
- One dimensional lookup: Simple diamond shaped g-g diagram where longitudinal acceleration is a function of lateral acceleration.  
- Two dimensional lookup: Two dimensional g-g diagram where longitudinal acceleration is a function of lateral acceleration and speed.  
- Aero Mass Tire: Simple physical model with quadratic aerodynamic downforce and drag, a mass, and a load sensitive tire.  
- General Model: A much more complicated model with suspension stiffnesses, wheels speeds. Much slower because it must optimize the vehicle state at every step.  

Run "example_tire" to see the tire model used.  
- The "Aero Mass Tire" model uses the load sensitivity behaviour from this model.  
- The "General" model uses the force vs slip shape and the friction ellipse.  

Python version 3.4.3
