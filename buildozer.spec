[app]
title = Vocabulary Assistant
package.name = VocabularyAssistant
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,ttf,ttc
version = 0.1

# Requirements
requirements = python3,kivy,pyjnius,android

# Android specific
android.permissions = RECORD_AUDIO,INTERNET,QUERY_ALL_PACKAGES,WRITE_EXTERNAL_STORAGE, READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
android.ndk = 25
android.sdk = 33
android.target_api = 33

# Add more specific queries for speech recognition
android.manifest.queries = org.kivy.android,com.google.android.googlequicksearchbox
android.manifest.queries.intent = android.speech.RecognitionService,android.speech.action.RECOGNIZE_SPEECH

# Add required hardware feature
android.manifest.features = android.hardware.microphone

# Basic settings
orientation = portrait
fullscreen = 0
android.arch = arm64-v8a

# Optional: If you want to use a specific Python version
python_version = 3

# (str) Application icon. (see https://kivy.org/doc/stable/guide/packaging-android.html#icon)
icon.filename = learn.png

# (str) Android icon (used for the app icon in the launcher)
android.icon = learn.png

# (str) Path to the splash screen image (optional)
android.splash = learn.png

# (str) Presplash screen image filename (optional)
presplash.filename = learn.png

[buildozer]
log_level = 2
warn_on_root = 1 