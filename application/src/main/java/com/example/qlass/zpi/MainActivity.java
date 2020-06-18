package com.example.qlass.zpi;

import android.Manifest;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.location.Criteria;
import android.location.Location;
import android.location.LocationListener;
import android.location.LocationManager;
import android.provider.Settings;
import android.support.annotation.NonNull;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.support.v7.app.AppCompatActivity;
import android.os.Bundle;
import android.util.Log;
import android.view.View;
import android.widget.Button;
import android.widget.TextView;
import com.example.qlass.zpi.Calculation;
import android.os.*;
import android.widget.Toast;

import org.json.JSONArray;
import org.json.JSONObject;
import org.jsoup.Jsoup;
import org.jsoup.nodes.Document;
import org.jsoup.select.Elements;
import org.w3c.dom.Element;
import org.w3c.dom.Text;

import java.io.DataOutputStream;
import java.io.IOException;
import java.net.HttpURLConnection;
import java.net.URL;
import java.time.LocalDateTime;
import java.util.ArrayList;
import java.util.List;


public class MainActivity extends AppCompatActivity {
    private static final int MY_PERMISSION_ACCESS_COARSE_LOCATION = 11;
    private static final int MY_PERMISSION_ACCESS_FINE_LOCATION = 11;
    private TextView textView;
    private TextView textView2;
    private LocationManager locationManager;
    private LocationListener locationListener;
    Integer i = 0;
    Calculation calculation = new Calculation();
    private Handler handler = new Handler();
    private Runnable runnable = new Runnable() {
        @Override
        public void run() {
            getData();
            handler.postDelayed(this, 1000);
        }
    };

    public interface GetLocation {
        public void onLocationChanged(Location location);

        public void onStatusChanged(String s, int i, Bundle bundle);

        public void onProviderEnabled(String s);

        public void onProviderDisabled(String s);
    }

    String speed = "";

    private void getData() {

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    Document doc = Jsoup.connect("http://192.168.43.200:5000/api").ignoreContentType(true).get();
                    Elements element = doc.select("body");
                    speed = element.text();
                } catch (IOException e) {

                }

                runOnUiThread(new Runnable() {
                    @Override
                    public void run() {
                        textView.setText(speed);
                    }
                });
            }
        }).start();

    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);
        Calculation calc = new Calculation();
        textView = (TextView) findViewById(R.id.textView);
        textView2 = (TextView) findViewById(R.id.textView2);
        locationManager = (LocationManager) getSystemService(Context.LOCATION_SERVICE);
        locationListener = new LocationListener() {
            @Override
            public void onLocationChanged(Location location) {

                calculation.setTimes(LocalDateTime.now());
                calculation.setLatitudes(location.getLatitude());
                calculation.setLongitudes(location.getLongitude());
                String x = calculation.toString();
                List<Double> test = calculation.getSpeedList();
                if (i > 0) {
                    sendPost();
                } else {
                    i++;
                }
            }

            @Override
            public void onStatusChanged(String provider, int status, Bundle extras) {

            }

            @Override
            public void onProviderEnabled(String provider) {

            }

            @Override
            public void onProviderDisabled(String provider) {

            }
        };

        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_COARSE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_COARSE_LOCATION}, MY_PERMISSION_ACCESS_COARSE_LOCATION);
        }
        if (ContextCompat.checkSelfPermission(this, android.Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            ActivityCompat.requestPermissions(this, new String[]{android.Manifest.permission.ACCESS_FINE_LOCATION}, MY_PERMISSION_ACCESS_FINE_LOCATION);
        }

        locationManager.requestLocationUpdates(LocationManager.GPS_PROVIDER, 1000, 0, locationListener);
        handler.postDelayed(runnable, 1000);
    }

    public void sendPost() {
        Thread thread = new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    URL url = new URL("http://192.168.43.200:5000/foo");
                    HttpURLConnection conn = (HttpURLConnection) url.openConnection();
                    conn.setRequestMethod("POST");
                    conn.setRequestProperty("Content-Type", "application/json;charset=UTF-8");
                    conn.setRequestProperty("Accept", "application/json");
                    conn.setDoOutput(true);
                    conn.setDoInput(true);
                    List<Double> speedList;
                    speedList = new ArrayList<>();
                    speedList = calculation.getSpeedList();
                    JSONObject jsonParam = new JSONObject();
                    JSONArray array = new JSONArray();
                    for (Double speed : speedList) {
                        array.put(speed);
                    }
                    jsonParam.put("speed", array);

                    DataOutputStream os = new DataOutputStream(conn.getOutputStream());
                    os.writeBytes(jsonParam.toString());

                    os.flush();
                    os.close();

                    conn.disconnect();
                } catch (Exception e) {
                    e.printStackTrace();
                }
            }
        });

        thread.start();
    }

}
