import java.io.*;
import java.util.*;
import java.net.*;
class Chatter {
  public static void main(String[] args) {
    Hashtable<String, PrintWriter> clientTable = new Hashtable<String, PrintWriter>();
    if (args.length != 1){                        //ensures port is specified at 
      System.out.println("Usage: Chatter port");  //command line
      System.exit(0);
    }  
    try{
      int port = Integer.parseInt(args[0]);
      ServerSocket servPort = new ServerSocket(port);
      System.out.println("The chat server is running on port " + port);
      while(true){                               //continuously checks for incoming 
        Socket clientSocket = servPort.accept(); //client connections 
        PrintWriter clientWriter = new PrintWriter(clientSocket.getOutputStream(), true);
        BufferedReader clientReader = new BufferedReader(new
                           InputStreamReader(clientSocket.getInputStream()));
        clientWriter.print("***Welcome to Chatter***\n" +
                 "Type bye to end\nWhat is your name?\n ");
        clientWriter.flush();
        String stringIn = clientReader.readLine();
        System.out.println("New client \'" + stringIn +
                          "\' on client port " + clientSocket.getPort()); 
        ClientChat clientSession = new ClientChat(clientSocket, clientWriter, 
                        clientReader, clientTable, stringIn);
        new Thread(clientSession).start();      // starts new process to handle client
      }
    }catch(Exception e){System.out.println("Cannot Start Server");} 
  }
} // end Chatter
class ClientChat implements Runnable{
  Hashtable<String, PrintWriter> clientTable =          //creates hash pair of 
                  new Hashtable<String, PrintWriter>(); //client and socket
  Socket ccsock;
  PrintWriter ccout;
  String ccsource;
  BufferedReader ccread;
  ClientChat(Socket s, PrintWriter pw, BufferedReader br,
             Hashtable<String, PrintWriter> h, String ccsource){
    ccsock = s;
    clientTable = h;
    ccout = pw;
    ccread = br;
    this.ccsource = ccsource;
    try{
      clientTable.put(ccsource, ccout);
    } catch(Exception e){}
  }
  public void run(){
    String broadcast;
    try{
      while(true){
        broadcast = ccread.readLine();  //Reads messages from clients
        PrintWriter send;
        if(broadcast.equals("bye")){    //Checks for keyword to disconnect
          for (Enumeration allClients = clientTable.keys();
             allClients.hasMoreElements();) {
            String speak = (String)allClients.nextElement();
            send = clientTable.get(speak);
            send.println("[Chatter]: " + ccsource + 
                         " has left the discussion");
            send.flush();               //sends broadcast indicating a 
          }                             //client disconnect
        }                               
        for (Enumeration allClients = clientTable.keys();
             allClients.hasMoreElements();) {
          String speak = (String)allClients.nextElement();
          send = clientTable.get(speak);
          send.println("["+ccsource+"]: "+broadcast);
          send.flush();                 //broadcasts message to all clients
        }
      }
    ccsock.close();                   //closes socket following disconnect
    }catch(Exception e){}
  }
}// end ClientChat
