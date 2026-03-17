import esper

from . import components

from .. import data

class RenderProcessor(esper.Processor):
    def process(self):
        for entID, (pos, rend) in esper.get_components(components.Position, components.Renderable):
            pass

class MovementProcessor(esper.Processor):
    def process(self):
        for entID, (pos, vel) in esper.get_components(components.Position, components.Velocity):
            pass
