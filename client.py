import socket, sys, pygame, os

def get_path():
    path = os.path.realpath(__file__)
    ex = True
    while ex == True:
        if path[len(path)-1:len(path)] != '\\':
            path = path[0:len(path)-1]
        else:
            ex = False
    return path


def display(data):
    f = open("cache", 'w')
    f.write(data)#.decode('utf-8'))
    f.close()
    f = open("cache", 'r')
    recreation = [['',[],[],None] for i in range (0, int(f.readline().rstrip()))]
    depth = [0 for i in range (0, len(recreation))]
    for i in range (0, len(recreation)):
        recreation[i][0] = f.readline().rstrip()
        temp = f.readline().rstrip()
        while temp != "":
            recreation[i][1].append(temp)
            temp = f.readline().rstrip()
        temp = f.readline().rstrip()
        while temp != "":
            recreation[i][2].append(int(temp))
            temp = f.readline().rstrip()
        if f.readline().rstrip() == "True":
            recreation[i][3] = True
        else:
            recreation[i][3] = False

    current = 0
    ins = 0
    depth = explore(recreation, depth, current, ins)
    biggest = 0
    for i in range (0, len(depth)):
        if depth[i] > biggest:
            biggest = depth[i]
    width = [0 for i in range (0, biggest)]
    for i in range (0, len(depth)):
        width[depth[i]-1] += 1
    tt = [0 for i in range (0, len(recreation))]
    total = [0 for i in range (0, biggest)]
    for i in range (0, len(recreation)):
        total[depth[i]-1] += 1
        tt[i] = total[depth[i]-1]
    pygame.display.init()
    win = pygame.display.set_mode((400,400))
    exis = True
    pygame.font.init()
    font = pygame.font.Font(get_path()+'Roboto.ttf', 12)
    while exis:

        win.fill((255,255,255))

        total = [0 for i in range (0, biggest)]

        for i in range (0, len(recreation)):
            for j in range (0, len(recreation[i][2])):
                dest = recreation[i][2][j]
                pygame.draw.line(win, (0,0,0), (int(400*(tt[i]/(width[depth[i]-1]+1))), int(400*(depth[i]/(biggest+1))-10)), (int(400*(tt[dest]/(width[depth[dest]-1]+1))), int(400*(depth[dest]/(biggest+1))-30)), 2)
            if recreation[i][3] == True:
                pygame.draw.circle(win, (100,200,100), (int(400*(tt[i]/(width[depth[i]-1]+1))), int(400*(depth[i]/(biggest+1))-20)), 10)
            else:
                pygame.draw.circle(win, (100,100,200), (int(400*(tt[i]/(width[depth[i]-1]+1))), int(400*(depth[i]/(biggest+1))-20)), 10)
            text_width, text_height = font.size(recreation[i][0][-1:])
            win.blit(font.render(recreation[i][0][-1:], True, (0,0,0)), (int(400*(tt[i]/(width[depth[i]-1]+1))-0.5*text_width), int(400*(depth[i]/(biggest+1))-20)-0.5*text_height))
            
        pygame.display.flip()
        
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exis = False
                    pygame.display.quit()


def explore(trie, depth, current, ins):
    ins += 1
    depth[current] = ins
    for i in range (0, len(trie[current][2])):
        depth = explore(trie, depth, trie[current][2][i], ins)
    return depth


futile = True
existance = True
first = True

send = "hello_server"

print("attempting to reach server")

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('3.8.152.9',8080))
from_server = client.recv(4096)
print("pysically connected")

while existance is futile:
    if sendall == "endpoint!":
        sendall += "hahafool"
    client.sendall((send).encode('utf-8'))
    client.sendall(("endpoint!").encode('utf-8'))
    
    if first == True:
        print("sent handshake")

    from_server = ""
    while True:
        data = client.recv(4096)
        if len(data.decode("utf-8")) == 0:
            from_server = "quit"
            break
        if data.decode('utf-8') == "endpoint!":
            break
        from_server += data.decode('utf-8')
    
    if first == True:
        print("recieved handshake")

    if send == "quit":
        client.close()
        sys.exit()

    if send == "display":
        display(from_server)

    if first == True:
        print("successfully reached server")
        print("input a command (or help for commands)")
        first = False
    elif send == "display":
        pass
    else:
        print(from_server)
    send = input()

    while send == "help":
        print("commands:")
        print("search  -  the word following it will be searched for in the trie")
        print("add  -  the word following it will be added to the trie")
        print("predict - the word following it will be used to search the list for any words it can be the first part of (like auto predict)")
        print("delete  -  the word following it will be deleted for in the trie (but all data will remain)")
        print("purge  -  the word following it will be searched for in the trie (and all data will be removed if able to do so)")
        print("display  -  copies current trie data to your device and displays it")
        print("quit - stops the connection and terminates program (please use rather than ctrl C,")
        print("it still works but ctrl C takes time for the server to realise the connection has been lost)\n")
        
        print("input a command (or help for commands)")
        send = input()















    
