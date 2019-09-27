# Learning and talking

* Android集成flutter.

## Chapter 1

* 新建一个Basic Activity类型的native app
* 新建一个flutter app
~~~~
    // apply plugin: 'com.android.application'
    apply plugin: 'com.android.library'
~~~~
    // applicationId "com.ic.flutter.flutter_app"

修改AndroidManifest.xml


~~~~
    <!--android:name="io.flutter.app.FlutterApplication"-->
    <!--android:label="flutter_app"-->

    <!--<category android:name="android.intent.category.LAUNCHER"/>-->
~~~~

将aar添加到lib文件夹中, 修改app/build.gradle
~~~~
    repositories {
        flatDir { dirs 'libs' }
    }
    compileOptions {
        sourceCompatibility 1.8
        targetCompatibility 1.8
    }
    splits {
        abi {
            enable true
            reset()
            include 'x86', 'armeabi-v7a', 'x86_64'
        }
    }
~~~~
~~~~
    dependencies {
        ...
        implementation(name: 'app-release', ext: 'aar')
    }
~~~~

创建一个Activity
~~~~
    <activity
        android:name=".FlutterInAndroidActivity"
        android:label="@string/app_name"
        android:theme="@style/AppTheme.NoActionBar">
    </activity>
~~~~

创建一个Activity
~~~~
//创建FlutterView
flutterView = Flutter.createView(this, getLifecycle(), route + "?" + jsonObject.toString();
//设置显示视图
setContentView(flutterView);
~~~~

将config下的Flutter文件和FlutterFragment拷贝到项目中, 修改包名
~~~~
//创建FlutterView
flutterView = Flutter.createView(this, getLifecycle(), route + "?" + jsonObject.toString();
//设置显示视图
setContentView(flutterView);
~~~~


详细文档请参考

* [godoc.org/golang.org/x/oauth2](http://godoc.org/golang.org/x/oauth2)
