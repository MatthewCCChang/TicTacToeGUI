import socket
import gameboard
import boardGUI

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

def sendMove(sock:socket,row:int,column:int)->None:
    '''Sends the row and column number through socket object'''
    sock.send((str(row)+str(column)).encode())
    
    
def receiveMove(socket: socket,player_two:gameboard.BoardClass())->int:
    '''Receives data via socket and updates the gameboard'''
    data=socket.recv(1024).decode() 
    player_two.updateGameBoard(int(data[0]),int(data[1]),"X")
    return int(data[0]),int(data[1])
    
    
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
        
def receiveAndSend(host:str,port:int)-> socket:
    """Waits for a connection to be established, sends own name while receiving client name and printing."""
    s=receiveInfo(host,port) 
    p_one_name=receiveName(s)
    print("Connected to "+p_one_name)
    return s
    
    
def runProgram()->None:
    '''Runs the program in main'''
    p_two_GUI=boardGUI.BoardGUI("player2")
   
        
if __name__=="__main__":
    runProgram()
        