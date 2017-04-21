#!/usr/bin/python
# AppelHaken.py
"""
    Copyright (C) 2010  Peter Hewitt

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

"""
import g,pygame,utils,gtk,sys,buttons,ah,slider

class AppelHaken:

    def __init__(self):
        self.score=0; self.level=1
        self.journal=True # set to False if we come in via main()
        self.canvas=None # set to the pygame canvas if we come in via activity.py
        self.keys={pygame.K_1:1,pygame.K_2:2,pygame.K_3:3,pygame.K_4:4}

    def display(self):
        g.screen.fill((0,0,70))
        buttons.draw()
        self.grid.draw()
        self.slider.draw()
        utils.display_number(g.score,self.score_cxy,g.font2,utils.CREAM)
        if self.grid.complete():
            utils.centre_blit(g.screen,g.smiley,self.smiley_cxy)

    def do_button(self,bu):
        if bu=='reset': self.grid.reset(); buttons.clear()
        elif bu=='new': self.grid.setup(); buttons.clear()
        else:
            if not self.grid.complete():
                self.grid.colour_ind=int(bu)

    def do_key(self,key):
        if key==pygame.K_o or key==265: self.do_button('new'); return
        if key==pygame.K_5 or key==263: self.do_button('reset'); return
        if not self.grid.complete():
            buttons.clear()
            if key in self.keys.keys():
                self.grid.colour_ind=self.keys[key]
                buttons.stay_down(str(self.grid.colour_ind))

    def buttons_setup(self):
        cx=g.sx(30.5)
        cy=g.sy(1.6); dy=g.sy(3)
        for i in range(1,5):
            buttons.Button(str(i),(cx,cy))
            cy+=dy
        buttons.Button('reset',(cx,g.sy(17.5)))
        buttons.Button('new',(cx,g.sy(20.5)))
        self.score_cxy=(cx,g.sy(14)); self.smiley_cxy=(g.sx(3),g.sy(20.5))

    def run(self):
        g.init()
        g.journal=self.journal
        if not self.journal:
            utils.load(); self.score=g.score; self.level=g.level
        else:
            g.score=self.score; g.level=self.level
        self.buttons_setup()
        if self.journal: # Sugar only
            a,b,c,d=pygame.cursors.load_xbm('my_cursor.xbm','my_cursor_mask.xbm')
            pygame.mouse.set_cursor(a,b,c,d)
        self.slider=slider.Slider(g.sx(16),g.sy(20.5),9,utils.GREEN)
        self.grid=ah.Grid()
        self.grid.new1(); self.grid.setup()
        going=True
        while going:
            # Pump GTK messages.
            while gtk.events_pending():
                gtk.main_iteration()

            # Pump PyGame messages.
            for event in pygame.event.get():
                if event.type==pygame.QUIT:
                    if not self.journal: utils.save()
                    going=False
                elif event.type == pygame.MOUSEMOTION:
                    g.redraw=True
                    if self.canvas<>None: self.canvas.grab_focus()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    g.redraw=True
                    if event.button==2: # centre button
                        if not self.journal:
                            g.version_display=not g.version_display
                    if event.button==1:
                        if self.grid.click():
                            pass
                        elif self.slider.mouse():
                            self.grid.new1(); self.grid.setup(); buttons.clear() # level changed
                        else:
                            bu=buttons.check()
                            if bu!='': self.do_button(bu)
                            else: self.grid.colour_ind=0
                elif event.type == pygame.KEYDOWN:
                    self.do_key(event.key); g.redraw=True
            if not going: break
            if self.grid.complete():
                buttons.clear()
            if g.redraw:
                self.display()
                if g.version_display: utils.version_display()
                pygame.display.flip()
                g.redraw=False
            self.score=g.score; self.level=g.level
            tf=False
            if pygame.mouse.get_focused(): tf=True
            pygame.mouse.set_visible(tf)
            g.clock.tick(40)

if __name__=="__main__":
    pygame.init()
    pygame.display.set_mode((800,600))
    game=AppelHaken()
    game.journal=False
    game.run()
    pygame.display.quit()
    pygame.quit()
    sys.exit(0)
