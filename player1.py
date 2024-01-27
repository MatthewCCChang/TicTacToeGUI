import socket
import gameboard
import boardGUI

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

    
def makeConnectionAgain(GUI:boardGUI)->socket:
    '''Prompts the user to reconnect.'''
    #rework everything
    response=input("Try to make connection again? y/n ")
    if response=="y":
        sock=sendInfo(player_two_host_info(),player_two_port(),player_one_username())   
        return sock
    elif response=="n":
        quit()
    

def sendMove(sock:socket,row:int,column:int)->None:
    '''Sends a string over the socket.'''
    sock.send((str(row)+str(column)).encode())

def receiveMove(sock: socket,player_one:gameboard.BoardClass())->int:
    '''Updates the gameboard with the information received.'''
    data=sock.recv(1024).decode()
    player_one.updateGameBoard(int(data[0]),int(data[1]),"O")
    return int(data[0]),int(data[1])

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

def sendAndReceive(ip:str,port:int,p_one_username:str)->socket:
    """Connects to the server and prints out the name of the server connected to."""
    s=sendInfo(ip,port,p_one_username)
    p_two_name=receivedName(s)
    print("Connected to "+p_two_name)
    return s


def runProgram()->None:
    '''Runs the program in main.'''
    p_one_GUI=boardGUI.BoardGUI("player1") 
    
                

if __name__=="__main__":
    runProgram()


    