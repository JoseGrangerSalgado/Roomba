from mesa import Model
from mesa.time import RandomActivation
from mesa.space import Grid
from agent import RandomAgent, ObstacleAgent, DirtyCell
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

class RandomModel(Model):
    """ 
    Creates a new roomba simulation.
    
    """
    def __init__(self, N, width, height,density,maxSteps):
        self.num_agents = N
        self.grid = MultiGrid(width,height,torus = False) 
        self.schedule = RandomActivation(self)
        self.running = True 

        self.datacollector = DataCollector(
            {
                "Dirty": lambda m: self.count_type(m, "Dirty"),
            }
        )

        # Creates the border of the grid
        border = [(x,y) for y in range(height) for x in range(width) if y in [0, height-1] or x in [0, width - 1]]

        for pos in border:
            obs = ObstacleAgent(pos, self)
            self.schedule.add(obs)
            self.grid.place_agent(obs, pos)

        # Add the agent to a random empty grid cell
        for i in range(self.num_agents):
            a = RandomAgent(i+1000, self, maxSteps) 
            self.schedule.add(a)
            self.grid.place_agent(a, (1,1))

        for (contents, x, y) in self.grid.coord_iter():
            if self.random.random() < density:
                new_dirt = DirtyCell((x, y), self)
                if x != 0 and x != 1 and y != 0 and y != 1 and y != width-1 and x != height-1:
                    self.schedule.add(new_dirt)
                    self.grid.place_agent(new_dirt, (x, y))
        self.datacollector.collect(self)

    def step(self):
        self.schedule.step()
        if self.count_type(self, "Dirty") == 0:
            self.running = False
        self.datacollector.collect(self)
    
    @staticmethod
    def count_type(model, agent_condition):
        count = 0
        for agent in model.schedule.agents:
            #print(agent.condition)
            if agent.condition == agent_condition:
                count += 1
        print("dirty places left",count)
        return count