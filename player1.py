import socket
import gameboard

def player_two_host_info()->str:
    """Prompts the user for the IP address of player2 and returns that information."""
    hostname=input("Please enter the hostname/IP address of player 2: ")
    return hostname

def player_two_port()->str:
    """Prompts the user for the port number to connect to player2 and returns that information."""
    port_number=input("Please enter the port number you'd like to use to connect with player 2: ")
    return int(port_number)

def player_one_username()->str:
    """Prompts the user for the username and returns that information."""
    user_name=input("Please enter your username: ").lower()
    return user_name

def sendInfo(ip: str="", port_number: int=0, user_name: str="")->socket:
    """Upon successful connection to player2, sends the username and if not, calls makeConnectionAgain()."""
    try:
        s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        s.connect((ip,port_number))
        s.send(user_name.encode())
        return s
    except socket.error:
        sock=makeConnectionAgain()
        return sock

def receivedName(sock:socket)->str:
    '''Returns the username sent by player2.'''
    player_two_username=sock.recv(1024).decode()
    return player_two_username

def playAgain(s:socket)->bool:
    '''Prompts the user to play again and , sends messages to player2 while returning Boolean value.'''
    value=True
    response=input("Would you like to play again? ")
    if response.upper()=="Y":
        s.send("Play Again".encode())
    if response.upper()=="N":
        s.send("Fun Times".encode())
        value=False
    return value
    
def makeConnectionAgain()->socket:
    '''Prompts the user to reconnect.'''
    response=input("Try to make connection again? y/n ")
    if response=="y":
        sock=sendInfo(player_two_host_info(),player_two_port(),player_one_username())   
        return sock
    elif response=="n":
        quit()
    
def makeMove(player_one:gameboard.BoardClass())->int:
    '''Prompts the user to make a valid move and prints the gameboard to visualize.'''
    player_one.printGameBoard()
    while True:
        row=input("Which row would you like to place o(0~2): ")
        column=input("Which column would you like to place o(0~2): ")
        if player_one.updateGameBoard(int(row), int(column),"X"):
            break
    player_one.printGameBoard()
    print("-"*14)
    return row, column

def sendMove(sock:socket,row:int,column:int)->None:
    '''Sends a string over the socket.'''
    sock.send((str(row)+str(column)).encode())

def receiveMove(sock: socket,player_one:gameboard.BoardClass())->None:
    '''Updates the gameboard with the information received.'''
    data=sock.recv(1024).decode()
    player_one.updateGameBoard(int(data[0]),int(data[1]),"O")

def playerOneWin(player_one:gameboard.BoardClass(),win: str="none")->bool:
    '''Depending on whether a winner was found, returns different Boolean values and messages while updating wins and losses.'''
    value=False
    if win=="X":
        print("You Win!")
        player_one.incrementWins()
        value=True
    elif win=="O":
        print("You Lose!")
        player_one.incrementLoss()
        value=True
    return value

def runProgram()->None:
    '''Runs the program in main.'''
    p_two_ip=player_two_host_info()
    p_two_port=player_two_port()
    p_one_username=player_one_username()
    s=sendInfo(p_two_ip,p_two_port,p_one_username)
    print(s)
    p_two_name=receivedName(s)
    print("Connected to "+p_two_name)
    player_one=gameboard.BoardClass(p_one_username)
    value=True
    while value: 
        row,column=makeMove(player_one)
        sendMove(s,row,column)
        if playerOneWin(player_one,player_one.isWinner()):
            player_one.printGameBoard()
            player_one.updateGamesPlayed()
            player_one.resetGameBoard()
            value=playAgain(s)
            if value==False:
                player_one.printStats(p_two_name,p_one_username)
                s.close()
                break
            if value==True:
                continue
        if player_one.boardIsFull():
            player_one.printGameBoard()
            print("Tie!")
            player_one.updateGamesPlayed()
            player_one.resetGameBoard()
            player_one.incrementTies()
            value=playAgain(s)
            if value==False:
                player_one.printStats(p_two_name,"Tie")
                s.close()
                break
            if value==True:
                continue
        receiveMove(s,player_one)
        if playerOneWin(player_one,player_one.isWinner()):
            player_one.printGameBoard()
            player_one.updateGamesPlayed()
            player_one.resetGameBoard()
            value=playAgain(s)
            if value==False:
                player_one.printStats(p_two_name,p_two_name)
                s.close()
                break
            if value==True:
                continue
        if player_one.boardIsFull():
            player_one.printGameBoard()
            print("Tie!")
            player_one.updateGamesPlayed()
            player_one.resetGameBoard()
            player_one.incrementTies()
            value=playAgain(s)
            if value==False:
                player_one.printStats(p_two_name,"Tie")
                s.close()
                break
            if value==True:
                continue


if __name__=="__main__":
    runProgram()

    