import java.util.HashMap;

public class repeated_in_string {
    public static void main(String[] args) {
        String name = "mehardeep singh arneja";

        HashMap<Character,Integer> count = new HashMap<>();

        for (char i : name.toCharArray()) {
            if (Character.isWhitespace(i)) {
                continue;
            }
            if (count.get(i) == null) {
                count.put(i,1);
            }
            else{
                count.put(i,count.get(i)+1);
            }
        }

        for (char i:count.keySet()) {
            System.out.println(i+" repeated "+count.get(i)+" times.");
        }

    }
}

