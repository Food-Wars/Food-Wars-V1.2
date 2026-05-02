import esper

from . import components

from .. import data
from ..import renderers

class RenderProcessor(esper.Processor):
    def process(dt):
        for entID, (pos, rend) in esper.get_components(components.Position, components.Renderable):

            surf, coords = data.getImg("player", rend.image)

            data.screen.blit(surf, renderers.getScreenPos(pos.Chunk, pos.xOffset, pos.yOffset), coords)

class MovementProcessor(esper.Processor):
    def process(dt):
        for entID, (pos, vel) in esper.get_components(components.Position, components.Velocity):
            pos.Chunk, pos.xOffset, pos.yOffset = data.getMovePositions(pos.Chunk, pos.xOffset, pos.yOffset, (vel.xVel, vel.yvel))
