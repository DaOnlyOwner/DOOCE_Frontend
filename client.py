import lib.dooce as dc
import tkinter as tk
import platform 
import pygame as pg
import io

pieces = {}
SIZE = 640

class BoardGUI:
    def __init__(self,as_black, game):
        self.as_black = as_black
        self.game = game
        self.screen = pg.display.set_mode((SIZE,SIZE),pg.NOFRAME)
        self.clock = pg.time.Clock()
        self.square_size = SIZE / 8

    def render_board(self):
        idx = 0
        if self.as_black:
            idx = 1
        alternating_colors = [pg.Color("lightgreen"),pg.Color("darkgreen")]
        for x in range(8):
            for y in range(8):
                pg.draw.rect(self.screen, alternating_colors[idx],(x*self.square_size,y*self.square_size,self.square_size,self.square_size))
                idx = 1-idx            
            idx = 1-idx

    def render_pieces(self):
        for x,rank in enumerate(self.game.get_board().as_mailbox()):
            for y,piece in enumerate(rank):
                if not piece:
                    continue
                id_ = (piece.type,piece.color)
                img = pieces[id_]
                self.screen.blit(img,(x*self.square_size-img.get_width()/5,y*self.square_size+img.get_height()/15))


    def render(self):
        self.screen.fill(pg.Color("white"))
        self.render_board()
        self.render_pieces()
        self.clock.tick(60)
        pg.display.flip()
        

# https://stackoverflow.com/questions/65649933/display-png-from-string-on-python-pygame
def load_image(path):
    with open(path, 'r') as file:
        img = pg.image.load(file)
        #return img
        img = pg.transform.smoothscale(img,(0.135*img.get_width(),0.135*img.get_height()))
        return img

def main():
    pg.init()
    piece_paths = [((dc.PieceType.queen,dc.Color.white),"pieces/wQ.png"),
    ((dc.PieceType.rook,dc.Color.white),"pieces/wR.png"),
    ((dc.PieceType.bishop,dc.Color.white),"pieces/wB.png"),
    ((dc.PieceType.knight,dc.Color.white),"pieces/wN.png"),
    ((dc.PieceType.king,dc.Color.white),"pieces/wK.png"),
    ((dc.PieceType.pawn,dc.Color.white),"pieces/wP.png"),

    ((dc.PieceType.queen,dc.Color.black),"pieces/bQ.png"),
    ((dc.PieceType.rook,dc.Color.black),"pieces/bR.png"),
    ((dc.PieceType.bishop,dc.Color.black),"pieces/bB.png"),
    ((dc.PieceType.knight,dc.Color.black),"pieces/bN.png"),
    ((dc.PieceType.king,dc.Color.black),"pieces/bK.png"),
    ((dc.PieceType.pawn,dc.Color.black),"pieces/bP.png")]
    for id_,path in piece_paths:
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