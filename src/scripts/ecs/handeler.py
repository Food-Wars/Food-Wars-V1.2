import esper

from . import components
from . import processors

player = esper.create_entity(components.Player, components.Position([0, 0], 0, 0), components.Velocity())
