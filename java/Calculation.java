package pl.wsikora.;


import java.time.Duration;
import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;

public class Calculation {
    private LocalDateTime previous;
    private double latitude1;
    private double longitude1;
    private LocalDateTime current;
    private double latitude2;
    private double longitude2;

    public Calculation() {
    }

    public Calculation(LocalDateTime previous, double latitude1, double longitude1, LocalDateTime current, double latitude2, double longitude2) {
        this.previous = previous;
        this.latitude1 = latitude1;
        this.longitude1 = longitude1;
        this.current = current;
        this.latitude2 = latitude2;
        this.longitude2 = longitude2;
    }

    public LocalDateTime getPrevious() {
        return previous;
    }

    public void setPrevious(LocalDateTime previous) {
        this.previous = previous;
    }

    public double getLatitude1() {
        return latitude1;
    }

    public void setLatitude1(double latitude1) {
        this.latitude1 = latitude1;
    }

    public double getLongitude1() {
        return longitude1;
    }

    public void setLongitude1(double longitude1) {
        this.longitude1 = longitude1;
    }

    public LocalDateTime getCurrent() {
        return current;
    }

    public void setCurrent(LocalDateTime current) {
        this.current = current;
    }

    public double getLatitude2() {
        return latitude2;
    }

    public void setLatitude2(double latitude2) {
        this.latitude2 = latitude2;
    }

    public double getLongitude2() {
        return longitude2;
    }

    public void setLongitude2(double longitude2) {
        this.longitude2 = longitude2;
    }

    private double setDistance() {
        double formula = 0.5 - Math.cos(Math.toRadians(latitude2 - latitude1)) / 2
                + Math.cos(Math.toRadians(latitude1)) * Math.cos(Math.toRadians(latitude2))
                * (1 - Math.cos(Math.toRadians(longitude2 - longitude1))) / 2;
        return 2 * 6371 * Math.asin(Math.sqrt(formula));
    }

    private double setTime() {
        double interval = Duration.between(previous, current).getSeconds();
        return interval / 3600;
    }

    private double setSpeed() {
        double time = setTime();
        double distance = setDistance();
        if (time > 0) {
            return distance / time;
        } else {
            return 0;
        }
    }

    public static void main(String[] args) {
        DateTimeFormatter formatter = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss");

        Calculation calculation = new Calculation();
        calculation.setPrevious(LocalDateTime.parse("2008-02-02 15:38:32", formatter));
        calculation.setLatitude1(39.92262);
        calculation.setLongitude1(116.43453);
        calculation.setCurrent(LocalDateTime.parse("2008-02-02 23:44:32", formatter));
        calculation.setLatitude2(39.92572);
        calculation.setLongitude2(122.44723);

        System.out.println(calculation.setDistance());
        System.out.println(calculation.setTime());
        System.out.println(calculation.setSpeed());
    }
}
