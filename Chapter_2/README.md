# Learning and talking

* Android集成flutter.

## Chapter 2

* 新建一个flutter module

代号1001的来源在这里:
~~~~
    工作目录\flutter_module\.android\Flutter\src\main\java\io\flutter\facade
~~~~

点击运行发现可以正常运行. 然后:
~~~~
    cd .android/
    gradlew flutter:assembleDebug
~~~~

修改main.dart
~~~~
    import 'dart:ui';

    void main() => runApp(getRouter(window.defaultRouteName));

    Widget getRouter(String name) {
        switch (name) {
            case 'route1':
            return MyApp();
            default:
            return Center(
                child: Text('Unknown route: $name', textDirection: TextDirection.ltr),
            );
        }
    }
~~~~

* 新建一个Basic Activity类型的native app

将aar添加到lib文件夹中, 修改app/build.gradle
~~~~
    android {
        ...
        <!-- repositories {
            flatDir { dirs 'libs' }
        } -->
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
    }

    dependencies {
        ...

        //导入flutter
        implementation project(':flutter')
    }
~~~~


在 android项目 根目录下的 settings.gradle 中添加如下代码

~~~~
    include ':app'
    setBinding(new Binding([gradle: this]))
    evaluate(new File(
        settingsDir.parentFile,
        'flutter_module/.android/include_flutter.groovy'
    ))  
~~~~

在MainActivity中启动flutter视图
~~~~
    FloatingActionButton fab = (FloatingActionButton) findViewById(R.id.fab);
    fab.setOnClickListener(new View.OnClickListener() {
        @Override
        public void onClick(View view) {
            FlutterView flutterView = Flutter.createView(MainActivity.this, getLifecycle(), "route1");
            ViewGroup.LayoutParams layoutParams = new ViewGroup.LayoutParams(ViewGroup.LayoutParams.MATCH_PARENT, ViewGroup.LayoutParams.MATCH_PARENT);
            addContentView(flutterView, layoutParams);
        }
    });
~~~~

运行成功

打包: 运行成功
