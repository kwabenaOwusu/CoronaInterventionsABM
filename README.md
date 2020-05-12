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

## Individuals
* They are characterized by their location (x and y coordinates).
* Health status: susceptible, exposed, asymptomatic, and symptomatic.
* Risk to life: how one values own life influencing decision to move.
* Social network:  list of other-individuals connected to an individual.
* Social radius: a measure of adherence to hygiene and social distancing.

## Government-official 
* They identify infectious individuals for treatments at hospitals. 
* Characterized by the efficiency of contact tracing: the proportion of infectious individuals traced for treatment at hospital (reflecting the capacity of health systems). 
* The model time step is a day. The length of one-time step depends on the size of the individuals (minus those under treatments at hospital). Simulations last for 100 days.
