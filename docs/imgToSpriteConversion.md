# Sprite Sheet Generation

The images from imgData are converted into sprite sheets using [Free texture packer](https://github.com/odrick/free-tex-packer).

texturePacker.ftpp in imgData is a project file that has all the required ssettings selected.

## Free texture packer settings

### Settings turned on

* Remove file ext
* Power of two
* Allow trim
* Detect identical

ALl other checkbox settings can be assumed to be turned off

### Chosen Settings

* Texture format: png
* Format: JSON (hash)
* Scale: 1
* Trim mode: trim
* Alpha threshold: 0
* Packer: MaxRectsPacker
* Method: Smart

### File Names

Both the json file and texture file have the same name as the folder they are from.

