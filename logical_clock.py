import random
import socket
import time
from multiprocessing import Process
import sys

def main_clock(port,num,msg_clk,total_val):
    try:
        host='127.0.0.1'
        sock = socket.socket()
        sock.bind((host, port))
        sock.listen(5)

        while True:
            #Establishing Connection
            connection, address = sock.accept()
            print("\nMaster - Client connection is established: "+str(num-1))
            init_msg = msg_clk.split(',')
            m_id = int(init_msg[0])
            msg_val = float(init_msg[1])
            time_difference1=0

            # byte conversion
            msg_clk = bytes(msg_clk, 'utf-8')
            connection.send(msg_clk)
            data_conn = connection.recv(1024)
            print("\nClient "+str(num-1) + " is recieved" + "\nLocal Clock: "+str(data_conn))
            print("\n")
            clk_message = data_conn.split(b",")
            flag=0
            if (int(clk_message[0])==2):
                m_id = int(clk_message[0])
                msg_val2 = float(clk_message[1])

                #calculating time difference for first client
                time_difference1=msg_val-msg_val2
                print("Time difference for first client: "+str(time_difference1)+"\n\n")
                print("-------------------------------------------------------------------------------\n\n") 
                new_cl = msg_val2 - (msg_val + (float(total_val) / 3))
            elif (int(clk_message[0]) == 3):
                m_id = int(clk_message[0])
                msg_val3 = float(clk_message[1])

                #calculating time difference for second client
                time_difference2 = msg_val-msg_val3
                print("Time difference for second client: "+str(time_difference2)+"\n\n")
                print("-------------------------------------------------------------------------------\n\n")

                #calculating average time value
                average_part=total_val/3
                if(num==3):
                    average_int = int(average_part)
                    average_fract = average_part - average_int
                    if(float(average_fract)>0.59):
                        average_int+=1
                        average_fract=average_fract-0.59
                        average_part=float(average_int)+float(average_fract)
                    print("\nBerkely's value of Master Clock: "+str(float("{0:.2f}".format(average_part))))
                    num=1
                    clk_change_val=msg_val+(float(average_part))
                    adjust_int = int(clk_change_val)
                    adjust_fract = clk_change_val - adjust_int
                    if (float(adjust_fract) > 0.59):
                        adjust_int  += 1
                        average_fract = adjust_fract - 0.59
                        clk_change_val = float(adjust_int) + float(average_fract)
                    cl_clk=float("{0:.2f}".format(clk_change_val))
                    new_cl=msg_val3-clk_change_val
                    print("\nNew Master Logical Clock Value: " +str(float("{0:.2f}".format(clk_change_val))))
                    altered_clk=str(float("{0:.2f}".format(clk_change_val)))
                    client_clock(num,cl_clk)
                    clk_change_val =str(clk_change_val)
                    clk_change_val = bytes(clk_change_val,'utf-8')
                    connection.send(clk_change_val)
                    clk_change_val=connection.recv(1024)
                    client_clock(num+1, cl_clk)

                    # checking for synchronization
                    if(str(cl_clk)==str(altered_clk)):
                        print("\nAll three clocks are synchronised.")
                    else:
                        print("\nClocks not synchronised.")
            else:
                print("\nInvalid output.")
                connection.close()
            connection.close()

    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Connection.")
        sys.exit(0)

        
def client_clock(n,value):
    if (int(n)<3):
        print("New Client "+str(n)+" Clock Value: "+str(value))

def client(port,c,client_clk,total_val):
    try:
        host='127.0.0.1'
        sock = socket.socket()
        clock_synch=0

        # Establishing Connection
        
        print("\nConnecting Client "+str(c-1)+" to master")
        sock.connect((host, port))
        client_clk=str(client_clk)
        print("\nClient "+str(c-1)+" Logical clock:" +str(client_clk))
        msg_clk = str(c)+',' + str(client_clk)
        data_conn = sock.recv(1024)
        print("\nMessage sucessfully recieved by Client "+str(c-1)+" from Master "+ str(data_conn))
        msg_clk = bytes(msg_clk, 'utf-8')

        sock.send(msg_clk)
        
        # Synchronizing clocks with each other

        if(c==3): 
            clock_synch = sock.recv(1024)
            clock_alt=str(clock_synch)+str(client_clk) 
            clock_alt = bytes(clock_alt, 'utf-8')
            sock.send(clock_alt)
            client_clock(c,clock_alt)
        sock.close()

    except (KeyboardInterrupt, SystemExit):
        print("\nEnding Connection")
        sys.exit(0)

if __name__ == "__main__":
    
    client_port1=9090
    client_port2=9000
    count =2
    logical_clock = float(random.randint(2, 20))
    client_logical_clock = float("{0:.2f}".format(random.choice([3,6,9,12,15,18,21])))
    process_port=8080
    print("\n\nStarting Connection...\n\n")
    print("Master is connected to port:" + str(process_port))
    print("Master's logical clock: " + str(client_logical_clock))
    
    msg_clk = '1,' + str(client_logical_clock)
    num=1
    total = 0
    
    # Listing Client Ports
    print("\nClient ports: ")
    
    print("Client "+str(num)+": " +str(client_port1))
    num=num+1
    print("Client "+str(num)+": " +str(client_port2))
    num=num+1

   
    
    logical_clock = float("{0:.2f}".format(random.choice([3, 6, 9, 12, 15, 18, 21])))
    total = total+ (logical_clock-client_logical_clock)
    Process(target=main_clock, args=(client_port1,count,msg_clk,total)).start()
    Process(target=client, args=(client_port1,count,logical_clock,total)).start()
    time.sleep(3)
    count+=1

    logical_clock = float("{0:.2f}".format(random.choice([3, 6, 9, 12, 15, 18, 21])))
    total = total+ (logical_clock-client_logical_clock)
    Process(target=main_clock, args=(client_port2,count,msg_clk,total)).start()
    Process(target=client, args=(client_port2,count,logical_clock,total)).start()
    time.sleep(3)
    count+=1