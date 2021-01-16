# works android 10, fails android 8
# https://github.com/purushottamyadavbattula/Data_exchange_flutter/blob/master/app/src/main/java/com/andymobitec/data_exchange/MainActivity.java
import random
from jnius import autoclass, java_method, PythonJavaClass, cast


FlutterActivity = autoclass("io.flutter.embedding.android.FlutterActivity")
PythonActivity = autoclass("org.kivy.android.PythonActivity")
MethodChannel = autoclass('io.flutter.plugin.common.MethodChannel')
FlutterEngineCache = autoclass("io.flutter.embedding.engine.FlutterEngineCache")
FlutterEngine = autoclass("io.flutter.embedding.engine.FlutterEngine")
DartEntrypoint = autoclass("io.flutter.embedding.engine.dart.DartExecutor$DartEntrypoint")

currentActivity = PythonActivity.mActivity
context = currentActivity.getApplicationContext()

def open_flutter_activity():
    # Set up the platform channel or Flutter will throw UnimplementedError
    mc =  MethodChannel(FlutterEngineCache.get("my_engine_id").getDartExecutor().getBinaryMessenger(), "FlutterKivy/test")
    mc.setMethodCallHandler(MyMethodCallHandler())

    # Start activity with cached Flutter engine
    currentActivity.startActivity(
        FlutterActivity.withCachedEngine("my_engine_id").build(context)
    )


# Data exchange between two platforms is done here
# AttributeError: 'tuple' object has no attribute 'invoke'
# https://github.com/kivy/pyjnius/blob/master/jnius/jnius_proxy.pxi#L124
class MyMethodCallHandler(PythonJavaClass):
    __javainterfaces__ = ['io/flutter/plugin/common/MethodChannel$MethodCallHandler']
    __javacontext__ = "app"

    @java_method("(Lio/flutter/plugin/common/MethodCall;Lio/flutter/plugin/common/MethodChannel$Result;)V")
    # @java_method("(Ljava/lang/Object;Ljava/lang/Object;)V")
    def onMethodCall(self, methodCall, result):
        print("on method call in kivy")
        if methodCall.method == "fromFlutter":
            # Access data from Flutter and send it back
            result.success(f"{int(random.random()*100)}Sent from Kivy "+ methodCall.argument("data"))

        elif methodCall.method == "updateKivyVar":
            from kivy.app import App
            APP_INSTANCE = App.get_running_app()
            APP_INSTANCE.my_temp = {"data":str(methodCall.argument("data"))}
            result.success("updated var successfully")
        else:
            result.success("Sent from Kivy Else")

# Configure and cache engine
# Usage: run_on_ui_thread(warm_up_flutter_engine)
def warm_up_flutter_engine():
    flutterEngine = FlutterEngine(context)
    flutterEngine.getDartExecutor().executeDartEntrypoint(DartEntrypoint.createDefault())
    FlutterEngineCache.getInstance().put("my_engine_id", flutterEngine)


# https://flutter.dev/docs/development/platform-integration/platform-channels?tab=android-channel-java-tab#jumping-to-the-ui-thread-in-android
# https://github.com/flutter/flutter/issues/34993
def run_on_ui_thread(func):
    class MyRunnable(PythonJavaClass):
        __javainterfaces__ = ['java/lang/Runnable']
        @java_method("()V")
        def run(self):
            func()
    Handler = autoclass('android.os.Handler')
    Looper = autoclass('android.os.Looper')
    Handler(Looper.getMainLooper()).post(MyRunnable())
