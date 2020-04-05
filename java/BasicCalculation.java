package com.company;

import java.lang.Math;
import java.time.Duration;
import java.time.LocalDateTime;
import java.time.Month;

public class BasicCalculation {

    public static void main(String[] args) {
        double distance = calculateDistance(54.366667, 18.633333, 54.466667, 17.016667);
        double time = calculateTime(LocalDateTime.now(), LocalDateTime.of(2020, Month.APRIL, 5, 19, 8, 56));
        double speed = calculateSpeed(distance, time);
        System.out.printf("distance: %f%n time: %f%n speed: %f%n", distance, time, speed);
    }

    private static double calculateDistance(double latitude1, double longitude1, double latitude2, double longitude2) {
        double formula = 0.5 - Math.cos(Math.toRadians(latitude2 - latitude1)) / 2 + Math.cos(Math.toRadians(latitude1)) *
                Math.cos(Math.toRadians(latitude2)) * (1 - Math.cos(Math.toRadians(longitude2 - longitude1))) / 2;
        return 2 * 6371 * Math.asin(Math.sqrt(formula));
    }

    private static double calculateTime(LocalDateTime current, LocalDateTime previous) {
        return Duration.between(previous, current).getSeconds();
    }

    private static double calculateSpeed(double distance, double time) {
        if (time != 0) {
            return distance / (time / 3600) ;
        } else {
            return 0;
        }
    }


}
