from mesa import Agent

class RandomAgent(Agent):
    """
    Agent that moves randomly.
    Attributes:
        unique_id: Agent's ID 
        direction: Randomly chosen direction chosen from one of eight directions
    """
    def __init__(self, unique_id, model, maxSteps):
        """
        Creates a new random agent.
        Args:
            unique_id: The agent's ID
            model: Model reference for the agent
        """
        super().__init__(unique_id, model)
        self.direction = 4
        self.condition = "Roomba"
        self.limit = maxSteps
        self.temp = 0

    def move(self):
        """ 
        Determines if the agent can move in the direction that was chosen
        """
        possible_steps = self.model.grid.get_neighborhood(
            self.pos,
            moore=True, # Boolean for whether to use Moore neighborhood (including diagonals) or Von Neumann (only up/down/left/right).
            include_center=True) 
        
        # Checks which grid cells are empty
        
        freeSpaces = list(map(self.checkProximity, possible_steps))
        print(freeSpaces)

        # If the cell is empty, moves the agent to that cell; otherwise, it stays at the same position
        if freeSpaces[self.direction]:
            self.model.grid.move_agent(self, possible_steps[self.direction])
            print(f"Se mueve de {self.pos} a {possible_steps[self.direction]}; direction {self.direction}")
        else:
            print(f"No se puede mover de {self.pos} en esa direccion.")

    def step(self):
        """ 
        Determines the new direction it will take, and then moves
        """        
        self.temp += 1
        if self.temp < self.limit:
            self.direction = self.random.randint(0,8)
            print(f"Roomba: {self.unique_id} movimiento {self.direction}")
            self.move()
        else:
            print("You have run out of steps for this Roomba")
    
    def checkProximity(self,pos):
        if len(self.model.grid.get_cell_list_contents(pos)) >= 1:
            other = self.model.grid.get_cell_list_contents(pos)
            if other[0].condition == "Dirty":
                return True
        if self.model.grid.is_cell_empty(pos) == True:
            return True
        else:
            return False
        

class ObstacleAgent(Agent):
    """
    Obstacle agent. Just to add obstacles to the grid.
    """
    def __init__(self, unique_id, model):
        super().__init__(unique_id, model)
        self.condition = "Wall"

    def step(self):
        #
        pass 

class DirtyCell(Agent):
    

    def __init__(self, pos, model):
        
        super().__init__(pos, model)
        self.pos = pos
        self.condition = "Dirty"

    def step(self):
        if len(self.model.grid.get_cell_list_contents(self.pos)) > 1:
            other = self.model.grid.get_cell_list_contents(self.pos)
            if other[1].condition == "Roomba" or other[0].condition == "Roomba":
                self.model.schedule.remove(self)
                self.model.grid.remove_agent(self)
            
            
