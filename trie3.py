import threading, copy, time, re

condition = threading.Condition()
trie = [["",[],[],False]]
blank_links = []

class organiser(threading.Thread):

    def __init__(self):
        threading.Thread.__init__(self)


    def run(self):
        global clients
        global trie
        global blank_links
        while True:
            time.sleep(150)
            print("I AM GETTING KEY")
            aq_key = False
            while aq_key == False:
                print("trying")
                aq_key = condition.acquire(timeout = 1)
                if aq_key == False:
                    print("organiser waiting on key")
                    aq_key = False
            print("organiser got key")
            clients = [c for c in clients if c.is_alive()]
            print(clients)
            if len(clients) == 0 and len(blank_links) > 0:
                print("organiser cleaning")
                self.clean()
            elif len(blank_links) > 50:
                print("organiser cleaning due to many spaces")
                self.clean()
            print("organiser done")
            condition.notify_all()
            condition.release()

    def clean(self):
        global trie
        global blank_links
        condition.acquire()
        dit = {}
        new_trie = []
        for i in range (0, len(trie)):
            if i in blank_links:
                pass
            else:
                dit[str(i)] = len(new_trie)
                new_trie.append(trie[i])
        for i in range (0, len(new_trie)):
            for j in range (0, len(new_trie[i][2])):
                new_trie[i][2][j] = dit[str(new_trie[i][2][j])]
        trie = new_trie
        blank_links = []
        condition.notify_all()
        condition.release()

class client(threading.Thread):

    def __init__(self, conn, addr, no):
        threading.Thread.__init__(self)
        self.conn = conn
        self.addr = addr
        self.no = no


    def run(self):
        global trie
        global blank_links
        self.conn.send(bytes("welcome", "utf-8"))
        verify = False

        while True:
            all_false = True
            if all_false == True:
                from_client = ''
                while True:
                    data = self.conn.recv(4096)
                    print("data", data)
                    if len(data.decode("utf-8")) == 0:
                        from_client = "quit"
                        break
                    if data.decode('utf-8') == "endpoint!":
                        break
                    from_client += data.decode('utf-8')
                
                if verify == False:
                    if from_client != "hello_server":
                        print("unverified access ettempted")
                        self.conn.close()
                        break
                    else:
                        verify = True

                aq_key = False
                while aq_key == False:
                    print("trying")
                    aq_key = condition.acquire(timeout = 1)
                    if aq_key == False:
                        print(self.no, "waiting on key")
                        aq_key = False
                print("key aqired",self.no)

                if from_client[0:7] == "search ":
                    info_to_send = self.check(from_client[7:])
                elif from_client[0:4] == "add ":
                    info_to_send = self.add(from_client[4:])
                elif from_client[0:7] == "delete ":
                    info_to_send = self.delete(from_client[7:])
                elif from_client[0:6] == "purge ":
                    info_to_send = self.purge(from_client[6:])
                elif from_client[0:8] == "predict ":
                    info_to_send = self.predict(from_client[8:])
                elif from_client == "display":
                    info_to_send = self.send()
                elif from_client == "quit":
                    condition.release()
                    self.conn.send(bytes("bye", 'utf-8'))
                    self.conn.close()
                    print(f"client {self.addr} disconnected",self.no)
                    break
                else:
                    info_to_send = "not a recognised command"

                self.conn.send(bytes(info_to_send, 'utf-8'))
                self.conn.send(bytes("endpoint!", 'utf-8'))
                condition.notify_all()
                condition.release()
            print("out", self.no)

    def send(self):
        global trie
        global blank_links
        condition.acquire()
        f = ""#open("tosend.txt", 'wb')
        f += str(len(trie)-len(blank_links))+"\n"
        for i in range (0, len(trie)):
            if i in blank_links:
                pass
            else:
                f += trie[i][0]+"\n"
                for j in range (0, len(trie[i][1])):
                    f += trie[i][1][j]+"\n"
                f += "\n"
                for j in range (0, len(trie[i][2])):
                    f += str(trie[i][2][j])+"\n"
                f += "\n"
                f += str(trie[i][3])+"\n"
        condition.notify_all()
        condition.release()
        return f

    def clean(self, string):#cleans input (hence including whats added etc in output)
        stri = re.sub('[^A-Za-z]+', '', string)
        strii = stri.lower()
        return strii

    def check(self, string):
        global trie
        condition.acquire()
        ptrie = copy.copy(trie)
        nstring = self.clean(string)
        current_state = 0
        output = ""

        for i in range (0, len(nstring)):
            inthere = False
            link = -1
            for j in range (0, len(ptrie[current_state][1])):
                if nstring[i:i+1] == ptrie[current_state][1][j]:
                    inthere = True
                    link = j
                    j = len(ptrie[current_state][1])
            if inthere == True:
                current_state = ptrie[current_state][2][link]
            else:
                output = nstring + " is not in trie"#ik the breif said return True/False
                i = len(nstring)                    #but it needs to be converted to string
        if output != nstring + " is not in trie":   #anyway so I may as well do strings that
            if ptrie[current_state][3] == True:     #are more user readable and could be 
                output = nstring + " is in trie"    #converted in applications
            else:
                output = nstring + " is not in trie"
        condition.release()
        return output

    def add(self, string):
        global trie
        global blank_links
        condition.acquire()
        ptrie = copy.copy(trie)
        pblank_links = copy.copy(blank_links)
        nstring = self.clean(string)
        current_state = 0
        output = ""

        for i in range (0, len(nstring)):
            inthere = False
            link = -1
            for j in range (0, len(ptrie[current_state][1])):
                if nstring[i:i+1] == ptrie[current_state][1][j]:
                    inthere = True
                    link = j
                    j = len(ptrie[current_state][1])
            if inthere == True:
                current_state = ptrie[current_state][2][link]
            else:
                if len(pblank_links) > 0:
                    ptrie[current_state][1].append(nstring[i:i+1])
                    ptrie[current_state][2].append(pblank_links[len(pblank_links)-1])
                    ptrie[pblank_links[len(pblank_links)-1]] = ([nstring[0:i+1],[],[],False])
                    current_state = pblank_links[len(pblank_links)-1]
                    pblank_links = pblank_links[0:len(pblank_links)-1]
                else:
                    ptrie[current_state][1].append(nstring[i:i+1])
                    ptrie[current_state][2].append(len(ptrie))
                    ptrie.append([nstring[0:i+1],[],[],False])
                    current_state = len(ptrie)-1
        if ptrie[current_state][3] == False:
            ptrie[current_state][3] = True
            output = "added " + nstring
        else:
            output = nstring + " is in trie already"
        trie = ptrie
        blank_links = pblank_links
        condition.notify_all()
        condition.release()
        return output

    def delete(self, string):#this does not remove parts of the Trie, only wether its a word or not
        global trie
        condition.acquire()
        ptrie = copy.copy(trie)
        nstring = self.clean(string)
        current_state = 0
        output = ""

        for i in range (0, len(nstring)):
            inthere = False
            link = -1
            for j in range (0, len(ptrie[current_state][1])):
                if nstring[i:i+1] == ptrie[current_state][1][j]:
                    inthere = True
                    link = j
                    j = len(ptrie[current_state][1])
            if inthere == True:
                current_state = ptrie[current_state][2][link]
            else:
                output = nstring + " is not in trie"
                i = len(nstring)
        if output != nstring + " is not in trie":
            if ptrie[current_state][3] == True:
                ptrie[current_state][3] = False
                output = nstring + " is no longer a word in trie"
            else:
                output = nstring + " was not in trie"
        trie = ptrie
        condition.notify_all()
        condition.release()
        return output

    def purge(self, string):#this removes parts on the trie with the word
        global trie
        global blank_links
        condition.acquire()
        ptrie = copy.copy(trie)
        pblank_links = copy.copy(blank_links)
        
        nstring = self.clean(string)
        current_state = 0
        output = ""
        to_remove = []
        last_link = -1
        last_state = -1

        for i in range (0, len(nstring)):
            inthere = False
            link = -1
            if i > 0 and len(ptrie[current_state][1]) <= 1 and ptrie[current_state][3] == False:
                to_remove.append(current_state)
                if len(to_remove) == 1:
                    last_link = last_state
            elif i > 0:
                to_remove = []
            for j in range (0, len(ptrie[current_state][1])):
                if nstring[i:i+1] == ptrie[current_state][1][j]:
                    inthere = True
                    link = j
                    j = len(ptrie[current_state][1])
            if inthere == True:
                last_state = current_state
                current_state = ptrie[current_state][2][link]
            else:
                output = nstring + " is not in trie"
                i = len(nstring)



        if len(ptrie[current_state][1]) == 0:
            to_remove.append(current_state)
        
            if output != nstring + " is not in trie":
                for i in range (0, len(to_remove)):
                    ptrie[to_remove[i]] = ["",[],[],None]
                for i in range (0, len(to_remove)):
                    pblank_links.append(to_remove[i])
                output = nstring + " is no longer a word in trie"
            replacement = []
            replacement_l = []
            for i in range (0, len(ptrie[last_link][2])):
                if ptrie[last_link][2][i] != to_remove[0]:
                    replacement.append(ptrie[last_link][2][i])
                    replacement_l.append(ptrie[last_link][1][i])
            ptrie[last_link][2] = replacement
            ptrie[last_link][1] = replacement_l
        else:
            ptrie[current_state][3] = False
            output = "could not remove " + nstring + ", no longer a word"
        if len(ptrie) == 0:           #I think my logic means this wont come into play...
            ptrie = [["",[],[],False]]#but just in case
        trie = ptrie
        blank_links = pblank_links
        condition.notify_all()
        condition.release()
        return output


    def predict(self, string):#fetch a list of possible words given a prompt
        global trie
        condition.acquire()
        ptrie = copy.copy(trie)
        nstring = self.clean(string)
        current_state = 0

        for i in range (0, len(nstring)):
            inthere = False
            link = -1
            for j in range (0, len(ptrie[current_state][1])):
                if nstring[i:i+1] == ptrie[current_state][1][j]:
                    inthere = True
                    link = j
                    j = len(ptrie[current_state][1])
            if inthere == True:
                current_state = ptrie[current_state][2][link]
            else:
                i = len(nstring)
        out = []
        out = self.search_from_pos(current_state, out, ptrie)#I did think of another way to do this
        condition.notify_all()                               #but it took sooooo much memory
        condition.release()
        
        if len(out) == 0:
            output = "no possible known words matching " + nstring
        else:
            output = "complete words for " + nstring + " could be: "
            for i in range (0, len(out)):
                output += out[i]
                output += ", "
        return output[:-2]


    def search_from_pos(self, position, out, ptrie):
        if ptrie[position][3] == True:
            out.append(ptrie[position][0])
        for i in range (0, len(ptrie[position][2])):
            out = self.search_from_pos(ptrie[position][2][i], out, ptrie)
        return out



import socket

serv = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serv.bind(('',8080))
serv.listen(5)

clients = []

organiser = organiser()
organiser.start()

while True:
    conn, addr = serv.accept()
    
    print(f"Connection from {addr} has been established!")

    clients.append(client(conn, addr,len(clients)))
    clients[len(clients)-1].start()
    print(clients)

    


































