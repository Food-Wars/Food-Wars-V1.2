import esper

from . import components

from .. import data
from ..import renderers

class RenderProcessor(esper.Processor):
    def process(dt):
        for entID, (pos, rend) in esper.get_components(components.Position, components.Renderable):
            data.screen.blit(data.getImg(rend.image), renderers.getScreenPos(pos.Chunk, pos.xOffset, pos.yOffset))

class MovementProcessor(esper.Processor):
    def process(dt):
        for entID, (pos, vel) in esper.get_components(components.Position, components.Velocity):
            pos.Chunk, pos.xOffset, pos.yOffset = data.getMovePositions(pos.Chunk, pos.xOffset, pos.yOffset, (vel.xVel, vel.yvel))
