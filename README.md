# Agent-Based Model for Assessing the Impact of Interventions on Covid-19 Pandemic: Dakar, Senegal
Designed to explore the impact of interventions to control the spread of covid-19. 

# Purpose 
The model was designed to explore the impact of interventions to control the spread of covid-19. Specifically, we investigate the combined effects of control measures such as 
  * efficiency of contact tracing for treatments at hospital, i.e. capacity of existing health systems.
  * to recommendations, i.e. hygiene and social distancing.
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
* Characterized by the efficiency of contact tracing: the proportion of infectious individuals traced for treatment at hospital (reflecting the capacity of health systems). 
* The model time step is a day. The length of one-time step depends on the size of the individuals (minus those under treatments at hospital). Simulations last for 100 days.


# Design: Agents, Environment, and Processes 
The model includes the four sub-models which are executed in this order at each time step (i) decision-to-move, (ii) moving-to-destination, (iii) interaction-with-others, and (iv) quarantine-by-officials. 

In each updating, 1 / (8*n) of a unit length of time passes by, where n is the number of individuals (minus those under treatment at hospital) at the time of updating. Therefore, each individual is updated 8 times, on average, in one-unit length of simulated time reflecting 8 hours of activeness per day for each individual.


# Submodels

### Social-network 
 * The social network follows a small-world social network (Watts and Strogatz, 1998). 
 * Small-world network is a graph with many nodes forming cliques (clusters of nodes which are well connected), and few nodes   that ‘reach across’ to other cliques. 
 * It is an important network structure in the study of human systems because it fits many real world networks (both physical and social) very well.  
     #### Pseudocode for social network
   * Each individual connects to its 2-nearest neighbors and then subject to random rewiring. 
   * In each rewiring event, an individual is randomly selected and drops one of its neighbors randomly. It then selects a       new  neighbor that is randomly chosen from the general population (excluding those to which it was already connected). 
   
   <p align="center">
   <img src="Fig1.png" width="650">
   <br>      
      <em>Fig 1: An example of small world network among for the individuals.</em>   
   </p>
   

 ### Decision-to-move
  * The decision to move (or not-move) is controlled by the parameter risk-life. This is a random number from a uniform           distribution between a minimum (0.0) and maximum (1.0).  
  * A decreasing risk-life (i.e. decreasing the maximum) produce a distribution of individuals who are less probable to take       risk (and vice-versa). 

     #### Pseudocode for Decision-to-move
     
     ```
     If random uniform (0.0, 1.0) > average (self risk-life + random neighbor risk-life ) 
                < move >
     else 
                <do not move>
    ```
  * With this setting, individuals with a lower risk-life and having other-individuals with lower risk-life in their social        network are more likely to move (and vice versa).
  * When an individual decides to move, it randomly selects a point-of-interest as its destination.
  * Once the destination has been reached, an individual chooses a new random destination.
