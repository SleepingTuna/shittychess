# coding=utf-8


from os import PathLike
from typing import Union
from typing import Tuple
from typing import NoReturn

import pygame


class ShittyMousePointer(pygame.sprite.Sprite):
    def __init__(self, x, y) -> NoReturn:
        """constructor"""

        pygame.sprite.Sprite.__init__(self)
        self.rect = pygame.Rect(x, y, 1, 1)


class ShittySprite(pygame.sprite.Sprite):
    """base sprite class for pieces and spaces"""

    def __init__(
            self,
            black: bool,
            rect: pygame.Rect,
            coords: Tuple[int, int],
            img_path: Union[PathLike, str]
    ) -> NoReturn:
        """constructor"""

        # super().__init__(self)
        pygame.sprite.Sprite.__init__(self)
        self.rect = rect
        self.black = black
        self.image: Union[pygame.image, None] = None
        self.coords = coords
        self.load_image(img_path)

    def load_image(self, img_path: Union[PathLike, str]) -> NoReturn:
        self.image = pygame.image.load(
            img_path if isinstance(img_path, str) else str(img_path)
        )
        width = 75
        height = 75
        rect = self.image.get_rect()
        if rect.width != width or rect.height != height:
            self.image = pygame.transform.smoothscale(self.image, (width, height))

    def move_to_front(self) -> bool:
        for group in self.groups():
            try:
                group.move_to_front(self)
                return True
            except AttributeError as e:
                print(f'{e}\ncontinuing...')
                continue
        return False


# class ShittySpace(ShittySprite):
#     """sprite class for board spaces"""

#     def __init__(
#             self,
#             black: bool,
#             rect: pygame.Rect,
#             coords: Tuple[int, int],
#             img_path: Union[PathLike, str]
#     ) -> NoReturn:
#         """constructor"""

#         super().__init__(black, rect, coords, img_path)
