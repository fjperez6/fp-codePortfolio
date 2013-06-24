import java.net.*;
import java.io.*;
// emulates nslookup with getbyname methods
public class nsLookupEmulator{
  public static void main (String[] args) {
    try {
      while (true) {
        System.out.println("Enter hostname or IP.\nexit to quit");
        BufferedReader userInput = new BufferedReader(new InputStreamReader
                                                       (System.in));
        String address = userInput.readLine();
        if (address.equals("exit")) {
          break;
        }
        System.out.println(translate(address) + "\n*****");
      }
    }
    catch (IOException ex) {
      System.err.println(ex);
    }
  }

  private static String translate(String address) {
    InetAddress addressToTranslate;
    try {
    addressToTranslate = InetAddress.getByName(address);
    }
    catch (UnknownHostException ex) {
      return "Cannot find host ";
    }
    if (ipAddrCheck(address)) {
      return addressToTranslate.getHostAddress();
    }
    else {
      return addressToTranslate.getHostName();
    }
  }

  private static boolean ipAddrCheck(String address) {
    char[] testNonDigit = address.toCharArray();
    for (int i = 0; i < testNonDigit.length; i++) {
      if (!Character.isDigit(testNonDigit[i])) {
        if (testNonDigit[i] != '.') return true;
      }
    }
    return false;
  }
}
