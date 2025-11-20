[app]

# (str) Title of your application
title = Shock Detector

# (str) Package name
package.name = shockdetector

# (str) Package domain (reverse-domain style)
package.domain = org.example

# (str) Source code where the main.py is located
source.dir = .

# (list) Application requirements
requirements = python3,kivy==2.1.0,plyer,pyjnius

# (str) Icon of the application
icon.filename = assets/icon.png

# (int) target API
android.api = 33

# (int) minimum API your APK will support
android.minapi = 21

# (str) Android entrypoint, default ok
# (list) add permissions
android.permissions = CALL_PHONE, RECEIVE_BOOT_COMPLETED, FOREGROUND_SERVICE

# (bool) Indicate whether the app uses a service
#android.services = myservice:start

# (str) custom package data
# (str) version
version = 0.1

[buildozer]
# (int) log level
log_level = 2

# add or edit this line
# (Use only one: arm64-v8a is recommended)
android.archs = arm64-v8a

