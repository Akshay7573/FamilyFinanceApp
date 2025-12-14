[app]
# (str) Title of your application
title = Family Finance

# (str) Package name
package.name = familyfinance

# (str) Package domain (use your own reverse domain)
package.domain = org.eduforge

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (extend if you add images/fonts/etc.)
source.include_exts = py,png,jpg,jpeg,kv,ttf,txt,json,atlas

# (str) Application versioning (simple)
version = 0.1

# (list) Application requirements
# Important: add every python library you import
requirements = python3,kivy,kivymd,requests

# (str) Supported orientation (one of landscape, portrait or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash / icon can be added later if you want
# presplash.filename = %(source.dir)s/data/presplash.png
# icon.filename = %(source.dir)s/data/icon.png

# ------------------------------
# Android specific
# ------------------------------
# (int) Android API to use. 33 works well for most.
android.api = 33

# (int) Minimum API your APK will support
android.minapi = 21

# (list) Android archs to build for
android.archs = arm64-v8a, armeabi-v7a

# (list) Permissions (your app uses internet because of requests + Google Script URL)
android.permissions = android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE

# (bool) Copy libraries instead of creating a single .so file
android.copy_libs = 1

# (str) If you want APK instead of AAB in some setups, keep this:
android.release_artifact = apk

[buildozer]
# (int) Log level (0 = error, 1 = info, 2 = debug)
log_level = 2
