import java.io.*;
import java.net.*;
import java.util.ArrayList;
import java.util.Collections;

public class WikiAnswerModel {
	Question question;
	ArrayList<String> wikiPages;
	ArrayList<Double> probabilities;
	ArrayList<Integer> cooccurrence;
	String guess;
	
	// TODO: add support for ignoring case
	public WikiAnswerModel(Question q)  {
		question = q;
		wikiPages = getWikiPages();
		cooccurrence = getCooccurrences();
		guess = guess();
	}
	
	public ArrayList<Integer> getCooccurrences() {
		cooccurrence = new ArrayList<Integer>();
		String answer1Page = wikiPages.get(0);
		String answer2Page = wikiPages.get(1);
		String answer3Page = wikiPages.get(2);
		
		ArrayList<ArrayList<Integer>> answer1FeatureIndexList = getAllFeatureIndices(answer1Page, question.features);
		ArrayList<ArrayList<Integer>> answer2FeatureIndexList = getAllFeatureIndices(answer2Page, question.features);
		ArrayList<ArrayList<Integer>> answer3FeatureIndexList = getAllFeatureIndices(answer3Page, question.features);		
		
		int answer1TotalCooccur = totalCooccurrence(answer1FeatureIndexList);
		int answer2TotalCooccur = totalCooccurrence(answer2FeatureIndexList);
		int answer3TotalCooccur = totalCooccurrence(answer3FeatureIndexList);
		
		cooccurrence.add(answer1TotalCooccur);
		cooccurrence.add(answer2TotalCooccur);
		cooccurrence.add(answer3TotalCooccur);
		return cooccurrence;
	}
	
	public ArrayList<String> getWikiPages() {
		wikiPages = new ArrayList<String>();
		try {
			for (int i = 0 ; i < question.wikiAnswers.size(); i++) {
				StringBuilder result = new StringBuilder();
				URL url_raw = new URL("https://en.wikipedia.org/w/index.php?format=json&action=raw&title=" + question.wikiAnswers.get(i));
				HttpURLConnection conn = (HttpURLConnection) url_raw.openConnection();
				conn.setRequestMethod("GET");
				
				BufferedReader rd = new BufferedReader(new InputStreamReader(conn.getInputStream()));
				String line;
				while ((line = rd.readLine()) != null) {
					result.append(line);
				}
				rd.close();
				String page = result.toString();
				wikiPages.add(page);
			}
		} catch (Exception e) {
			System.err.println("Error: " + e.getMessage());
		}
		return wikiPages;
	}
	
	public String guess() {
		@SuppressWarnings("unchecked")
		ArrayList<Integer> sortedList = (ArrayList<Integer>) cooccurrence.clone();
		if (question.features.contains("NOT"))
			Collections.sort(sortedList);
		else
			Collections.sort(sortedList,Collections.reverseOrder());
		//System.out.println("SortedList = " + sortedList);
		//System.out.println("SortedList 0th element = " + sortedList.get(0));
		int index = cooccurrence.indexOf(sortedList.get(0));
		//System.out.println("Index = " + index);
		String answer = question.answers.get(index);
		return answer;
	}
	
	//Count all co-occurrences of 
	public int totalCooccurrence(ArrayList<ArrayList<Integer>> list) {
		int count = 0;
		for (int i = 0; i < list.size(); i++) {
			for (int j = i+1; j < list.size(); j++) {
				count += countCooccurrence(list.get(i), list.get(j));
			}
		}
		return count;
	}
	
	// Count co-occurrences of all two word pairs appearing within a window from list1 and list2
	public int countCooccurrence(ArrayList<Integer> list1, ArrayList<Integer> list2) {
		int count = 0;
		for (int i = 0; i < list1.size(); i++) {
			for (int j = 0; j < list2.size(); j++) {
				//100 characters ~= 10-15 words window size
				//slightly larger to account for wiki markups
				int window = 100;
				if (Math.abs(list1.get(i) - list2.get(j)) <= window)
					count++;	
			}
		}
		return count;
	}
	
	//Index list for all features
	public ArrayList<ArrayList<Integer>> getAllFeatureIndices(String page, ArrayList<String> features) {
		ArrayList<ArrayList<Integer>> list = new ArrayList<ArrayList<Integer>>();
		for (int i = 0; i < features.size(); i++) {
			list.add(getFeatureIndices(page, features.get(i)));
		}
		return list;
	}
	
	//Index list for one feature
	public ArrayList<Integer> getFeatureIndices(String page, String feature) {
		ArrayList<Integer> list = new ArrayList<Integer>();
		int lastIndex = 0;
		while(lastIndex != -1) {
			lastIndex = page.indexOf(feature,lastIndex);
			if (lastIndex != -1) {
				list.add(lastIndex);
				lastIndex += feature.length();
			}
		}
		return list;
	}
	
}

