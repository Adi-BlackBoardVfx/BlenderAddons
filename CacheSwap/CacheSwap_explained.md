# Cache Swap

### What is it exactly?
An addon for Blender3D (version 2.8) that helps us work efficiently with animation cache files, especially when the pipeline requires constant animation updates.

### What can it do?
Find all scene objects that use the same cache file, and automatically update all of them to a different cache version.
The script is intended for already existing objects (after their initial import), making the actual swap inside the relevant cache modifier.
Handled cache types are: ABC(alembic) \ MDD \ PC2

### How does it work?
The UI is located in the 3D View panel right side panel, under the ‘Cache Swap’ tab.
It displays information based on the active object:
If the active object isn’t linked to any cache file, it will display a message accordingly. Otherwise, the script will identify the current linked cache and display further options.

At this point, the user can enter a path to the updated cache file. In case the new cache file’s name matches the current one, a warning will be displayed.
Clicking on ‘Upload And Swap’ will do the following:
confirm the new given path is valid, and that the file format matches the current one (.acb file can only be swapped with .abc, .mdd/.pc2 can be swapped with each other).
If these conditions aren’t met, the operation will break and an error message will be displayed.
Find all scene objects linked to the same cache as the active object.
Upload the new cache file, and swap the current with the new for all found objects
In case there’s a format change (between .mdd and .pc2), relevant changes will be made to the modifier.
When successfully finished, a message will appear at the bottom info panel:

### It wouldn’t work if…
If the new entered cache path isn’t valid, or is the wrong file format for the swap (example: there’s no swapping between .abc and .mdd)
If the current object has more than one cache modifier- the current cache cannot be identified.
If the relevant objects are linked to different cache files (example: if some of them were already manually swapped) - the automatic swap will occur only in objects linked to the same file.
