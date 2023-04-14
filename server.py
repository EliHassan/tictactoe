import socket
import threading
import time
board = dict()
server_port=5131
class Dot:
    def __init__(self,value):
        self.value = value
    def __str__(self):
        return self.value
    def value_change(self,new):
        self.value = new
def to_srt(a):
    timoxa = '\n' + '-'*7 + '\n'
    for v,i in enumerate(a.values(),1):
        timoxa += '|' + str(i)
        if v % 3 == 0:
            timoxa += '|\n' + '-'*7 + '\n'
    return timoxa.encode()
def end_game():
    end = True
    places = [[1,2,3],[4,5,6],[7,8,9],[1,4,7],[2,5,8],[3,6,9],[1,5,9],[3,5,7]]
    for i in places:
        if board[str(i[0])].value == board[str(i[1])].value == board[str(i[2])].value:
            end = False
        # Change this line of code to check if there are any empty spaces in the board
        if any(board[str(j)].value not in ['X', 'O'] for j in range(1, 10)):
            end = False
    return end
players = ['P1','P2']
turn = 0
def give_choise(connections,num, event_for_wait, event_for_set,variable):
    conn = connections[num]['sock']
    while True:
        event_for_wait.wait()
        event_for_wait.clear()
        conn.send(to_srt(board))
        data = conn.recv(1024)
        # Change this line of code to use the value_change method of the Dot class
        board[data.decode()].value_change(variable)
        event_for_set.set()
        if end_game():
            conn.send('Game over'.encode())
            break
def main():
    e1 = threading.Event()
    e2 = threading.Event()
    events = [e1,e2]
    variables = ['X','O']
    connections = []
    sock = socket.socket()
    sock.bind(('localhost', server_port))
    print("Ready! run clientx")
    sock.listen(5)
    k = 0
    for i in range(1, 10):
        board[f'{i}'] = Dot(str(i))
    while k < 2:
        conn, addr = sock.accept()
        print("New connection on:", addr)
        connections.append({'sock' : conn, 'address' : addr, 'stats': 0, 'name': 'Unknown'})
        th = threading.Thread(name='th'+str(len(connections)), target=give_choise, args=(connections,len(connections)-1,events[k%2],events[(k+1)%2],variables[k%2]))
        th.start()
        k +=1
    else:
        e1.set()
if __name__ == '__main__':
    main()