# Learning and talking

* Android集成flutter.

## Chapter 1

* 新建一个flutter app

修改build.gradle
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

* 新建一个Basic Activity类型的native app

将aar添加到lib文件夹中, 修改app/build.gradle. 缺点: 不能再x86的模拟器运行(难受呀). 分析aar包发现lib下面flutter-x86只有8B, 根本没打包进去... (20190929 最新进展, 可以用debug包跑模拟器, 哈哈哈)
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

启动flutter视图
~~~~
//创建FlutterView
flutterView = Flutter.createView(this, getLifecycle(), route + "?" + jsonObject.toString();
//设置显示视图
setContentView(flutterView);
~~~~

将config下的Flutter文件和FlutterFragment拷贝到项目中, 修改包名(来源请收看Chapter_2, 代号1001)
~~~~
//创建FlutterView
flutterView = Flutter.createView(this, getLifecycle(), route + "?" + jsonObject.toString();
//设置显示视图
setContentView(flutterView);
~~~~

