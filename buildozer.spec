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

android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

android.permissions = READ_EXTERNAL_STORAGE

[buildozer]
log_level = 2
warn_on_root = 1
