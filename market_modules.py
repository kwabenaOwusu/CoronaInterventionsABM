#!/usr/bin/env python
# coding: utf-8


### initialization
num_agents = 500 # number of agents 
num_citizens_infected = 5 # number of infectious agents (half-symptomatic and half-asymptomatic) 

prob_exposed = 0.3 # probability of a susceptible becoming exposed (not yet infectious upoun contact
incubation_period = 5  # days required to transition from exposed to infectious
prob_infection = 0.8 # probability of an exposed transitioning to infectious (asymptomatic) else symptomatic
recovery_susceptible = 14 # days to remain immune upoun recovery 
asymptomatic_recovery = 9 # days to transition from asymptomatic to recovered
quarantined_recovery = 14 # days to clinical recovery 
num_years = 150 # number of years of simulation

#risk_life = 0.5 #  risk level by moving outside
#social_radius = 2 # social radius within which interaction is possible
#eff_quarantined = 0.25 # efficiency of contact tracing symptomatic for treatments at hospitals
#hospital_capacity = 1 # the capacity of the hospitals (in reference to the general population)
#essentials_move = 8 # move out only for essentials

point_deviation_x =1500 # deviation from centers
point_deviation_y =1500

area_boundary = (boundary_proj.at[0,'geometry']) # extract polygon geometry of boundary shape
minx, miny, maxx, maxy = area_boundary.bounds # get the bounds of study area


class agent:  # create an empty class
    pass     
      

def initialize():
    global agents, all_agents, exposed_agents, susceptible_agents, infected_agents, asymptomatic_agents, symptomatic_agents, symptomatic1_agents, symptomatic2_agents,  time1, quarantined, quarantined1, quarantined2,quarantined3
    global time_of_day, time, center, alert_official, nonalert_official,citizen_list,official_list,social_network_lines, social_network_lines1, updating_citizens, citizen_list, official_list
    global hospitals_multipoint, schools_multipoint, place_worship_multipoint, marketplaces_multipoint
    global exposed_plot, susceptible_plot, infected_plot, symptomatic_plot, asymptomatic_plot,symptomatic1_plot,symptomatic2_plot, susceptible_plot1 
    global prob_exposed, incubation_period, prob_infection, asymptomatic_recovery, risk_life, social_radius, eff_quarantined, quarantined_recovery , hospital_capacity, essentials_move

    
    # storage
    agents = []
    exposed_plot = [0]
    susceptible_plot =[(num_agents - num_citizens_infected)] 
    #susceptible_plot1 =[0]
    infected_plot =[num_citizens_infected]
    symptomatic_plot =[math.ceil(num_citizens_infected / 2)]
    asymptomatic_plot =[num_citizens_infected - math.ceil(num_citizens_infected / 2)]
    symptomatic1_plot =[math.ceil(num_citizens_infected / 2)]
    symptomatic2_plot =[0]
  
    center=[] 
    quarantined =[] 
    quarantined1 = [0] 
    quarantined2 = [0] 
    quarantined3 = [0] 
    time = 0
    time1 =[time]
    
   
    # geodataframes for social network plot (just for visualization if neccessary)
    social_network_lines = gpd.GeoDataFrame(geometry='geometry',columns=['geometry'], crs=edges_proj.crs) # lines of social network
    social_network_lines1 = gpd.GeoDataFrame(geometry='geometry',columns=['geometry'], crs=edges_proj.crs) # lines of social network for rewiring
    
    
    # multipoint of places of interest (if wants to find nearest place)
    hospitals_multipoint= MultiPoint(hospitals_proj['centroid'])
    schools_multipoint= MultiPoint(schools_proj['centroid'])
    place_worship_multipoint= MultiPoint(place_worship_proj['centroid'])
    marketplaces_multipoint= MultiPoint(marketplaces_proj['centroid'])
    
    
    # set the centers of clustering
    for i in range(5):
        while True:   
            x = random.uniform(minx, maxx)
            y = random.uniform(miny, maxy)
            pnt0 = Point(x, y)
            if  area_boundary.contains(pnt0):
                center.append((x,y))
                break
    
    # loop to initialize variables for agents
    for j in range(num_agents):   
        ag = agent()
        ag.type = 'citizen' 
        ag.trust_official = random.uniform(0,risk_life) # trust in officials
          
        # set clusters of citizens based on number of center
        if (j < 0.2 * num_agents) :
            while True:
                ag.x = random.gauss(center[0][0],point_deviation_x)
                ag.y = random.gauss(center[0][1], point_deviation_y)
                pnt1=Point(ag.x, ag.y)
                if area_boundary.contains(pnt1):
                    ag.geometry = pnt1
                    break 
                        
        elif (0.20 * num_agents) <= j < (0.4 * num_agents) :
            while True:
                ag.x = random.gauss(center[1][0],point_deviation_x)
                ag.y = random.gauss(center[1][1], point_deviation_y)
                pnt2=Point(ag.x, ag.y)
                if area_boundary.contains(pnt2):
                    ag.geometry = pnt2
                    break 
                        
        elif  (0.4 * num_agents) <= j <  (0.6 * num_agents) :
            while True:
                ag.x = random.gauss(center[2][0],point_deviation_x)
                ag.y = random.gauss(center[2][1], point_deviation_y)
                pnt3=Point(ag.x, ag.y)
                if area_boundary.contains(pnt3):
                    ag.geometry = pnt3
                    break 
                        
        elif (0.6 * num_agents) <= j <  (0.8 * num_agents) :
            while True:
                ag.x = random.gauss(center[3][0],point_deviation_x)
                ag.y = random.gauss(center[3][1], point_deviation_y)
                pnt4=Point(ag.x, ag.y)
                if area_boundary.contains(pnt4):
                    ag.geometry = pnt4
                    break 
        else :
            while True:
                ag.x = random.gauss(center[4][0],point_deviation_x)
                ag.y = random.gauss(center[4][1], point_deviation_y)
                pnt5=Point(ag.x, ag.y)
                if area_boundary.contains(pnt5):
                    ag.geometry = pnt5
                    break 
                        
        ag.social_network = [] # social network geometry of citizen
        ag.social_network_agent =[] # social network agent of citizen
        ag.route = [] # route to keep path 
        
        agents.append(ag) # store  all the agents
        #else: # if an official
        #ag.geometry = Point(center[(j-num_citizens)][0],center[(j-num_citizens)][1]) # assign it one of the centers
            
            
        
    # keep agents according to type
    sample_citizens = random.sample(agents, num_citizens_infected) # randomly sample citizens to initialise as infectious
    counter_init = 0
    for ag in agents: # assign the status to citizens
        if ag in sample_citizens :
            if  counter_init % 2 == 0 : # first half as symptomatic
                ag.status = 'infected'
                ag.specifics = 'symptomatic'
                ag.time_exposed = 0
                ag.time_symptomatic = 0
                ag.time_asymptomatic = 0
                ag.time_recovered = 0
                ag.quarantined = 'no'
                ag.time_quarantined = 0
                counter_init += 1
            elif counter_init % 2 != 0 : # second half as asymptomatic
                ag.status = 'infected'
                ag.specifics = 'asymptomatic'
                ag.time_exposed = 0
                ag.time_symptomatic = 0
                ag.time_asymptomatic = 0
                ag.time_recovered = 0
                ag.quarantined = 'no'
                ag.time_quarantined = 0
                counter_init += 1
                
        else : # remaining as susceptibles
            ag.status = 'susceptible' 
            ag.specifics = 'null'
            ag.time_exposed = 0
            ag.time_symptomatic = 0
            ag.time_asymptomatic = 0
            ag.time_recovered = 0
            ag.quarantined = 'no'
            ag.time_quarantined = 0
    
    
    # social network according to small world network, nearest k neighbours (here 2)
    counter = 0  
    for ag in agents:
        for i in range(2):
            multipoint_social_network=MultiPoint([nb.geometry for nb in agents if nb != ag and nb.geometry not in ag.social_network]) # multipoint of all except myself and one already in my network
            nearest_social_network = nearest_points(ag.geometry, multipoint_social_network)[1]   # the nearest point from myself
            ag.social_network.append(nearest_social_network) # keep geometry of those in my network
            ag.social_network_agent.append([ag for ag in agents if ag.geometry == nearest_social_network][0]) # keep agent but not geometry
            social_network_linestring1=LineString([ag.geometry,nearest_social_network])# create linestring just for plotting
            social_network_lines.at[counter,'geometry'] = social_network_linestring1 # append  linestring of social network to corresponding geodataframe
            counter += 1
     
    # iteration of the small world network
    counter = 0
    #while counter < (20): # counter should not be more than (num_agent-(k+1)) no matter the probability!!!
    for ag in agents :
            #ag = random.choice([j for j in agents]) # randomly sample a citizen  agent
        if random.random() < 0.05: # set low for high number of agents
            chose1= random.choice(ag.social_network_agent) # randomly select an agent from the focal-agent social network
            ag.social_network_agent.remove(chose1) # remove the selected agent from the focal-agent social network
            chose2 = random.choice([nb for nb in agents if nb!=chose1 and nb not in ag.social_network_agent]) # select agent but not the one just removed and those still in focal-agent social network
            ag.social_network_agent.append(chose2) # add the agent (just above) to the focal-agent social network
            chose2.social_network_agent.append(ag) # the selected agent added to focal-agent also has the the focal agent as its neighbors
            social_network_linestring2=LineString([ag.geometry,chose2.geometry])# create linestring
            social_network_lines1.at[counter,'geometry'] = social_network_linestring2 # append  linestring of social network to corresponding geodataframe
            counter += 1        
            
#initialize()


###observation
def observe():
    
    global agents, all_agents, exposed_agents, susceptible_agents, infected_agents, asymptomatic_agents, symptomatic_agents, symptomatic1_agents, symptomatic2_agents,  time1, quarantined, quarantined1, quarantined2,quarantined3
    global time_of_day, time, center, alert_official, nonalert_official,citizen_list,official_list,social_network_lines, social_network_lines1, updating_citizens, citizen_list, official_list
    global hospitals_multipoint, schools_multipoint, place_worship_multipoint, marketplaces_multipoint, susceptible_plot1
    global exposed_plot, susceptible_plot, infected_plot, symptomatic_plot, asymptomatic_plot,symptomatic1_plot,symptomatic2_plot
    global prob_exposed, incubation_period, prob_infection, asymptomatic_recovery, risk_life, social_radius, eff_quarantined, quarantined_recovery, hospital_capacity, essentials_move
     
    
    plt.clf()  # clear plot
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(23,8))
    gs = gridspec.GridSpec(1, 2, width_ratios=[2.5, 1]) 
    #fig.patch.set_facecolor('white') # reset the black background
    #fig, ax = plt.subplots(figsize=(12,8)
    
      
    ax = plt.subplot(gs[0]) 
    # Plot the street
    edges_proj.plot(ax=ax, linewidth=0.25,edgecolor='#969494')
    
    # Plot the boundary
    boundary_proj.plot(ax=ax,color="black" ,alpha=1 ,linewidth=2, ec='white')
     
    # Plot the hospitals
    #hospitals_proj.plot(ax=ax,color='magenta', alpha=1, markersize=10, zorder=3 )

    # Plot schools
    #schools_proj.plot(ax=ax, color='yellow', alpha=1, markersize=10,zorder=3)

    # Plot mosques/churches
    #place_worship_proj.plot(ax=ax, color='cyan', alpha=1, markersize=10,zorder=3)

    # Plot shopping center / marketsplaces
    marketplaces_proj.plot(ax=ax, color='yellow', alpha=1, markersize=100,zorder=3)
    
    
    # updating agents
    #all_agents = gpd.GeoDataFrame([ag.geometry for ag in agents],geometry='geometry',columns=['geometry'], crs=edges_proj.crs) # empty geodataframe for citizens
    exposed_agents = gpd.GeoDataFrame([ag.geometry for ag in agents if ag.status=='exposed'],geometry='geometry',columns=['geometry'], crs=edges_proj.crs)
    susceptible_agents = gpd.GeoDataFrame([ag.geometry for ag in agents if ag.status=='susceptible'],geometry='geometry',columns=['geometry'], crs=edges_proj.crs)
    #infected_agents = gpd.GeoDataFrame([ag.geometry for ag in agents if ag.status=='infected'],geometry='geometry',columns=['geometry'], crs=edges_proj.crs)
    asymptomatic_agents = gpd.GeoDataFrame([ag.geometry for ag in agents if ag.status == 'infected' and ag.specifics == 'asymptomatic'],geometry='geometry',columns=['geometry'], crs=edges_proj.crs)
    symptomatic_agents = gpd.GeoDataFrame([ag.geometry for ag in agents if ag.status == 'infected' and ag.specifics == 'symptomatic'],geometry='geometry',columns=['geometry'], crs=edges_proj.crs)
    symptomatic1_agents = gpd.GeoDataFrame([ag.geometry for ag in agents if ag.status == 'infected' and ag.specifics == 'symptomatic' and ag.quarantined == 'no'],geometry='geometry',columns=['geometry'], crs=edges_proj.crs)
    #symptomatic2_agents = gpd.GeoDataFrame([ag.geometry for ag in agents if ag.status == 'infected' and ag.specifics == 'symptomatic' and ag.quarantined == 'yes'],geometry='geometry',columns=['geometry'], crs=edges_proj.crs)
    
    
    colors = numpy.linspace(0, 1, 4) ; mymap = plt.get_cmap("Reds") ; my_colors = mymap(colors)   # set three different color of reds 
    #plotting agents
    if len(susceptible_agents) > 0:
        susceptible_agents.plot(ax=ax, marker='o', alpha=1,markersize=10, color=my_colors[0], zorder=5)
    if len(exposed_agents) > 0:
        exposed_agents.plot(ax=ax, marker='o', alpha=1,markersize=10, color=my_colors[1], zorder=5)
    if len(asymptomatic_agents) > 0:
        asymptomatic_agents.plot(ax=ax, marker='o', alpha=1,markersize=10, color=my_colors[2], zorder=5)
    if len(symptomatic1_agents) > 0:
        symptomatic1_agents.plot(ax=ax, marker='o', alpha=1,markersize=10, color=my_colors[3], zorder=5)
        
            
    #network to visualisation (if necessary)
    #social_network_lines.plot(ax=ax,alpha=1, lw=0.7, color='yellow')
    #if len(social_network_lines1) > 0:
        #social_network_lines1.plot(ax=ax,alpha=1, lw=0.7, color='yellow')

    # labels of main plot
    ax.set_title('Dakar, day =' + str(int(time)),fontsize=15) # title
    #ax.set_xlabel('X Coordinates (meters)',fontsize=15)
    #ax.set_ylabel('Y Coordinates (meters)',fontsize=15)
    ax.set_yticks([]) ; ax.set_xticks([])
    
    
    ax.text(-1945000, 1677494, r'nr. of susceptibles  = ' + str(num_agents - num_citizens_infected) , {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1676500, r'nr. of infectious = ' + str(num_citizens_infected), {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1675500, r'risk to life = ' + str(risk_life), {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1674500, r'prob of exposed = ' + str(prob_exposed), {'color': 'w', 'fontsize': 14}, style='italic', alpha=1)
    ax.text(-1945000, 1673500, r'probability of asymptomatic  = ' + str(prob_infection) , {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1672500, r'probability of symptomatic  = ' + str(round((1-prob_infection),2)) , {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1671500, r'social radius = ' + str(social_radius)  + ' m' , {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1670500, r'eff. contact tracing = ' + str(eff_quarantined), {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1669500, r'capacity of hospital = ' + str(hospital_capacity) + ' % pop.', {'color': 'w', 'fontsize': 14}, style='italic')
    ax.text(-1945000, 1668500, r'activeness per day = ' + str(essentials_move ) + ' hours', {'color': 'w', 'fontsize': 14}, style='italic')
    #ax.text(-1945000, 1670300, r'hospital recovery = ' + str(quarantined_recovery) + 'days', {'color': 'w', 'fontsize': 13}, style='italic')
    #ax.text(-1945000, 1669500, r'recovery period = ' + str(recovery_susceptible) + 'days', {'color': 'w', 'fontsize': 13}, style='italic')
    #ax.text(-1945000, 1676700, r'incubation_exposed = ' + str(incubation_period)  + 'days' ,{'color': 'w', 'fontsize': 13}, style='italic')
    #ax.text(-1945000, 1675100, r'recovery_asymptomatic = ' + str(asymptomatic_recovery) + 'days', {'color': 'w', 'fontsize': 13}, style='italic')
     
   
    
    #quarantine identified infected
    # create an inset in the lower right corner (loc=4) with borderpad=1, i.e. 10 points padding (as 10pt is the default fontsize) to the parent axes
    axins = inset_axes(ax, width=3.5, height=3, loc=8, borderpad=1)
    ## Turn ticklabels of insets off
    axins.tick_params(labelleft=False, labelbottom=False)
    quarantine_xs = [point.x   for point in quarantined]
    quarantine_ys = [point.y  for point in quarantined]
    axins.scatter(quarantine_xs, quarantine_ys, marker='o', alpha=1, color='red',s=12)
    axins.set_title('IN, OUT, REMAIN = ' + str(quarantined1[-1]) + ':' + str(quarantined2[-1]) + ':' + str(quarantined3[-1]),color = 'w')
    axins.set_yticks([]) ; axins.set_xticks([])
  
   
    # Here we create a legend: we'll plot empty lists with the desired color and label
    #for colorx, places in [('magenta','hospital'), ('yellow','school'), ('cyan','church/mosque'),('lime','marketplace')]:
        #ax.scatter([], [], c=colorx, s=100, label=places, alpha=1, edgecolors='none',marker='s')
    #leg1=ax.legend(frameon=True,title='',labelspacing=1,loc="upper left",fontsize=14)
    for colorx, places in [('yellow','marketplace')]:
        ax.scatter([], [], c=colorx, s=100, label=places, alpha=1, edgecolors='none',marker='s')
    leg1=ax.legend(frameon=True,title='',labelspacing=1,loc="upper left",fontsize=14)
    
    
    
    # plot of dynamics 
    ax1 = plt.subplot(gs[1])
    
    #time series plot
    #ax1.plot(time1,susceptible_plot, color='white',linewidth=3.0)
    #infected_plot[-1] += len(quarantined)
    #ax1.plot(time1,infected_plot, color='red',linewidth=3.0)
    #ax1.set_title('Dynamics of disease progression',fontsize=15) # title
    #ax1.set_ylabel('Number of individuals',fontsize=15)
    #ax1.set_xlabel('Days',fontsize=15)
    #plt.xticks([], [])
    #ax1.set_ylim([0,num_citizens])
    
    # stackplot
    y=[susceptible_plot, exposed_plot, asymptomatic_plot, symptomatic_plot] 
    pal = [my_colors[0], my_colors[1], my_colors[2], my_colors[3]]
    ax1.stackplot(time1,y, colors=pal)
    ax1.set_title('Dynamics of disease',fontsize=15) # title
    ax1.set_ylabel('Number of individuals',fontsize=15)
    ax1.set_xlabel('Days',fontsize=15)
    ax1.set_ylim([0,num_agents])


    for coly, individuals in [(my_colors[0],'susceptible'),(my_colors[1],'exposed'), (my_colors[2],'asymptomatic'), (my_colors[3],'symptomatic'),]:
        ax1.plot([], [], c=coly, label=individuals,alpha=1,linewidth=3.0)
    ax1.legend(frameon=True,title='',labelspacing=1,loc="lower left",fontsize=14)

    # adding basemap
    #ctx.add_basemap(ax,attribution='')
    #ax.set_axis_off()
    #"""
    # Remove white space around the figure
    plt.tight_layout(pad=-10) # space between subplots
    
    # Save the figure as png file with resolution of 300 dpi
    suptitle_font = {'family':'DejaVu Sans', 'fontsize':45, 'fontweight':'normal', 'y':0.15, 'color':'white'}
    fig.canvas.draw()
    plt.savefig('day_%04d.png' %time, bbox_inches='tight', pad_inches=0, dpi=300)

#observe()



###updating
def update_main():
    
    global agents, all_agents, exposed_agents, susceptible_agents, infected_agents, asymptomatic_agents, symptomatic_agents, symptomatic1_agents, symptomatic2_agents,  time1, quarantined, quarantined1, quarantined2,quarantined3
    global time_of_day, time, center, alert_official, nonalert_official,citizen_list,official_list,social_network_lines, social_network_lines1, updating_citizens, citizen_list, official_list
    global hospitals_multipoint, schools_multipoint, place_worship_multipoint, marketplaces_multipoint
    global exposed_plot, susceptible_plot, infected_plot, symptomatic_plot, asymptomatic_plot,symptomatic1_plot,symptomatic2_plot, susceptible_plot1
    global prob_exposed, incubation_period, prob_infection, asymptomatic_recovery, risk_life, social_radius, eff_quarantined, quarantined_recovery, hospital_capacity, essentials_move

 
    focal_citizen = random.choice([j for j in agents if j.quarantined == 'no']) # randomly sample an  agent
    focal_citizen_network = random.choice(focal_citizen.social_network_agent).trust_official # randomly select one of focal agents network agent-trust in in offcials 
    
    if  random.random() > ((focal_citizen.trust_official  +  focal_citizen_network) / 2) : 
        if len(focal_citizen.route) == 0 : # if route list is empty
            #places = ['hospitals','schools','place_worship','marketplaces'] 
            places = ['marketplaces'] 
            point_interest = random.choice(places) # randomly select a target location
        
            # selecting nearest of the target to focal agent
            if point_interest == 'marketplaces' :
                nearest_point_interest=random.choice(marketplaces_proj['centroid'])
            #if point_interest == 'hospitals' :
                ##nearest_point_interest = nearest_points(focal_citizen.geometry, hospitals_multipoint)[1]
                #nearest_point_interest=random.choice(hospitals_proj['centroid']) # randomly choice a hospital not nearest
            #elif point_interest == 'schools' :
                #nearest_point_interest=random.choice(schools_proj['centroid'])
            #elif point_interest == 'place_worship' :
                #nearest_point_interest=random.choice(place_worship_proj['centroid'])
            #elif point_interest == 'marketplaces' :
                #nearest_point_interest=random.choice(marketplaces_proj['centroid'])
        
            # shortest path or route of Dijkstra’s algorithm
            orig_xy = (focal_citizen.y, focal_citizen.x) # Get focal agent x and y coordinates
            target_xy = (nearest_point_interest.y, nearest_point_interest.x) # Get target x and y coordinates
        
            orig_node = ox.get_nearest_node(G_proj, orig_xy, method='euclidean') # Find the node in the graph that is closest to the origin point (here, we want to get the node id)
            target_node = ox.get_nearest_node(G_proj, target_xy, method='euclidean') # Find the node in the graph that is closest to the target point (here, we want to get the node id)
    
            focal_citizen_route = nx.shortest_path(G=G_proj, source=orig_node, target=target_node, weight='length') # calculate the shortest path or route between these nodes then plot it
            #fig, ax = ox.plot_graph_route(G_proj, focal_citizen_route, node_size=0)
            
            focal_citizen_route = [str(i) for i in focal_citizen_route] # make route (osmid) as a list
            focal_citizen_route1=nodes_proj.loc[nodes_proj['osmid'].isin(focal_citizen_route), 'geometry'] # all osmid corresponding geometry 
            focal_citizen.route=list(focal_citizen_route1) # make above as a list
            #gpd.GeoDataFrame(focal_citizen.route, columns=['geometry'])
            focal_citizen.geometry = focal_citizen.route[0] # set current geometry to first in path
            del focal_citizen.route[0] # delete the path just moved to
            
                         
            # if an infected agents in neighborhood set susceptibles as exposed
            focal_citizen_neighbors = [j for j in agents if (j.quarantined == 'no') and ((j.geometry).distance(focal_citizen.geometry) < social_radius) and (j != focal_citizen)]
            focal_citizen_neighbors_infected = [j for j in focal_citizen_neighbors if j.status == 'infected']
            if len(focal_citizen_neighbors_infected) > 0 :
                if all([(focal_citizen.status == 'susceptible'),(focal_citizen.specifics == 'null') ,(random.random() < prob_exposed),(focal_citizen.quarantined == 'no')]) :
                    focal_citizen.status = 'exposed'
                    focal_citizen.specifics = 'null'
                   
            # if exposed for more than five days, set to infected either as symptomatic or asymptomatic        
            if all([(focal_citizen.status == 'exposed') , (focal_citizen.specifics == 'null') , (focal_citizen.time_exposed > incubation_period), (focal_citizen.quarantined == 'no')]) :
                if random.random() < prob_infection :
                    focal_citizen.status = 'infected'
                    focal_citizen.specifics = 'asymptomatic'
                else :
                    focal_citizen.status = 'infected'
                    focal_citizen.specifics = 'symptomatic'
                    
            # if asymptomatics for more than 9 days , recover to susceptible
            if all([(focal_citizen.status == 'infected'),(focal_citizen.specifics == 'asymptomatic') ,(focal_citizen.time_asymptomatic > asymptomatic_recovery), (focal_citizen.quarantined == 'no')]) :
                    focal_citizen.status = 'susceptible'
                    focal_citizen.specifics = 'recovered'
                    
            # if asymptomatics recovered for more than 14 days , transition to susceptible
            if all([(focal_citizen.status == 'susceptible'),(focal_citizen.specifics == 'recovered') ,(focal_citizen.time_recovered > recovery_susceptible), (focal_citizen.quarantined == 'no')]) :
                    focal_citizen.status = 'susceptible'
                    focal_citizen.specifics = 'null'
                                    
                   
                       
    
        else :
            focal_citizen.geometry = focal_citizen.route[0]
            del focal_citizen.route[0]
            
                        # if an infected agents in neighborhood set susceptibles as exposed
            focal_citizen_neighbors = [j for j in agents if (j.quarantined == 'no') and ((j.geometry).distance(focal_citizen.geometry) < social_radius) and (j != focal_citizen)]
            focal_citizen_neighbors_infected = [j for j in focal_citizen_neighbors if j.status == 'infected']
            if len(focal_citizen_neighbors_infected) > 0 :
                if all([(focal_citizen.status == 'susceptible'),(focal_citizen.specifics == 'null') ,(random.random() < prob_exposed),(focal_citizen.quarantined == 'no')]) :
                    focal_citizen.status = 'exposed'
                    focal_citizen.specifics = 'null'
                   
            # if exposed for more than five days, set to infected either as symptomatic or asymptomatic        
            if all([(focal_citizen.status == 'exposed') , (focal_citizen.specifics == 'null') , (focal_citizen.time_exposed > incubation_period), (focal_citizen.quarantined == 'no')]) :
                if random.random() < prob_infection :
                    focal_citizen.status = 'infected'
                    focal_citizen.specifics = 'asymptomatic'
                else :
                    focal_citizen.status = 'infected'
                    focal_citizen.specifics = 'symptomatic'
                    
            # if asymptomatics for more than 9 days , recover to susceptible
            if all([(focal_citizen.status == 'infected'),(focal_citizen.specifics == 'asymptomatic') ,(focal_citizen.time_asymptomatic > asymptomatic_recovery), (focal_citizen.quarantined == 'no')]) :
                    focal_citizen.status = 'susceptible'
                    focal_citizen.specifics = 'recovered'
                    
            # if recovered for more than 14 days , transition to susceptible
            if all([(focal_citizen.status == 'susceptible'),(focal_citizen.specifics == 'recovered') ,(focal_citizen.time_recovered > recovery_susceptible), (focal_citizen.quarantined == 'no')]) :
                    focal_citizen.status = 'susceptible'
                    focal_citizen.specifics = 'null'

#update_main()


### iterations within time-step
def update_one_unit_time():
    global agents, all_agents, exposed_agents, susceptible_agents, infected_agents, asymptomatic_agents, symptomatic_agents, symptomatic1_agents, symptomatic2_agents,  time1, quarantined, quarantined1, quarantined2,quarantined3
    global time_of_day, time, center, alert_official, nonalert_official,citizen_list,official_list,social_network_lines, social_network_lines1, updating_citizens, citizen_list, official_list
    global hospitals_multipoint, schools_multipoint, place_worship_multipoint, marketplaces_multipoint
    global exposed_plot, susceptible_plot, infected_plot, symptomatic_plot, asymptomatic_plot,symptomatic1_plot,symptomatic2_plot, susceptible_plot1
    global prob_exposed, incubation_period, prob_infection, asymptomatic_recovery, risk_life, social_radius, eff_quarantined, quarantined_recovery, hospital_capacity, essentials_move

    time += 1  # update time
    t = 0.
    while t < 1 :
        t += 1. / (essentials_move * sum([1 for j in agents if j.quarantined == 'no'])) # we assume a 1 / (number of fishes) time passes by per time. we use twlve bcos 8 hours of activity 
        update_main()       # thus on-average each fish agent is updated once per time.
        
        
      
    # when status changed begins to count number of days, setting all other times to zero
    for ag in agents :
        if all([(ag.status == 'susceptible') , (ag.specifics == 'recovered'),(ag.quarantined == 'no')]) :
            ag.time_recovered += 1
            ag.time_exposed = 0
            ag.time_symptomatic  = 0
            ag.time_asymptomatic = 0
            
        elif all([(ag.status == 'exposed'),(ag.specifics == 'null') ,(ag.quarantined == 'no')]) :
            ag.time_exposed += 1
            ag.time_symptomatic  = 0
            ag.time_asymptomatic = 0
            ag.time_recovered = 0
            
        elif all([(ag.status == 'infected'),(ag.specifics == 'asymptomatic'),(ag.quarantined == 'no')]) :
            ag.time_asymptomatic += 1
            ag.time_exposed = 0
            ag.time_symptomatic  = 0
            ag.time_recovered = 0
            
      
             

    counter_xx = 0 # track number of symptomatic quarantined per day
    for ag in agents :
        if all([(ag.status == 'infected'),(ag.specifics == 'symptomatic'),(ag.quarantined == 'no'),(random.random() < eff_quarantined)]):
            ag.quarantined = 'yes'
            ag.time_quarantined = 0
            counter_xx += 1
    quarantined1.append(counter_xx) # comes into quarantine box
      

    counter_yy = 0
    for ag in agents : # recovery from quarantined, less likely as number of quarantined increases
        if all([(ag.status == 'infected'),(ag.specifics == 'symptomatic'),(ag.quarantined == 'yes')]):
            ag.time_quarantined += 1                                 
            if (ag.time_quarantined > quarantined_recovery) :
                if random.random() < (1-(sum([1 for j in agents if j.quarantined == 'yes']) / float(hospital_capacity * num_agents))) : 
                    ag.quarantined = 'no'
                    ag.status = 'susceptible'
                    ag.specifics == 'recovered'
                    counter_yy += 1
    quarantined2.append(counter_yy) # go outside quarantined box   
    quarantined = [j.geometry for j in agents if j.quarantined == 'yes'] # placed under quarantined
    quarantined3.append(abs(sum(quarantined1) - sum(quarantined2))) # remaining in quarantined box
    
    
    susceptible_plot.append(sum([1 for j in agents if j.status == 'susceptible'])) # number of susceptibles
    #susceptible_plot1.append(sum([1 for j in agents if j.status == 'susceptible'and j.specifics == 'recovered'])) # number of susceptibles
    exposed_plot.append(sum([1 for j in agents if j.status == 'exposed'])) # number of exposed
    infected_plot.append(sum([1 for j in agents if  j.status == 'infected'])) # all infected
    asymptomatic_plot.append(sum([1 for j in agents if j.status == 'infected' and j.specifics == 'asymptomatic'])) # number of all asymptomatics
    symptomatic_plot.append(sum([1 for j in agents if j.status == 'infected' and j.specifics == 'symptomatic'])) # number of all symptomatic
    symptomatic1_plot.append(sum([1 for j in agents if j.status == 'infected' and j.specifics == 'symptomatic' and j.quarantined == 'no'])) # number of symptomatic  not quarantined
    symptomatic2_plot.append(sum([1 for j in agents if j.status == 'infected' and j.specifics == 'symptomatic' and j.quarantined == 'yes'])) # number of symptomatic  quarantined
    time1.append(time)
    
      
    csvfile = "simulation_data.csv"   # a csv-file output 
    header = ['susceptible_all','exposed', 'infected_all','asymptomatic','symptomatic_all','sympto_not_quarantined','sympto_quarantined', 'in_per_day','out_per_day','remaining_per_day']
    main_data = [susceptible_plot, exposed_plot, infected_plot,asymptomatic_plot,symptomatic_plot,symptomatic1_plot,symptomatic2_plot,quarantined1, quarantined2, quarantined3]
    with open(csvfile, "w") as output:
        writer = csv.writer(output) 
        writer.writerow(header)
        writer.writerows(zip(*main_data))    

#update_one_unit_time()





