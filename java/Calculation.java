package com.company;

import java.time.Duration;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;

public class Calculation {
    private List<LocalDateTime> times = new ArrayList<>();
    private List<Double> latitudes = new ArrayList<>();
    private List<Double> longitudes = new ArrayList<>();

    public Calculation() {
    }

    public Calculation(List<LocalDateTime> times, List<Double> latitudes, List<Double> longitude) {
        this.times = new ArrayList<>();
        this.latitudes = new ArrayList<>();
        this.longitudes = new ArrayList<>();
    }

    public List<LocalDateTime> getTimes() {
        return times;
    }

    public void setTimes(LocalDateTime time) {
        this.times.add(time);
    }

    public List<Double> getLatitudes() {
        return latitudes;
    }

    public void setLatitudes(Double latitude) {
        this.latitudes.add(latitude);
    }

    public List<Double> getLongitudes() {
        return longitudes;
    }

    public void setLongitudes(Double longitude) {
        this.longitudes.add(longitude);
    }

    public List<Double> getDistanceList() {
        List<Double> distanceList = new ArrayList<>();
        if (latitudes.size() == longitudes.size() && latitudes.size() > 1) {
            for (int i = 0; i < latitudes.size() - 1; i++) {
                distanceList.add(calculateDistance(
                        latitudes.get(i + 1),
                        latitudes.get(i),
                        longitudes.get(i + 1),
                        longitudes.get(i)));
            }
        }
        return distanceList;
    }

    private double calculateDistance(double latitudePrevious, double latitudeCurrent, double longitudePrevious, double longitudeCurrent) {
        double formula = 0.5 - Math.cos(Math.toRadians(latitudeCurrent - latitudePrevious)) / 2
                + Math.cos(Math.toRadians(latitudePrevious)) * Math.cos(Math.toRadians(latitudeCurrent))
                * (1 - Math.cos(Math.toRadians(longitudeCurrent - longitudePrevious))) / 2;
        return 2 * 6371 * Math.asin(Math.sqrt(formula));
    }

    private double calculateTime(LocalDateTime previous, LocalDateTime current) {
        return (double) Duration.between(previous, current).getSeconds() / 3600;
    }

    private List<Double> getTimeList() {
        List<Double> timeList = new ArrayList<>();
        if (times.size() > 1) {
            for (int i = 0; i < times.size() - 1; i++) {
                timeList.add(calculateTime(times.get(i), times.get(i + 1)));
            }
        }
        return timeList;
    }

    private double calculateSpeed(double distance, double time) {
        if (time > 0) {
            return distance / time;
        } else {
            return 0;
        }
    }

    public List<Double> getSpeedList() {
        List<Double> speedList, distanceList, timeList;
        speedList = new ArrayList<>();
        distanceList = getDistanceList();
        timeList = getTimeList();
        if (distanceList.size() == timeList.size() && distanceList.size() > 0) {
            for (int i = 0; i < distanceList.size(); i++) {
                speedList.add(calculateSpeed(distanceList.get(i), timeList.get(i)));
            }
        }
        return speedList;
    }

    @Override
    public String toString() {
        return "Calculation{" +
                "\ntimes=" + times.toString() +
                ",\nlatitudes=" + latitudes.toString() +
                ",\nlongitudes=" + longitudes.toString() +
                ",\ntime durations=" + getTimeList() +
                ",\ndistances=" + getDistanceList() +
                ",\nspeeds=" + getSpeedList() +
                "\n}";
    }
}
