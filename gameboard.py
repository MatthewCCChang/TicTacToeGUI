class BoardClass:
    """A class to store the user moves on a gameboard
    
    Attributes:
        username_one(str): The user's username.
        wins(int): The number of wins the user has.
        ties(int): The number of ties the user has.
        loss(int): The number of losses the user has.
        total_games(int): The number of games the user has played.
        text(2D array): The gameboard.
    """
    
    def __init__(self,username_one: str="",wins:int=0,ties:int=0,loss:int=0) -> None:
        """Make a gameboard.
        
        Args:
            username_one(str): The user's username.
            wins(int): The number of wins the user has.
            ties(int): The number of ties the user has.
            loss(int): The number of losses the user has.
        """
        self.username_one=username_one
        self.wins=wins
        self.ties=ties
        self.losses=loss
        self.total_games=wins+ties+loss
        self.text=[["0","1","2"],["3","4","5"],["6","7","8"]]

    def updateGamesPlayed(self)->None:
        """Increment the number of games played by one."""
        self.total_games+=1
    
    def resetGameBoard(self)->None:
        """Resets the gameboard to original state."""
        self.text=[["0","1","2"],["3","4","5"],["6","7","8"]]
        
    def printGameBoard(self)->None:
        """Prints the gameboard for user to visualize."""
        for i in self.text:
            print(i)
        

    def updateGameBoard(self,row: int=0, column: int=0,player: str="x")->bool:
        """Updates the gameboard with a user move.
        
        If the input is invalid or a move has already been made in that position, will return false.
        If the input is valid, will update the gameboard with the position and return true."""
        value=False
        if (row!=0 and row!=1 and row!=2) or (column!=0 and column!=1 and column!=2):
            print("Please enter a number between 0 and 2:")
        elif self.text[row][column]=="O" or self.text[row][column]=="X":
            print("Please don't enter in a spot already taken")
        else:
            self.text[row][column]=player.upper()
            value=True
        return value

    def isWinner(self)->str:
        """Determines if a user has won.
        
        Returns different strings to differentiate between who won or no one has won yet."""
        winner="none"
        for i in range(len(self.text)-1):
            if self.text[i][0]==self.text[i][1]==self.text[i][2]:
                winner=self.text[i][0]
        for j in range(len(self.text[0])-1):
            if self.text[0][j]==self.text[1][j]==self.text[2][j]:
                winner=self.text[0][j]
        if self.text[0][0]==self.text[1][1]==self.text[2][2]:
            winner=self.text[0][0]
        if self.text[0][2]==self.text[1][1]==self.text[2][0]:
            winner=self.text[0][2]
        return winner

    def incrementWins(self)->None:
        """Increment number of wins by one."""
        self.wins+=1
        
    def incrementLoss(self)->None:
        """Increment number of losses by one."""
        self.losses+=1

    def incrementTies(self)->None:
        """Increment number of ties by one."""
        self.ties+=1
        
    def boardIsFull(self)->bool:
        """Checks whether the board is full"""
        is_full =False
        count=0
        for i in range(len(self.text)):
            for j in self.text[i]:
                if j=="O" or j=="X":
                    count+=1
        if count==9:
            is_full=True
        return is_full
            

    def printStats(self,user_two: str,winner:str)->None: 
        """Prints out the user stats.
        
        Prints out user's username, opponent's username, the winner of the last game,
        the number of games played, the number of wins the user has, the number of losses
        the user has, and the number of ties the user has."""
        print("Self: "+self.username_one+" "+"Opponent: "+user_two+" "+"Winner: "+winner+" ")
        print("Games: "+str(self.total_games)+" Wins: "+str(self.wins)+" Losses: "+str(self.losses)+" Ties: "+str(self.ties))