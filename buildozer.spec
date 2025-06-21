[app]
title = Moaz Video Downloader
package.name = moazdownloader
package.domain = org.moaz.downloader
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ico
version = 1.0
requirements = python3,kivy,hostpython3,openssl,yt-dlp,plyer,ffmpeg
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.minapi = 21
android.icon = moaz.png
# (str) Supported orientation (one of landscape, sensorLandscape, portrait or all)
orientation = portrait
# (list) Permissions
#android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
# (str) Presplash of the application
#android.presplash = presplash.png
# (str) Supported architectures
#android.archs = arm64-v8a, armeabi-v7a, x86, x86_64
# (str) Application entry point
entrypoint = test1.py
# (str) Android NDK version to use
#android.ndk = 23b
# (str) Android SDK version to use
#android.sdk = 24
# (str) Android NDK API to use
#android.ndk_api = 21
# (str) Custom source folders for requirements
# (list) Garden requirements
#garden_requirements =
# (str) Custom source folders for requirements
#custom_source_folders =
# (str) The directory in which python-for-android should look for your own build recipes (if any)
#p4a.local_recipes = 