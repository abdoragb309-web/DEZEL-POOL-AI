[app]
title = DEZEL POOL AI
package.name = dezelpoolai
package.domain = org.dezel
source.dir = .
source.include_exts = py,png,jpg,jpeg,webp,kv,atlas,txt
version = 1.0.0
requirements = python3,kivy
orientation = portrait
fullscreen = 0

# Android settings
android.api = _for_buildozer_default
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

# Permissions are intentionally minimal. If gallery access behaves differently
# on your Android version, use the in-app file chooser or copy an image into the app folder.
android.permissions = READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
