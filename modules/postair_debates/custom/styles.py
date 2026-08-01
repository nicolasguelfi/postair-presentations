"""Module styles — thin façade over the postair_dark design system (pack-first).

Blocks import ``from custom.styles import Styles as s`` and use ``s.project.*``
for every shared token; block-local variants live in each block's BlockStyles.
"""

from postair_pack.design_systems.postair_dark import DesignSystem
from streamtex.styles import StxStyles

DS = DesignSystem()


class Custom:
    ds = DS
    colors = DS.colors
    titles = DS.titles
    body = DS.body
    containers = DS.containers
    cards = DS.cards


class Styles(StxStyles):
    project = Custom
