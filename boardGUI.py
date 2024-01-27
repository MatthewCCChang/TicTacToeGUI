import gameboard as board
import tkinter as tk
import player1 as p1
import player2 as p2
import socket

class BoardGUI:
    """A class to handle the GUI for the game."""
    #to store gameboard obj
    board_var=0
    #to store tk obj
    master=0
    
    def __init__(self,title:str) -> None:
        """Make a GUI.
        
        Args:
        title(str): The name of the player starting the GUI.
        """
        self.board_one=board.BoardClass()
        self.board_two=board.BoardClass()
        self.value=False
        if title=="player1":
            self.value=True
        self.setCanvas(title)
        self.initVar()
        self.setName(title)
        self.createText("Please enter the host info:")
        self.createInputIP()
        self.createText("Please enter the port number:")
        self.createInputPort()
        if self.value:
            self.createText("Please enter your username:")
            self.createInputName()
        self.createButton()
        self.showGUI()
        
    def initVar(self):
        """Initializa variables."""
        self.port=0
        self.ip=""
        self.username=""
        self.input1=tk.StringVar()
        self.input2=tk.IntVar()
        self.input3=tk.StringVar()
        
    def setHost(self,host_info:str)->None:
        """Set the host information to input host_info."""
        self.host=host_info  #going to be string
        
    def getHost(self)->str:
        """Get the host information."""
        return self.host
    
    def setPort(self,port_num:str)->None:
        """Set the port number to input port_num."""
        self.port=int(port_num)
        
    def getPort(self)->int:
        """Get the port number."""
        return self.port
    
    def setName(self,input:str="player2"):
        """Set the name of the user."""
        self.username=input
    
    def getName(self)->str:
        """Get the name of the user."""
        return self.username
    
    def setCanvas(self,username:str)->None:
        """Set up the canvas."""
        self.master=tk.Tk()
        self.master.title(username)
        self.master.resizable(1,1)
        self.master.geometry("500x500")
        
    def createText(self,display:str):
        """Create a label with text."""
        self.label=tk.Label(self.master,text=display).pack()
        return self.label
        
    def createInputIP(self):
        """Create entry for inputing IP address."""
        #string"Enter IP Address"
        self.entry1=tk.Entry(self.master,textvariable=self.input1).pack()
        
       
    def createInputPort(self):
        """Create entry for inputing port number."""
        #"Enter Port Number"
        self.entry2=tk.Entry(self.master,textvariable=self.input2).pack()
    
    def createInputName(self):
        """Create entry for inputing username."""
        #"Enter Username"
        self.entry3=tk.Entry(self.master,textvariable=self.input3).pack()
        
    
    def destroyWin(self):
        """Destroys the current window, stores the information, and establishes connection."""
        self.master.destroy()
        self.setHost(self.input1.get())
        self.setPort(self.input2.get())
        if self.getName()=="player1":
            self.setName(self.input3.get())
            self.board_one.setUser(self.getName())
        
        #use p1 and p2 to setup server and client, call the functions they have for setting up logic
        if self.getName()=="player2":
            self.board_two.setUser("player2")
            s2=p2.receiveInfo(self.getHost(),self.getPort())
            self.p_one_name=p2.receiveName(s2)
            self.boardWindow()
            self.storeSocket(s2)
            row,col=p2.receiveMove(s2,self.board_two) 
            self.updateButton(row,col,"X")
            self.updateInfo("player2 turn")

        else:
            self.boardWindow()
            s1=p1.sendAndReceive(self.getHost(),self.getPort(),self.getName())
            self.storeSocket(s1)
            self.updateInfo("player1 turn")
        
    def storeSocket(self,s:socket)->None:
        """Stores the socket."""
        self.sock=s
        
    def getSocket(self)->socket:
        """Retrieves the socket."""
        return self.sock
        
    def boardWindow(self):
        """Sets up the board window"""
        if self.getName()=="player2":
            self.setCanvas("board2")
        else:
            self.setCanvas("board1")
        self.createFrame()
        self.createTopLeftButton()
        self.createTopMidButton()
        self.createTopRightButton()
        self.createMidLeftButton()
        self.createMidMidButton()
        self.createMidRightButton()
        self.createBotLeftButton()
        self.createBotMidButton()
        self.createBotRightButton()
        self.createDisplayInfo()
        
    def playAgain(self,sock:socket):
        """Updates the GUI to beginning state of a game."""
        sock.send("Play Again".encode())
        # self.enterButton1.pack_forget()
        # self.enterButton2.pack_forget()
        self.right.pack_forget()
        self.right=tk.Frame(self.master,width=50, height=100,background="green")
        self.updateButton(0,0,"0")
        self.updateButton(0,1,"1")
        self.updateButton(0,2,"2")
        self.updateButton(1,0,"3")
        self.updateButton(1,1,"4")
        self.updateButton(1,2,"5")
        self.updateButton(2,0,"6")
        self.updateButton(2,1,"7")
        self.updateButton(2,2,"8")
        
        

    def createFrame(self):
        """Creates frames."""
        self.top=tk.Frame(self.master, width=300, height=80,background="blue")
        self.top.pack()
        self.mid=tk.Frame(self.master,width=300, height=80)
        self.mid.pack()
        self.bot=tk.Frame(self.master,width=300, height=80,bg="red")
        self.bot.pack()
        
        #create fourth frame on the right side for displaying info, have everything else fill to expand
        self.right=tk.Frame(self.master,width=50, height=100,background="green")
        #self.right.pack()
        
    
    def posButtonPressed(self,row:int,col:int)->int: #not updating upon button click
        """Updates the gameboard and button, sends and receives the moves while checking if someone won."""
        s=self.getSocket()
        self.input=""
        self.opponent=""
        value=True
        if self.getName()=="player2":
            self.input="O"
            self.opponent="X"
            self.switchButtonState()
            self.updateButton(row,col,self.input)
            self.updateInfo("player1 turn")
            self.board_two.updateGameBoard(row,col,self.input)
            p2.sendMove(s,row,col)
            self.master.update()
            #check winner
            if p2.playerTwoWin(self.board_two,self.board_two.isWinner()): #only reach when p2 wins, alr updated
                value=False
                self.setWinner("player2")
                self.board_two.updateGamesPlayed()
                self.p_won()
                self.master.update()
                self.board_two.resetGameBoard()
                self.gameStop(s) #this line doesn't run until y/n button clicked on p1
                self.master.update()
            #receive move
            if value:
                oppo_row,oppo_col=p2.receiveMove(s,self.board_two)
                self.updateInfo("player2 turn")
                self.updateButton(oppo_row,oppo_col,self.opponent)
            #check winner
                if p2.playerTwoWin(self.board_two,self.board_two.isWinner()):
                    self.setWinner(self.p_one_name)
                    self.board_two.updateGamesPlayed()
                    self.p_lose()
                    self.master.update()
                    self.board_two.resetGameBoard()
                    self.gameStop(s)
                    self.master.update()
                if self.board_two.boardIsFull():   
                    self.setWinner("Tie") 
                    self.board_two.incrementTies()
                    self.board_two.updateGamesPlayed()
                    self.p_tie()
                    self.master.update()
                    self.board_two.resetGameBoard()
                    self.gameStop(s)
                    self.master.update()
            #p2.sendAndReceiveMove(s,row,col,self.board_two)
        else:
            self.input="X"
            self.opponent="O"
            value=True
            self.switchButtonState()
            self.updateButton(row,col,self.input)
            self.updateInfo("player2 turn")
            self.board_one.updateGameBoard(row,col,self.input)
            p1.sendMove(s,row,col)
            self.master.update()
            #check winner
            if p1.playerOneWin(self.board_one,self.board_one.isWinner()):
                value=False
                self.setWinner(self.getName())
                self.board_one.updateGamesPlayed()
                self.p_won()
                self.master.update()
                self.board_one.resetGameBoard()
                self.gameStop(s)
                self.master.update()
            elif self.board_one.boardIsFull():   
                value=False 
                self.setWinner("Tie")
                self.board_one.incrementTies()
                self.board_one.updateGamesPlayed()
                self.p_tie()
                self.master.update()
                self.board_one.resetGameBoard()
                self.gameStop(s)
                self.master.update()
            if value:
                oppo_row,oppo_col=p1.receiveMove(s,self.board_one)
                self.updateInfo("player1 turn")
                self.updateButton(oppo_row,oppo_col,self.opponent)
                self.master.update()
                #check winner
                if p1.playerOneWin(self.board_one,self.board_one.isWinner()):
                    self.setWinner("player2")
                    self.board_one.updateGamesPlayed()
                    self.p_lose()
                    self.master.update()
                    self.board_one.resetGameBoard()
                    self.gameStop(s)
                    self.master.update()
        self.switchButtonState()
        
    def switchButtonState(self):
        """ENables and disables the button."""
        state=self.topLeftButton["state"]
        if state=="normal":
            self.topLeftButton.config(state="disabled")
            self.topMidButton.config(state="disabled")
            self.topRightButton.config(state="disabled")
            self.midLeftButton.config(state="disabled")
            self.midMidButton.config(state="disabled")
            self.midRightButton.config(state="disabled")
            self.botLeftButton.config(state="disabled")
            self.botMidButton.config(state="disabled")
            self.botRightButton.config(state="disabled")
        elif state =="disabled":
            self.topLeftButton.config(state="normal")
            self.topMidButton.config(state="normal")
            self.topRightButton.config(state="normal")
            self.midLeftButton.config(state="normal")
            self.midMidButton.config(state="normal")
            self.midRightButton.config(state="normal")
            self.botLeftButton.config(state="normal")
            self.botMidButton.config(state="normal")
            self.botRightButton.config(state="normal")
    
    def updateButton(self,row:int,col:int,input:str):
        """Updates the button text to O/X."""
        if row==0:
            if col==0:
                self.topLeftButton.config(text=input)
            elif col==1:
                self.topMidButton.config(text=input)
            elif col==2:
                self.topRightButton.config(text=input)
        elif row==1:
            if col==0:
                self.midLeftButton.config(text=input)
            elif col==1:
                self.midMidButton.config(text=input)
            elif col==2:
                self.midRightButton.config(text=input)
        elif row==2:
            if col==0:
                self.botLeftButton.config(text=input)
            elif col==1:
                self.botMidButton.config(text=input)
            elif col==2:
                self.botRightButton.config(text=input)
    
    def p_won(self):
        """Display label when a player has won."""
        self.play1=tk.Label(self.master,text="You Won. Play Again?")
        self.play1.pack(in_=self.right)
        self.right.pack()
        
        
    def p_lose(self):
        """Display label when a player has lost."""
        self.play2=tk.Label(self.master,text="You Lost. Play Again?")
        self.play2.pack(in_=self.right)
        self.right.pack()
        
    def p_tie(self):
        """Display label when a player has tied."""
        self.play3=tk.Label(self.master,text="You Tied. Play Again?")
        self.play3.pack(in_=self.right)
        self.right.pack()
    
    def gameStop(self,s:socket):
        """Checks whether player wants to play again and acts based on the response."""
        if self.getName()=="player2":
            data=s.recv(1024).decode()
            if data=="Play Again":
                self.right.pack_forget()
                self.master.update()
                self.right=tk.Frame(self.master,width=50, height=100,background="green")
                self.updateButton(0,0,"0")
                self.updateButton(0,1,"1")
                self.updateButton(0,2,"2")
                self.updateButton(1,0,"3")
                self.updateButton(1,1,"4")
                self.updateButton(1,2,"5")
                self.updateButton(2,0,"6")
                self.updateButton(2,1,"7")
                self.updateButton(2,2,"8")
                self.master.update()
                row,col=p2.receiveMove(s,self.board_two) 
                self.updateButton(row,col,"X")
                self.updateInfo("player2 turn")
                self.master.update()
            elif data=="Fun Times":
                self.final_two=tk.Label(self.master,text=self.board_two.printStats(self.p_one_name,self.getWinner()))
                self.final_two.pack(in_=self.right, side="bottom")
        else:
            self.yesButton(s)
            self.noButton(s)
    
    def setWinner(self,win:str):
        """Stores the winner to a string."""
        self.winner=win
        
    def getWinner(self)->str:
        """Returns the winner."""
        return self.winner
    
    def createButton(self):
        """Creates a button to submit info about the connection."""
        self.enterButton=tk.Button(self.master,text="Enter",command=self.destroyWin)
        self.enterButton.pack()
       
    def yesButton(self,s:socket):
        """Creates a button that says yes to play again prompt."""
        self.enterButton1=tk.Button(self.master,text="yes",command=lambda:self.playAgain(s))
        self.enterButton1.pack(in_=self.right)
        
    def noButton(self,s:socket):
        """Creates a button that says no to play again prompt."""
        self.enterButton2=tk.Button(self.master,text="no",command=lambda:self.quitGame(s))
        self.enterButton2.pack(in_=self.right)
    
    def quitGame(self,sock:socket):
        """Prints the stats for player1 and closes the socket."""
        sock.send("Fun Times".encode())
        self.final_one=tk.Label(self.master,text=self.board_one.printStats("player2",self.getWinner()))
        self.final_one.pack(in_=self.right, side="bottom")
        sock.close()
    
    def createDisplayInfo(self):
        """Creates a label for displaying who's turn it is."""
        self.display=tk.Label(self.master,text='')
        self.display.pack()
        
    def updateInfo(self,info:str):
        """Updates who's turn it is."""
        self.display.config(text=info)
    
    def createTopLeftButton(self):
        """Creates the top left button."""
        self.topLeftButton=tk.Button(self.master,text="0",command=lambda: self.posButtonPressed(0,0))
        self.topLeftButton.pack(in_=self.top,side="left")

    def createTopMidButton(self):
        """Creates the top middle button."""
        self.topMidButton=tk.Button(self.master,text="1",command=lambda:self.posButtonPressed(0,1))
        self.topMidButton.pack(in_=self.top,side="left")
    
    def createTopRightButton(self):
        """Creates the top right button."""
        self.topRightButton=tk.Button(self.master,text="2",command=lambda:self.posButtonPressed(0,2))
        self.topRightButton.pack(in_=self.top,side="left")
    
    def createMidLeftButton(self):
        """Creates the middle left button."""
        self.midLeftButton=tk.Button(self.master,text="3",command=lambda:self.posButtonPressed(1,0))
        self.midLeftButton.pack(in_=self.mid,side="left")
    
    def createMidMidButton(self):
        """Creates the middle middle button."""
        self.midMidButton=tk.Button(self.master,text="4",command=lambda:self.posButtonPressed(1,1))
        self.midMidButton.pack(in_=self.mid,side="left")
        
    def createMidRightButton(self):
        """Creates the middle right button."""
        self.midRightButton=tk.Button(self.master,text="5",command=lambda:self.posButtonPressed(1,2))
        self.midRightButton.pack(in_=self.mid,side="left")
    
    def createBotLeftButton(self):
        """Creates the bottom left button."""
        self.botLeftButton=tk.Button(self.master,text="6",command=lambda:self.posButtonPressed(2,0))
        self.botLeftButton.pack(in_=self.bot,side="left")
        
    def createBotMidButton(self):
        """Creates the bottom middle button."""
        self.botMidButton=tk.Button(self.master,text="7",command=lambda:self.posButtonPressed(2,1))
        self.botMidButton.pack(in_=self.bot,side="left")
    
    def createBotRightButton(self):
        """Creates the bottom right button."""
        self.botRightButton=tk.Button(self.master,text="8",command=lambda:self.posButtonPressed(2,2))
        self.botRightButton.pack(in_=self.bot,side="left")
    
    def showGUI(self):
        """Gets the GUI running."""
        self.master.mainloop() 
