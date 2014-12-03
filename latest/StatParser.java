import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileWriter;
import java.io.PrintWriter;
import java.math.BigInteger;
import java.util.HashMap;
import java.util.HashSet;
import java.util.Scanner;


public class StatParser {

	public static void main(String[] args) {
		Scanner sc = new Scanner(System.in);
		System.out.print("Enter number of servers: ");
		int numServers = sc.nextInt();
		System.out.print("Enter number of malicious hosts: ");
		int numMalicious = sc.nextInt();
		System.out.print("Enter number of normal clients: ");
		int numClients = sc.nextInt();
		int total = numServers + numMalicious + numClients;
		
		
		HashSet<String> malicious = new HashSet<String>();
		int firstMalicious = numServers + numClients + 1;
		
		for (int i = firstMalicious; i <= total; i++){
			String host = "10." + (i/65536)%256 + "." + (i/256)%256 + "." + i%256;
			malicious.add(host);
		}
		
		//for (String s: (String[]) malicious.toArray(new String[malicious.size()])){
		//	System.out.println(s);
		//}
		
		try {
			sc = new Scanner(new File("data.txt"));
		
			HashMap<String, Server> statMap = new HashMap<String, Server>();
			while (sc.hasNext()){
				String json = sc.nextLine();
				String src, dst;
				int count;
				for (int i = 1; i < json.length(); i++){
					if (json.charAt(i) == '{'){
	
						int start = i + 11;
						i += 11;
						while (json.charAt(i) != '"'){
							i++;
						}
						src = json.substring(start, i);
						start = i + 12;
						i += 12;
						while (json.charAt(i) != '"'){
							i++;
						}
						dst = json.substring(start, i);
						i += 11;
						start = i;
						while (json.charAt(i) != '"'){
							i++;
						}
						count = Integer.parseInt(json.substring(start, i));
						src = longToDot(src);
						dst = longToDot(dst);
						if (!(statMap.containsKey(dst))){
							statMap.put(dst, new Server(dst));
						}
						if (malicious.contains(src)){
							Server svr = statMap.get(dst);
							svr.maliciousConnections += count;
							svr.totalConnections += count;
						} else {
							Server svr = statMap.get(dst);
							svr.totalConnections += count;
						}
						//System.out.print("Src: " + longToDot(src) + " Dst: " + longToDot(dst) + " Count: " + count + "\n");
					}
				}
			}
			sc.close();
			
		
			try{
				PrintWriter out = new PrintWriter(new FileWriter("stats.csv", true));
				out.println("Server IP, Malicious Requests, Normal Requests, Total Requests, Normal Ratio, Malicious Ratio");
				for (String s : statMap.keySet()){
					Server svr = statMap.get(s);
					out.println(s + ", " + svr.maliciousConnections + ", " + (svr.totalConnections - svr.maliciousConnections) + ", " + svr.totalConnections + ", " + (double)(svr.totalConnections - svr.maliciousConnections)/svr.totalConnections + ", " + (double)svr.maliciousConnections/svr.totalConnections);
				}
				out.close();
			} catch (Exception e){
				System.out.println(e);
			}
		} catch (FileNotFoundException e1) {
			// TODO Auto-generated catch block
			e1.printStackTrace();
		}
	}
	
	public static String longToDot(String address){
		StringBuffer sb = new StringBuffer();
		BigInteger ip = new BigInteger(address);
		sb.append(ip.mod(BigInteger.valueOf((256))));
		sb.insert(0, ".");
		ip = ip.divide(BigInteger.valueOf(256));
		sb.insert(0, ip.mod(BigInteger.valueOf((256))));
		sb.insert(0, ".");
		ip = ip.divide(BigInteger.valueOf(256));
		sb.insert(0, ip.mod(BigInteger.valueOf((256))));
		sb.insert(0, ".");
		ip = ip.divide(BigInteger.valueOf(256));
		sb.insert(0, ip.mod(BigInteger.valueOf((256))));
		
		
		return sb.toString();
	}

}

class Server{
	public long totalConnections;
	public long maliciousConnections;
	String address;
	
	public Server(String _address){
		totalConnections = 0;
		maliciousConnections = 0;
		address = _address;
	}
}
