import java.util.ArrayList;
import java.util.Arrays;
import java.util.HashMap;

class tracker {
    int[] Attendance;
    int[] Total;
    String[] Subjects;
    double required;

    tracker(int[] att, int[] total, String[] subjects, double Req) {
        this.Attendance = att;
        this.Total = total;
        this.Subjects = subjects;
        this.required = Req;
    }

    public void track() {
        for (int i = 0; i < this.Attendance.length; i++) {
            int d = 0;
            while (true) {
                double per = ((this.Attendance[i] + d) * 100.0) / (this.Total[i] + d);

                if (per >= this.required) {
                    break;
                }
                d++;
            }
            if (d == 0) {
                System.out.println(this.Subjects[i] + ": No worries 😊.");
            } else {
                System.out.println(this.Subjects[i] + ": You need to attend " + d + " more classes to reach " + this.required + "%.");
            }
        }
    }
}

public class attendance_tracker {
    public static void main(String[] args) {
        int[] attended = {4, 18, 3, 1, 4, 21};
        int[] total = {7, 25, 4, 1, 6, 28};
        String[] subjects = {"Math", "Mechanical", "Chemistry", "English", "CTPS", "Electrical"};
        double required = 80;
        tracker t = new tracker(attended, total, subjects, required);
        t.track();
    }
}
