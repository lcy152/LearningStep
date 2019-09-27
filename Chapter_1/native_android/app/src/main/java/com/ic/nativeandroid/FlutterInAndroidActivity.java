package com.ic.nativeandroid;

import android.os.Bundle;
import android.support.annotation.Nullable;
import android.support.v7.app.AppCompatActivity;

import org.json.JSONException;
import org.json.JSONObject;
import io.flutter.view.FlutterView;

public class FlutterInAndroidActivity  extends AppCompatActivity {
    private FlutterView flutterView;

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceStae) {
        super.onCreate(savedInstanceStae);

        String route = getIntent().getStringExtra("_route_");
        String params = getIntent().getStringExtra("_params_");
        JSONObject jsonObject = new JSONObject();
        try {
            jsonObject.put("pageParams", params);
        } catch (JSONException e) {
            e.printStackTrace();
        }

        //将FlutterView设置进ContentView中,设置内容视图
        //创建FlutterView
        flutterView = com.ic.nativeandroid.config.Flutter.createView(this, getLifecycle(), route + "?" + jsonObject.toString());
        //设置显示视图
        setContentView(flutterView);
        System.out.print("current: " + "MyFlutterActivity");

    }
}
