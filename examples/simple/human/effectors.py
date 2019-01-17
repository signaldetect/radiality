"""
radiality:examples:simple:human:effectors
"""

from radiality import effect
from radiality import Effector


class Family(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def gathered(self) -> None:
        """
        TODO: Add docstring
        """
        # Causes the `hello_said` event
        await self.hello_said()


class Animal(Effector):
    """
    TODO: Add docstring
    """

    @effect
    async def sound_made(self, name: str) -> None:
        """
        TODO: Add docstring
        """
        print(f'{name} made a sound! -- {self._name} said.')
