[app]
title = Family Finance
package.name = familyfinance
package.domain = org.eduforge
source.dir = .
source.include_exts = py,png,jpg,jpeg,kv,ttf,txt,json,atlas

version = 0.5

requirements = python3,kivy==2.3.0,kivymd==1.2.0,requests,certifi

orientation = portrait
fullscreen = 0

android.api = 33
android.accept_sdk_license = True
android.minapi = 21
android.archs = arm64-v8a, armeabi-v7a
android.permissions = android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE
android.copy_libs = 1
android.release_artifact = apk

[buildozer]
log_level = 2
