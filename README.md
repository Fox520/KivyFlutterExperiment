# KivyFlutterExperiment

## Setting up

1. Run buildozer android debug
2. Replace .buildozer/android/platform/build-armeabi-v7a/dists/myapp__armeabi-v7a/templates/build.tmpl.gradle with the one in this repository
3. In build.tmpl.gradle, change the maven url `CHANGE_ME` to the absolute path of 'repo' in this repository
Something like `/home/User/KivyFlutterExperiment/flutter_side/repo`


4. Add below to `.buildozer/android/platform/build-armeabi-v7a/dists/myapp__armeabi-v7a/templates/AndroidManifest.tmpl.xml`

```
<activity
            android:name="io.flutter.embedding.android.FlutterActivity"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize"
            />
```
