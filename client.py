import lib.dooce as dc
import tkinter as tk
import platform 
import pygame as pg
import io

pieces = {}

class BoardGUI:
    def __init__(self,as_black, game):
        self.as_black = as_black
        self.game = game
        self.screen = pg.display.set_mode((640,640),pg.NOFRAME)
        self.clock = pg.time.Clock()


    def render_board(self):
        idx = 0
        if self.as_black:
            idx = 1
        alternating_colors = [pg.Color("lightgreen"),pg.Color("darkgreen")]
        for x in range(8):
            for y in range(8):
                pg.draw.rect(self.screen, alternating_colors[idx],(x*80,y*80,80,80))
                idx = 1-idx            
            idx = 1-idx

    def render_pieces(self):
        for x,rank in enumerate(self.game.get_board().as_mailbox()):
            for y,piece in enumerate(rank):
                if not piece:
                    continue
                id_ = (piece.type,piece.color)
                p,c = id_
                if p == dc.PieceType.bishop and c == dc.Color.black:                    
                    img = pieces[id_]
                    self.screen.blit(img,(300,300))


    def render(self):
        self.screen.fill(pg.Color("white"))
        self.render_board()
        self.render_pieces()
        self.clock.tick(60)
        pg.display.flip()
        

# https://stackoverflow.com/questions/65649933/display-svg-from-string-on-python-pygame
def load_image(path):
    with open(path, 'r') as file:
        img = pg.image.load(file)
        return img
        img = pg.transform.smoothscale(img,(10*img.get_width(),10*img.get_height()))

def main():
    pg.init()
    piece_paths = [((dc.PieceType.queen,dc.Color.white),"pieces/wQ.svg"),
    ((dc.PieceType.rook,dc.Color.white),"pieces/wR.svg"),
    ((dc.PieceType.bishop,dc.Color.white),"pieces/wB.svg"),
    ((dc.PieceType.knight,dc.Color.white),"pieces/wN.svg"),
    ((dc.PieceType.king,dc.Color.white),"pieces/wK.svg"),
    ((dc.PieceType.pawn,dc.Color.white),"pieces/wP.svg"),

    ((dc.PieceType.queen,dc.Color.black),"pieces/bQ.svg"),
    ((dc.PieceType.rook,dc.Color.black),"pieces/bR.svg"),
    ((dc.PieceType.bishop,dc.Color.black),"pieces/bB.png"),
    ((dc.PieceType.knight,dc.Color.black),"pieces/bN.svg"),
    ((dc.PieceType.king,dc.Color.black),"pieces/bK.svg"),
    ((dc.PieceType.pawn,dc.Color.black),"pieces/bP.svg")]
    for id_,path in piece_paths:
        p,c = id_
        if p == dc.PieceType.bishop and c == dc.Color.black:
            pieces[id_] = load_image(path) 
    
    running = True
    game = dc.Game()
    boardGUI = BoardGUI(False,game)
    while running:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                running = False
        boardGUI.render()

if __name__ == "__main__":
    main()