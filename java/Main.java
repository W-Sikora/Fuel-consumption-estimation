package com.company;

import java.time.LocalDateTime;
import java.util.Random;

public class Main {

    public static void main(String[] args) {
        Random random = new Random();
        random.nextDouble();

        Calculation calculation = new Calculation();

        int i = 0, iterations = 7;
        while (i < iterations ) {
            try {
                Thread.sleep(5000);
            } catch (InterruptedException ex) {
                Thread.currentThread().interrupt();
            }
            calculation.setTimes(LocalDateTime.now());
            calculation.setLatitudes(39.92262 + random.nextDouble() / 2000);
            calculation.setLongitudes(116.43453 + random.nextDouble() / 2000);
            System.out.println(calculation.toString());
            i++;
        }
        JsonObject jsonObj = new JsonObject();
        JsonArray jsonArray = new Gson().toJsonTree(calculation.getSpeedList()).getAsJsonArray();
        jsonObj.add("speeds", jsonArray);
        System.out.println(jsonObj);
    }
}
