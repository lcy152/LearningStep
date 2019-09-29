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
        compileOptions {
            sourceCompatibility 1.8
            targetCompatibility 1.8
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

* 异常(以下为在有百度语音SDK项目中集成遭遇, 因为百度语音SDK带so文件, 所以main/jniLibs下有so文件, 但是用下列解决办法也无法解决).

1 编译遭遇--20190928

~~~~
couldn't find "libflutter.so"
~~~~

解决办法, 解压flutter module的apk, 添加到项目的main/jniLibs中. 然后新问题:

~~~~
A/flutter: [FATAL:flutter/runtime/dart_vm.cc(389)] Error while initializing the Dart VM: Precompiled runtime requires a precompiled snapshot
A/libc: Fatal signal 6 (SIGABRT), code -6 (SI_TKILL) in tid 29318 (m.datu.rt.queue), pid 29318 (m.datu.rt.queue)
~~~~

解决办法: 无

~~~~
Process 'command 'D:\flutter_SDK\flutter\bin\flutter.bat'' finished with non-zero exit value -529697949
~~~~

解决办法: 无

2 奇怪, 昨天编译还不能过, 今天编译过了, 打包啥的都正常了...难道是将so包放到jniLibs下有缓存吗? 总之重启一下试试吧--20190929

集成到一个只有百度SDK的项目比较: 
~~~~
    Chapter_1优先考虑, 因为耦合度低, 缺点是不能再x86的模拟器运行flutter画面, 真机无碍.
    Chapter_2耦合度高 // Chapter_2能在项目main/jniLibs下有so文件时没能解决问题. // 已解决, 重启大法
~~~~


空项目比较: 
~~~~
    Chapter_1缺点是不能再x86的模拟器运行flutter画面, 真机无碍.
    Chapter_2没有任何问题.
~~~~


3 INSTALL_FAILED_NO_MATCHING_ABIS
~~~~
    splits {
        abi {
            enable true
            reset()
            include 'x86', 'armeabi-v7a','x86_64'
            universalApk true
        }
    }
~~~~

4 指定编译版本
~~~~
    release {
        ...
        ndk {
            // 设置支持的SO库架构
            abiFilters "armeabi-v7a", "x86"
        }
    }
~~~~

5 启动flutter的时候可以看到log如下, 所以以下四个文件是必须存在aar中.
I/ResourceExtractor: Extracted baseline resource assets/isolate_snapshot_data
I/ResourceExtractor: Extracted baseline resource assets/vm_snapshot_instr
I/ResourceExtractor: Extracted baseline resource assets/vm_snapshot_data
I/ResourceExtractor: Extracted baseline resource assets/isolate_snapshot_instr

