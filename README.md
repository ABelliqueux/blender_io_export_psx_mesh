![Pic or it didn't happen](https://wiki.arthus.net/assets/blender-psx.jpg)

# Blender 3dcam PSX engine Level exporter

This Blender plugin is to be used in conjunction with the [3dcam PSX engine](https://github.com/ABelliqueux/3dcam-headers).  
It allows exporting a gouraud shaded, UV textured Blender scene to a format compatible with the aforementionned engine.  

![3d scene](https://wiki.arthus.net/assets/demo.gif)

## Documentation

[Check the Wiki](https://github.com/ABelliqueux/blender_io_export_psx_mesh/wiki) for in-depth informations.

## Features

**Be warned this is WIP** !

### Plugin

  * Export UV textured models
  * Export vertex painted models
  * Export camera positions for in game use
  * Export vertex animations
  * Export up to 3 light sources
  * Export pre-rendered backgrounds for in-game use (8bpp and 4bpp)
  * VRam auto layout for TIMs
  * Export sound/music as VAG/XA files

![comparison](https://wiki.arthus.net/assets/rt-8b-4b.gif)  
Real-time 3D / 8bpp background / 4bpp background

## Planned

  * Fix and improve all the things !

# Install the plugin

**This plugin is not compatible with Blender > 2.79.**

1. Download and install Blender 2.79b.

http://download.blender.org/release/Blender2.79/

2. Clone this repository in the [addons folder](https://docs.blender.org/manual/en/latest/advanced/blender_directory_layout.html) of blender 2.79 :

```bash
git clone https://github.com/ABelliqueux/blender_io_export_psx_mesh.git
```

3. Dependencies 

These utilities should be in your [$PATH](https://stackoverflow.com/questions/44272416/how-to-add-a-folder-to-path-environment-variable-in-windows-10-with-screensho#44272417) :

  * [pngquant](https://pngquant.org/) : convert image to 4/8bpp palettized pngs
  * [ffmpeg](https://ffmpeg.org/) : convert audio to WAV
  * [img2tim](https://github.com/Lameguy64/img2tim) : convert image to psx TIM - Win32 pre-built bin : https://github.com/Lameguy64/img2tim#download
  * [wav2vag](https://github.com/ColdSauce/psxsdk/blob/master/tools/wav2vag.c) : convert WAV to psx VAG - Win32 pre-built bin :  http://psx.arthus.net/tools/wav2vag-win32.zip
  * [psxavenc](https://github.com/ABelliqueux/candyk-psx/tree/master/toolsrc/psxavenc) : convert WAV to psx XA  - Win32 pre-built bin :  http://psx.arthus.net/sdk/candyk-psx-tools.zip
  * [xainterleave](https://github.com/ABelliqueux/candyk-psx/tree/master/toolsrc/xainterleave) : interleave psx XA files - Win32 pre-built bin :  http://psx.arthus.net/sdk/candyk-psx-tools.zip

For users with **Imagemagick** installed, there is an option when exporting to use that instead of pngquant.  

4. Enable the add-on in Blender by going to user preferences, Add-ons tab, and enable `Import-Export: PSX TMesh exporter`.  

On Linux : `~/.config/blender/2.79/scripts/addons`  
On macOS : `./Blender.app/Contents/Resources/2.79/addons`  
On Windows : `%USERPROFILE%\AppData\Roaming\Blender Foundation\Blender\2.93\`  

# Install the 3D engine

Head over to the [3dcam repo](https://github.com/ABelliqueux/3dcam-headers) and follow the setup instructions there.

# Export your scene !

Open a working copy of your scene, add the needed [flags](https://github.com/ABelliqueux/blender_io_export_psx_mesh/wiki/Flags) and export your level in the `3dcam-headers` folder.
Following [those steps](https://github.com/ABelliqueux/3dcam-headers#compiling), you should now see your scene running on PSX !

# Custom properties helper add-on

## 3dcam-helper

A [small blender addon](https://github.com/ABelliqueux/blender_io_export_psx_mesh/blob/main/3dcam-engine-helper.py) is provided that facilitates setting and copying [flags](https://github.com/ABelliqueux/blender_io_export_psx_mesh/wiki/Flags) between several objects in your scene.

![Setting an object's flags](https://wiki.arthus.net/assets/3dcam-helper-flags.gif)  

See [the documentation](https://github.com/ABelliqueux/blender_io_export_psx_mesh/wiki/Flags#3dcam-helper) for usage instruction.

**The script only does the job of creating/updating the object's custom properties, so it is not mandatory to use it.**

# Credits

Based on the [code](https://pastebin.com/suU9DigB) provided by TheDukeOfZill, 04-2014, on http://www.psxdev.net/forum/viewtopic.php?f=64&t=537#p4088  
pngquant : [https://github.com/kornelski/pngquant](https://github.com/kornelski/pngquant)  
img2tim : [https://github.com/Lameguy64/img2tim](https://github.com/Lameguy64/img2tim)  
Freeimage : [https://freeimage.sourceforge.io/](https://freeimage.sourceforge.io/)  
