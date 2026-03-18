import esper

from . import components
from . import processors

def init():
    player = esper.create_entity(components.Player("player", "active", 20), components.Position([0, 0], 0, 0), components.Velocity(), components.Renderable("playerImage", (0, 0, 16, 32)))

    esper.add_processor(processors.MovementProcessor)
    esper.add_processor(processors.RenderProcessor)

