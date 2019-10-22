# Render Farm Toolset

### What is it exactly?
An addon for Blender3D (version 2.8) that saves us time preparing a .blend file for upload to a render farm, automating a few manual operations.
This comes in useful when the pipeline is structured in a way that divides texture files from blend files, allowing to update each file separately.

### What does it do?
Remap all images in a .blend file to a path given by the user.
Basically it automates what we’ve been doing manually so far:
Pack all images> unpack all > remove all unpacked files > Find missing files > make all paths relative
The script ignores all missing images and reports them at the end of the operation.

### How does it work?
The UI is located under scene properties, along with other render settings.
The only input required is the Remap Path, to which the user wants to link all images.
The path needs to be absolute (not relative), and link to an existing directory.
If conditions are met, the ‘Remap Images’ button will become active, otherwise an error message will detail the problem.

### Anything else?
+ The ‘Remap Images’ button runs some heavy operations (depending on the amount of textures), so blender’s UI may become unresponsive for a short while.
+ Before clicking the button, It’s recommended  to open the system console for a few reasons:
    + the script prints out updates while operating, so you know it’s working even when the UI is unresponsive.
    + You get to follow the operations and make sure everything is as expected
    + At the end of the operation the script reports the missing files that were ignored, it’s up to the user to decide what to do with them.
+ Due to API restrictions, the script uses blender’s predefined directory for unpacked images- a folder named ‘textures’ in the same location as the blend file. Before running make sure there’s nothing important in that folder as it will be deleted.

