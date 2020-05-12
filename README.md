# Agent-Based Model for Assessing the Impact of Interventions on Covid-19 Pandemic: Dakar, Senegal

# Purpose 
The model was designed to explore the impact of interventions to control the spread of covid-19. Specifically, we investigate the combined effects of control measures such as 

* efficiency of contact tracing for treatments at hospital, i.e. capacity of existing health systems.
* adherence to recommendations, i.e. hygiene and social distancing.
* of human behavior regarding risk to life. 
	
on the progression of the disease in terms of the number of infections.


# Overview 
The model has three kinds of entities: individuals, government-official, and the environment. 

### Environment
* This constitutes the drivable public streets network and paths that pedestrians can use. 
* The street network is a graph that stores the paths as edges and junctions as nodes. 
* The junctions are characterized by their location (x and y coordinates). 
* The street network also has buildings or specific points-of-interest (POIs), i.e. marketplaces.
* These points-of-interest (POIs) are characterized by their location as polygons.

### Individuals
* They are characterized by their location (x and y coordinates).
* Health status: susceptible, exposed, asymptomatic, and symptomatic.
* Risk to life: how one values own life influencing decision to move.
* Social network:  list of other-individuals connected to an individual.
* Social radius: a measure of adherence to hygiene and social distancing.

### Government-official  
* They identify infectious individuals for treatments at hospitals. 
* Characterized by the efficiency of contact tracing: the proportion of infectious individuals traced for treatment at hospital. 
* The model time step is a day. The length of one-time step depends on the size of the individuals (minus those under treatments at hospital). Simulations last for 100 days.


# Design: Processes and Scheduling
The model includes the four sub-models which are executed in this order at each time step (i) decision-to-move, (ii) moving-to-destination, (iii) interaction-with-others, and (iv) quarantine-by-officials. 

In each updating, 1 / (8.n) of a unit length of time passes by, where n is the number of individuals (minus those under treatment at hospital) at the time of updating. Therefore, each individual is updated 8 times, on average, in one-unit length of simulated time reflecting 8 hours of activeness per day for each individual.


# Submodels

### Social-network 
* The social network follows a small-world social network (Watts and Strogatz, 1998). 
* Small-world network is a graph with many nodes forming cliques (clusters of nodes which are well connected), and fewnodes   that ‘reach across’ to other cliques. 
* It is an important network structure in the study of human systems because it fits many real world networks (both 	physical and social) very well.  
	#### Pseudocode for social network
	```
	1. Each individual connects to its 2-nearest neighbors and then subject to random rewiring. 
	2. In each rewiring event, an individual is randomly selected and drops one of its neighbors randomly. 
	3. It then selects a new  neighbor that is randomly chosen from the general population (excluding those to which it was already connected). 
	```
	<p align="center">
	<img src="Fig1.png" width="650">
	<br>      
	<em>Fig 1: An example of small world network among for the individuals.</em>   
   	</p>
  

 ### Decision-to-move
  * The decision to move (or not-move) is controlled by the parameter _risk-life_. This is a random number from a uniform           distribution between a minimum (0.0) and maximum (1.0).  
  * A decreasing _risk-life_ (i.e. decreasing the maximum) produce a distribution of individuals who are less probable to take       risk (and vice-versa). 

     #### Pseudocode for Decision-to-move
     
     ```
     If random uniform (0.0, 1.0) > average (self risk-life + random neighbor risk-life ) 
                < move >
     else 
              <do not move>
    ```
  * With this setting, individuals with a lower _risk-life_ and having other-individuals with lower risk-life in their social        network are more likely to move (and vice versa).
  * When an individual decides to move, it randomly selects a point-of-interest as its destination.
  * Once the destination has been reached, an individual chooses a new random destination.
  
  
### Moving-to-destination
 * Individuals find the optimal route (in terms of distance) from its current location to the destination using Dijkstra          algorithm (Dijkstra, 1959). 
 * Dijkstra algorithm is used for finding the shortest path from an origin to a destination that minimizes a cost (eg. in        terms of time, distance or financial cost). 
 * Individuals move along the street paths and covers one node in each model iteration of the day. 

     #### Pseudocode for Dijkstra Algorithm
	```
	Let distance of start node from start node be zero.
	Let distance of all other nodes from start node be infinity.
	Repeat
		Visit the unvisited node with the smallest known distance from the start node.
		For the current node, examine its unvisited neighbors.
	  	For the current node, calculate distance of each neighbor from start node.
          	If the calculated distance of a node is less than the known distance, update the shortest distance.
	  	Update the previous node of each of the updated distances.
	  	Add the current node to the list of visited nodes.
	Until all nodes are visited
	```
  
  
### Interaction-with-others
  * Individuals only interact with other-individuals within a distance _social-radius_ from itself. 
  * The epidemic is represented using the SEIRS (Susceptible - Exposed - Infectious - Recovered - Susceptible). 
  
  <p align="center">
   <img src="Fig2.png" width="650">
   <br>      
      <em>Fig 2: The SEIR model</em>   
  </p>  
  
  	
   #### Pseudocode for Interaction and progression of disease

   1. If an infectious (i.e. symptomatic or asymptomatic) individual is located within the social-radius, a susceptible
	individual becomes exposed with probability prob-exposed, i.e. the individual is infected but not infectious. 
   2. After an incubation duration of incubation-period days, an exposed individual transition to infectious and becomes
	asymptomatic with probability prob-infection, else symptomatic. 
   3. Asymptomatic individuals recover and becomes susceptible again (i.e. recovery does not confer lifelong immunity 	    after asymptomatic-recovery days. The recovered individual remains immune for recovery-susceptible days before becomes susceptible. 

 
 ### Quaranine-by-officials
 * Symptomatic individuals are removed from the general population and treated at hospital with probability _efficiency-           contact-tracing_. 
 * After _recovery-symptomatic_ days at the hospital, they either recover (and returned to the general population) or die. 
 * The probability of recovery is dependent on the number of individuals being treated at the hospital, i.e. recovery             becomes less likely as the number of individuals at the hospitals increases. 
 * This setting reflects that the health-care quality becomes poorer as the health system becomes over-capacited.

      #### Pseudocode of contact tracing to treatment at hospital
      
 	```
	
	If infectious and symptomatic and random (0,1) < efficiency-contact-tracing
		If random (0,1) < 1 – (nr. of individuals at hospital / carrying capacity of hospital)
			recover and returned to the general population
		else
			after 14 days, immunity dies-out and becomes susceptible 

	```

### Initialization 
The model is initialized with a number of susceptible and infectious (symptomatic and symptomatic) individuals. The other parameters initialized for individuals includes, _prob-exposed_, _incubation-period-exposed_, _prob-infection_, _days-recovery-asymptomatic_, _recovery-period_, _risk-life_, _social-radius_ ,_days-recovery-symptomatic_, activeness-per-day, and hospital-capacity. The government official is initialized with _efficiency-contact-tracing_.

### Output
A stack area plots and csv file showing the number of exposed, susceptible, asymptomatic, and symptomatic individuals.

<p align="center">
   <img src="Fig3.png" width="750">
   <br>      
      <em>Fig 3: Snapshot of model interface.</em>   
  </p>
