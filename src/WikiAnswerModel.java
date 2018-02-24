import java.io.*;
import java.net.*;
import com.google.gson.*;
public class WikiAnswerModel {
	public static void main (String[] args) throws Exception{
		URL url = new URL("https://en.wikipedia.org/w/api.php?action=query&prop=revisions&rvprop=content&format=jsonfm&formatversion=2&titles=pizza");
		
		HttpURLConnection request = (HttpURLConnection) url.openConnection();
		request.connect();
		
		JsonElement jsonElement = new JsonParser().parse(new InputStreamReader((InputStream) request.getContent()));
		JsonElement pages = jsonElement.getAsJsonObject().get("query").getAsJsonObject().get("pages");
		
		JsonObject obj = new JsonParser().parse(new InputStreamReader((InputStream) request.getContent())).getAsJsonObject();
		
		System.out.println(obj.get("query"));
		System.out.println("hello");
	}
}
