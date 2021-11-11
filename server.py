from model import RandomModel, ObstacleAgent,DirtyCell
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter
from mesa.visualization.modules import CanvasGrid, ChartModule, PieChartModule

COLORS = {"Dirty": "#00AA00"}

def agent_portrayal(agent):
    if agent is None: return
    
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}

    if (isinstance(agent, ObstacleAgent)):
        portrayal["Color"] = "grey"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.2
    
    if (isinstance(agent, DirtyCell)):
        portrayal["Color"] = "black"
        portrayal["Layer"] = 1
        portrayal["r"] = 0.3

    return portrayal

model_params = {"N": UserSettableParameter("slider", "Numero de Roombas", 4, 1, 10, 1), "width":10, "height":10, "density": UserSettableParameter("slider", "Porcentage de Celdas Sucias", 0.65, 0.01, 1.0, 0.01),"maxSteps": UserSettableParameter("slider", "Max Number of Steps", 250, 50, 300, 25)}

tree_chart = ChartModule(
    [{"Label": label, "Color": color} for (label, color) in COLORS.items()]
)

grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = ModularServer(RandomModel, [grid,tree_chart], "Roomba", model_params)
                       
server.port = 8521 # The default
server.launch()