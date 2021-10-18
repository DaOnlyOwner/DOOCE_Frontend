from pygame.mouse import get_pos
import lib.dooce as dc
import tkinter as tk
import pygame as pg
import threading as th

pieces = {}
SIZE = 640
piece_offsets_x = {dc.PieceType.bishop:7,dc.PieceType.knight:7,dc.PieceType.pawn:17,dc.PieceType.king:7,dc.PieceType.rook:14,dc.PieceType.queen:5}
piece_offsets_y = {dc.PieceType.bishop:6,dc.PieceType.knight:6,dc.PieceType.pawn:10,dc.PieceType.king:8,dc.PieceType.rook:12.9,dc.PieceType.queen:11}


class BoardGUI:
    def __init__(self,as_black, gameplay):
        self.as_black = as_black
        self.game = gameplay.get_game()
        self.gameplay = gameplay
        self.screen = pg.display.set_mode((SIZE,SIZE))
        self.clock = pg.time.Clock()
        self.square_size = SIZE / 8
        self.from_=None
        self.delta = (0,0)
        self.lastMP = (0,0)
        self.running = True

    def render_board(self):
        idx = 0
        if self.as_black:
            idx = 1
        alternating_colors = [pg.Color("#eeeed2"),pg.Color("#769656")]
        for x in range(8):
            for y in range(8):
                pg.draw.rect(self.screen, alternating_colors[idx],(x*self.square_size,y*self.square_size,self.square_size,self.square_size))
                idx = 1-idx            
            idx = 1-idx
    
    def stop(self):
        self.running = False

    def get_pos_of_piece(self,x,y,pt):
        offset_x = piece_offsets_x[pt]
        offset_y = piece_offsets_y[pt]
        if not self.as_black: 
            return (x*self.square_size+offset_x,y*self.square_size+offset_y)
        else: 
            return ((8-x)*self.square_size+offset_x,y*self.square_size+offset_y)

    def render_pieces(self):
        for x,rank in enumerate(self.game.get_board().as_mailbox()):
            for y,piece in enumerate(rank):
                if not piece:
                    continue
                id_ = (piece.type,piece.color)
                img = pieces[id_]
                if((x,y) != self.from_):
                    if not self.as_black:
                        self.screen.blit(img,self.get_pos_of_piece(x,y,piece.type))
                    else:
                        self.screen.blit(img,self.get_pos_of_piece(x,y,piece.type))
        if self.from_ != None:
            piece = self.game.get_board().as_mailbox()[self.from_[0]][self.from_[1]]
            id_ = piece.type,piece.color
            img = pieces[id_]
            x,y = self.from_
            self.screen.blit(img,(self.get_pos_of_piece(x,y,piece.type)[0]+self.delta[0],self.get_pos_of_piece(x,y,piece.type)[1]+self.delta[1]))

    def update_click(self,event):
        # Detect if clicked on a piece
        if event.type == pg.MOUSEBUTTONDOWN and event.button == 1 and self.from_ == None: # Pressed the left mb
            click_pos = pg.mouse.get_pos()
            for x, rank in enumerate(self.game.get_board().as_mailbox()):
                for y,piece in enumerate(rank):
                    if not piece:
                        continue
                    id_ = (piece.type,piece.color)
                    img = pieces[id_]
                    img_rect = pg.Rect(self.get_pos_of_piece(x,y,piece.type)[0],self.get_pos_of_piece(x,y,piece.type)[1],img.get_width(),img.get_height())
                    if img_rect.collidepoint(click_pos):
                        self.from_ = (x,y)
                        self.lastMP = pg.mouse.get_pos()
                        #self.delta = (pg.mouse.get_pos()[0]-self.get_pos_of_piece(x,y,piece.type)[0],pg.mouse.get_pos()[1]-self.get_pos_of_piece(x,y,piece.type)[1])

    def update_let_go(self,event):
        # Detect if let go over another field
        if event.type == pg.MOUSEBUTTONUP and self.from_ != None:
            # Get the index of the field
            to = (-1,-1)
            for x in range(8):
                for y in range(8):
                    r = pg.Rect(x*self.square_size,y*self.square_size,self.square_size,self.square_size)
                    if(r.collidepoint(pg.mouse.get_pos())):
                        to = (x,y)
            from_ = self.from_
            self.from_ = None
            self.delta = (0,0)
            return (from_,to)
        return ((-1,-1),(-1,-1))
        
    def update_drag(self,event):
        # Detect if user drags the piece
        if event.type == pg.MOUSEMOTION and self.from_ != None:
            pos = pg.mouse.get_pos()
            self.delta = (self.delta[0]+pos[0]-self.lastMP[0],self.delta[1]+pos[1]-self.lastMP[1])
            self.lastMP = pos
    
    def render(self):
        self.screen.fill(pg.Color("white"))
        self.render_board()
        self.render_pieces()
        self.clock.tick(60)
        pg.display.flip()

    def render_and_update(self):
        from_,to = (-1,-1),(-1,-1)
        for e in pg.event.get():
            if e.type == pg.QUIT:
                self.running = False
            self.update_click(e)
            from_,to = self.update_let_go(e)
            self.update_drag(e)
        if from_[0] != -1:
            idx_from = from_[0]+8*from_[1]
            idx_to = to[0]+8*to[1]
            from_str = dc.sq_idx_to_str(idx_from)
            to_str = dc.sq_idx_to_str(idx_to)
            mv_str = from_str+to_str
            mv = self.gameplay.get_game().from_dooce_algebraic_notation(mv_str)
            if mv != None:
                self.gameplay.incoming_move(mv)
                self.gameplay.pick_next_move()

        self.render()    

    def mainloop(self):
        while self.running:
            self.render_and_update()  


# https://stackoverflow.com/questions/65649933/display-png-from-string-on-python-pygame
def load_image(path):
    with open(path, 'r') as file:
        img = pg.image.load(file)
        #return img
        img = pg.transform.smoothscale(img,(0.14*img.get_width(),0.14*img.get_height()))
        return img

class GUI:
    def __init__(self):
        self.root = tk.Tk()
        #self.root.geometry("640x640")
        self.root.title("Options DOOCE")
        tk.Label(self.root,text="Hashtable size").grid(row=0,column=0)
        self.tt_size = tk.Entry(self.root)
        self.tt_size.grid(row=0,column=1)
        tk.Label(self.root,text="Minutes to play").grid(row=1,column=0)
        self.mtp = tk.Entry(self.root)
        self.mtp.grid(row=1,column=1)
        tk.Button(self.root,text="New game",command=self.new_game_default).grid(row=2)
        tk.Button(self.root,text="New game from FEN").grid(row=3,column=0)
        self.fenEntry = tk.Entry(self.root).grid(row=3,column=1,ipadx=100)
        tk.Label(self.root, text="Move Info: ").grid(row=5,column=0)
        tk.Label(self.root, text="PV: ").grid(row=6,column=0)
        self.pv_label = tk.Label(self.root, text="")
        self.pv_label.grid(row=6,column=1)
        tk.Label(self.root,text="Depth: ").grid(row=7,column=0)
        self.depth_label = tk.Label(self.root,text="")
        self.depth_label.grid(row=7,column=1)
        tk.Label(self.root,text="Score: ").grid(row=8,column=0)
        self.score_label = tk.Label(self.root,text="")
        self.score_label.grid(row=8,column=1)

        self.boardGUIThread = None
        self.boardGUI = None

    def mainloop(self):
        self.root.mainloop()
        if self.boardGUI != None:
            self.boardGUI.stop()
            self.boardGUIThread.join()

    def pygame_mainloop(self,gameplay):
        pg.init()
        self.boardGUI = BoardGUI(False,gameplay)
        self.boardGUI.mainloop()
        pg.display.quit()
        pg.quit()

    def new_game_default(self):
        if self.boardGUI != None:
            self.boardGUI.stop()
            self.boardGUIThread.join()
            self.boardGUI = None
        try:
            tt_size_str = self.tt_size.get()
            mtp_str = self.mtp.get()
            tt_size = 0
            mtp = 0
            if tt_size_str == "": 
                print("Using standard values for transposition table size")
                tt_size = 1 << 20
            if mtp_str == "":
                print("Using standard values for minutes to think")
                mtp = 5
            if tt_size_str != "" and mtp_str != "":
                tt_size = int(eval(self.tt_size.get()))
                mtp = int(self.mtp.get())
            gameplay = dc.make_gameplay_st(dc.Game(),mtp,tt_size)
            self.boardGUIThread = th.Thread(target=self.pygame_mainloop,args=[gameplay])
            self.boardGUIThread.start()
        except Exception as e:
            print(e)
        



def main():
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

    gui = GUI()
    gui.mainloop()
    
    

if __name__ == "__main__":
    main()