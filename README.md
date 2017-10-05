# Speisekammer Server
A django app to manage products in stock 

## Installation
1. Make sure you have django and django rest framework installed.
2. Create a new django project or change to your existing projects directory
3. git submodule add git://github.com/aldowiese/speisekammer_server
4. Add 'rest_framework' and 'speisekammer_server.apps.SpeisekammerServerConfig' to INSTALLED_APPS
5. Include speisekammer's urls in your projects urlconf
