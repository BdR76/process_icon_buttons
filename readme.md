process_icon_buttons.py
=======================

This GIMP Python script can be used when designing button icons for games or
websites. It automates the processing and resizing of the final button images,
while keeping the high definition original image unchanged.

![From GIMP image to separate png files](/preview.png?raw=true "preview")

What is it
----------
Graphics assets such as buttons are usually created in a high resolution
layered image. For example there is a layer with a colored backface, an
outline, glossy effects and so on, and for each separate button, only the icon
(play, reset, menu etc.) changes. This ensures all the buttons look the same
and also allows you to keep the original design in high resolution, for making
any changes at a later time or adding new buttons.

Using this high resolution image as starting point, the individual buttons can
be created by toggling the appropriate layers to visible, then copy&paste to a
new image, resize, save as PNG, and then repeat for the next button and so on.
However this process is tedious and takes a lot of time when done by hand.

The GIMP Python script `process_icon_buttons.py` automates the process of
selecting, resizing and exporting the buttons icon from a "master image" file.

How to use it
-------------
Download and install [GIMP](https://www.gimp.org/) and copy the file
`process_icon_buttons.py` into the following directory:

	.\GIMP 2\lib\gimp\2.0\plug-ins\

After you've put the file in the plug-ins directory, open GIMP and there
should be a new menu item available, under `Tools -> Process icon buttons`.

Use GIMP to design a button using separate layers for all the elements. As a
reference see the example image provided in the file `button_example.xcf`.
Design the button elements in normal layers, and place each icon in a separate
`Layer Group`. Toggle the layers visibility to get desired button composition,
and then start the `Process icon buttons` menu item.

First, choose a folder where you want to save the exported button image files.
The script processes the image by going through all `Layer Group`, making it
visible and then exporting it to a .PNG file. The name of the group determines
the export filename. For example the group name `btn_play [64]` will result in
a file called `btn_play.png` with image size 64 pixel width, new height is adjusted
automatically according to aspect ratio of image.

After you've exported all buttons, you can select different layers and then
export again, for example to create a "highlight" version of each button.
You can optionally use the textbox "Add post-fix to filename" to add for
example "_hl" to each filename, so that `btn_play [64]` will be exported
as `btn_play_hl.png`.

Known bugs / trouble shooting
-----------------------------
If you start the plug-in while a Layer Group is selected,
then you will get the following error message:

	TypeError: can't pickle GroupLayer objects

This is due to a [bug in GIMP](https://github.com/efexgee/mapper/issues/1).
Simply select another layer, so a layer without a (-) or (+) symbol
in front of it. Then try again and it should work correctly.


Questions, comments -- Bas de Reuver (bdr1976@gmail.com)
