[app]
title = Dashboard IoT
package.name = iot_dashboard
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,txt
version = 0.1
requirements = python3,kivy==2.1.0,requests
orientation = portrait
fullscreen = 0

[platform:android]
android.permissions = INTERNET
android.api = 33
android.minapi = 21
android.sdk = 20
android.ndk = 25.1.8937393