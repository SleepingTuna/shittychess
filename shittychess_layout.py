# coding=utf-8


import itertools
from typing import NoReturn
from typing import Union

import pygame

from shittychess_sprites import ShittyMousePointer
from shittychess_pieces import ShittyPiece
from shittychess_pieces import ShittyPawn
from shittychess_pieces import ShittyKnight
from shittychess_pieces import ShittyBishop
from shittychess_pieces import ShittyRook
from shittychess_pieces import ShittyQueen
from shittychess_pieces import ShittyKing


class ShittyGroup(pygame.sprite.Group):
    """subclassing sprite Group to add more functionality"""

    def __init__(self):
        pygame.sprite.Group.__init__(self)

    def sprite_exists(self, coords: str) -> bool:
        for sprite in self.sprites():
            if sprite.coords == coords:
                return True
        return False

    def coords_to_sprite(self, coords: str) -> Union[ShittyPiece, None]:
        for sprite in self.sprites():
            if sprite.coords == coords:
                return sprite
        return None


class ShittyLayout:
    """
    this class manages where all the pieces are on the board
    might want to use this as a property of ShittyBoard
    """

    def __init__(self) -> NoReturn:
        self.screen = None  # pygame.Surface
        self.settings = None  # ShittySettings
        self.logic = None  # ShittyLogic

        self.sprite_group_black = ShittyGroup()
        self.sprite_group_white = ShittyGroup()
        self.sprite_group_all = ShittyGroup()

        self.initial_piece_layout = []

    def configure(self) -> NoReturn:
        """
        configure layout's properties after some of them have been
        assigned externally
        """

        self.initial_piece_layout = [
            # black
            ['a8', ShittyRook, True, self.settings.rook_path(black=True)],
            ['b8', ShittyKnight, True, self.settings.knight_path(black=True)],
            ['c8', ShittyBishop, True, self.settings.bishop_path(black=True)],
            ['d8', ShittyQueen, True, self.settings.queen_path(black=True)],
            ['e8', ShittyKing, True, self.settings.king_path(black=True)],
            ['f8', ShittyBishop, True, self.settings.bishop_path(black=True)],
            ['g8', ShittyKnight, True, self.settings.knight_path(black=True)],
            ['h8', ShittyRook, True, self.settings.rook_path(black=True)],
            ['a7', ShittyPawn, True, self.settings.pawn_path(black=True)],
            ['b7', ShittyPawn, True, self.settings.pawn_path(black=True)],
            ['c7', ShittyPawn, True, self.settings.pawn_path(black=True)],
            ['d7', ShittyPawn, True, self.settings.pawn_path(black=True)],
            ['e7', ShittyPawn, True, self.settings.pawn_path(black=True)],
            ['f7', ShittyPawn, True, self.settings.pawn_path(black=True)],
            ['g7', ShittyPawn, True, self.settings.pawn_path(black=True)],
            ['h7', ShittyPawn, True, self.settings.pawn_path(black=True)],

            # white
            ['a2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['b2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['c2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['d2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['e2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['f2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['g2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['h2', ShittyPawn, False, self.settings.pawn_path(black=False)],
            ['a1', ShittyRook, False, self.settings.rook_path(black=False)],
            ['b1', ShittyKnight, False, self.settings.knight_path(black=False)],
            ['c1', ShittyBishop, False, self.settings.bishop_path(black=False)],
            ['d1', ShittyQueen, False, self.settings.queen_path(black=False)],
            ['e1', ShittyKing, False, self.settings.king_path(black=False)],
            ['f1', ShittyBishop, False, self.settings.bishop_path(black=False)],
            ['g1', ShittyKnight, False, self.settings.knight_path(black=False)],
            ['h1', ShittyRook, False, self.settings.rook_path(black=False)],
        ]

        self.reset()

    def reset(self) -> NoReturn:
        """reset the board to a new game state"""

        self.clear()
        for piece in self.initial_piece_layout:
            if piece[2]:
                self.sprite_group_black.add(piece[1](
                    piece[2],
                    self.logic.coords_to_rect(piece[0]),
                    piece[0],
                    piece[3]))
            else:
                self.sprite_group_white.add(piece[1](
                    piece[2],
                    self.logic.coords_to_rect(piece[0]),
                    piece[0],
                    piece[3]))
        for sprite in itertools.chain(
                self.sprite_group_black,
                self.sprite_group_white
        ):
            self.sprite_group_all.add(sprite)

    def sprite_clicked(self, x: int, y: int, black: bool) -> bool:
        """returns true if sprite clicked"""

        if black:
            target_group = self.sprite_group_black
        else:
            target_group = self.sprite_group_white
        collisions = pygame.sprite.spritecollide(
            ShittyMousePointer(x, y),
            target_group,
            False
        )
        if len(collisions) == 1:
            return True
        return False

    def click_to_sprite(
            self,
            x: int,
            y: int,
            black: bool
    ) -> Union[ShittyPiece, None]:
        """returns piece sprite if clicked, or None"""

        if black:
            target_group = self.sprite_group_black
        else:
            target_group = self.sprite_group_white
        collisions = pygame.sprite.spritecollide(
            ShittyMousePointer(x, y),
            target_group,
            False
        )
        if len(collisions) == 1:
            return collisions[0]
        return None

    def coords_to_sprite(self, coords: str) -> Union[ShittyPiece, None]:
        """
        pass chess coords, returns sprite if sprite exists at coords
        else returns None
        """

        return self.sprite_group_all.coords_to_sprite(coords)

    # rename this method
    def sprite_exists_all(self, coords: str) -> bool:
        """returns True if sprite any sprite at coords, else returns False"""

        return self.sprite_group_all.sprite_exists(coords)

    # rename this method
    def sprite_exists_black(self, coords: str) -> bool:
        """returns True if any black sprite is at coords, else returns False"""

        return self.sprite_group_black.sprite_exists(coords)

    # rename this method
    def sprite_exists_white(self, coords: str) -> bool:
        """returns True if any white sprite is at coords, else returns False"""

        return self.sprite_group_white.sprite_exists(coords)

    def draw(self) -> NoReturn:
        """draw all the pieces"""

        self.sprite_group_all.draw(self.screen)

    def clear(self) -> NoReturn:
        """
        remove all the pieces from the sprite group containers
        this will clear the board of all pieces
        """

        self.sprite_group_black.empty()
        self.sprite_group_white.empty()
        self.sprite_group_all.empty()

    def resize(self) -> NoReturn:
        """
        reposition all the pieces to their current correct position
        this should be used if the board size is changed, or headers
        are disabled or enabled, as that will change the board size
        """

        for sprite in self.sprite_group_all:
            tmp_rect = self.logic.coords_to_rect(sprite.coords)
            sprite.set_rect(pygame.Rect(
                tmp_rect.left,
                tmp_rect.top,
                sprite.rect.width,
                sprite.rect.height
            ))
