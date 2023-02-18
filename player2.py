import socket
import gameboard

def hostInfo()->str:
    '''Prompts the user to enter the host name as input and returns the host name'''
    ip_address=input("Please enter the host name: ")
    port=int(input("What port number do you want to use: "))
    return ip_address,port

def receiveInfo(ip: str="", port_number: int=5001)->socket:
    '''Receives information of the hostname and port number, creates a server socket and makes a connection. 

    Upon successful connection, sends "player2" as username.'''
    s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.bind((ip,port_number))
    s.listen()
    conn, address= s.accept()  #conn is new socket obj
    return conn

def receiveName(conn:socket)->str:
    """Receives username through socket and returns the name while sending own name"""
    data=conn.recv(1024).decode() #the username
    conn.send("player2".encode())
    return data 

def makeMove(player_two: gameboard.BoardClass)->int:
    '''Accepts a gameboard object, prints the current gameboard, prompts the user for where to place their mark, then updates gameboard. '''
    player_two.printGameBoard()
    while True:
        row=input("Which row would you like to place o(0~2): ")
        column=input("Which column would you like to place o(0~2): ")
        if player_two.updateGameBoard(int(row), int(column),"O"):
            break
    player_two.printGameBoard()
    print("-"*14)
    return row, column 
    
def sendMove(sock:socket,row:int,column:int)->None:
    '''Sends the row and column number through socket object'''
    sock.send((str(row)+str(column)).encode())
    
    
def recieveMove(socket: socket,player_two:gameboard.BoardClass())->None:
    '''Receives data via socket and updates the gameboard'''
    data=socket.recv(1024).decode() 
    player_two.updateGameBoard(int(data[0]),int(data[1]),"X")
    
    
def playAgain(s:socket)->bool:
    '''Returns Boolean values based off of data received via socket'''
    value=False
    response = s.recv(1024).decode()
    if response =="Play Again":
        value=True
    if response =="Fun Times":
        value=False
    return value
    
def playerTwoWin(player_two: gameboard.BoardClass(),win: str="none")->bool:
    '''Checks whether a winner has been found and if yes, increments wins and losses'''
    value=False
    if win=="O":
        print("You Win!")
        player_two.incrementWins()
        value=True
    elif win=="X":
        print("You Lose!")
        player_two.incrementLoss()
        value=True
    return value
        
def runProgram()->None:
    '''Runs the program in main'''
    host,port=hostInfo()
    s=receiveInfo(host,port) 
    p_one_name=receiveName(s)
    print("Connected to "+p_one_name)
    player_two = gameboard.BoardClass("player2")
    value=True
    while (value): 
        recieveMove(s,player_two)
        if playerTwoWin(player_two,player_two.isWinner()):
            player_two.printGameBoard()
            player_two.updateGamesPlayed()
            player_two.resetGameBoard()
            value=playAgain(s)
            if value==False:    
                player_two.printStats(p_one_name,p_one_name)
                s.close()
                break
            if value==True:
                continue
        if player_two.boardIsFull():
            player_two.printGameBoard()
            print("Tie!")
            player_two.updateGamesPlayed()
            player_two.resetGameBoard()
            player_two.incrementTies()
            value=playAgain(s)
            if value==False:    
                player_two.printStats(p_one_name,"None")
                s.close()
                break
            if value==True:
                continue
        row,column=makeMove(player_two)
        sendMove(s,row,column)
        if playerTwoWin(player_two,player_two.isWinner()):
            player_two.printGameBoard()
            player_two.updateGamesPlayed()
            player_two.resetGameBoard()
            value=playAgain(s)
            if value==False:    
                player_two.printStats(p_one_name,"player2")
                s.close()
                break
            if value==True:
                continue
        if player_two.boardIsFull():
            player_two.printGameBoard()
            print("Tie!")
            player_two.updateGamesPlayed()
            player_two.resetGameBoard()
            player_two.incrementTies()
            value=playAgain(s)
            if value==False:    
                player_two.printStats(p_one_name,"None")
                s.close()
                break
            if value==True:
                continue
        
        
if __name__=="__main__":
    runProgram()
        