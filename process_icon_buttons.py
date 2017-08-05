#!/usr/bin/env python
# coding: utf-8

# Process icon buttons
# layout of button stored in layers, a group layer for each icon
# Iterate all icon groups, copy, resize and export to png

from gimpfu import *
import os

# remove any <chars> character in string <s>
def remchars(s, chars):
	str = s
	for n in chars:
		str = str.replace(n, "")
	return str

# check if a string value represents a valid integer
def RepresentsInt(s):
	try: 
		int(s)
		return True
	except ValueError:
		return False

def process_iconbtn(image, img_path, name, postfix):
	# determine export size width, for example name is "icon play [64]" width is 64 pixels
	wpx = -1 # new width in pixels

	# check if Layer Group name contains brackets '[' and ']'
	if (name.find('[') > -1) and (name.find(']') > -1):
		# find value between brackets
		pos1 = name.index('[')
		pos2 = name.index(']')
		wd = name[pos1+1:pos2]
		# check if value is a valid integer
		if (RepresentsInt(wd)):
			# cast to int and strip from name, example "icon play [64]" -> name=icon play, wpx=64
			wpx = int(wd)
			name = name[:pos1-1]
			name = name.strip() # trim

	# prepare export filename based on path name
	img_name = name.replace(" ", "_") + postfix
	img_name = remchars(img_name, "#<>,'\"/=%?¿!¡") # remove illegal chars
	filename = "%s\%s.%s" % (img_path, img_name, "png")

	# create selection based on path
	pdb.gimp_rect_select(image, 0, 0, 1024, 1024, 2, 0, 0) # img, x, y, w, h, op (2=CHANNEL-OP-REPLACE), feather=0, feather-radius=0
	
	# copy and paste as new temporary image
	# pdb.gimp_edit_copy(image.layers[0])
	pdb.gimp_edit_copy_visible(image)
	tmp_img = pdb.gimp_edit_paste_as_new()
	
	# resize new image
	# w = tmp_img.width
	# h = tmp_img.height
	# pdb.gimp_progress_init("Scaling Image...",None)
	if (wpx > 0):
		pdb.gimp_context_set_interpolation(INTERPOLATION_LANCZOS)
		pdb.gimp_image_scale(tmp_img, wpx, wpx)

	# save to file and clean up temporary image
	pdb.gimp_file_save(tmp_img, tmp_img.active_layer, filename, filename)
	pdb.gimp_image_delete(tmp_img)

	return
	
def process_icon_buttons(img, layer, path, pfx):

	# trim any spaces
	pfx = pfx.strip()
	
	# first make all icon (Layer Groups) invisible
	for mylayer in img.layers:
		#check if layer is a group and drill down if it is
		if pdb.gimp_item_is_group(mylayer):
			mylayer.visible = False

	# iterate all layers
	for mylayer in img.layers:
		# check if layer is a group
		if pdb.gimp_item_is_group(mylayer):
			# make Layer Group icon visible and process it
			mylayer.visible = True
			process_iconbtn(img, path, mylayer.name, pfx)
			mylayer.visible = False

	# GIMP dialog already shows process bar, so end message not needed
	#pdb.gimp_message('Process icon buttons is ready')

# tell gimp about our plugin
register(
	"python_fu_process_icon_buttons",
	"Process icon buttons\nPlug-in to process a layered image with icon buttons\nand copy, resize and export them to separate png files",
	"Process icon buttons layergroups and export as png files",
	"Bas de Reuver",
	"Bas de Reuver",
	"2017",
	"<Image>/Tools/Process icon buttons", # menu path
	"", # Create a new image, don't work on an existing one
	[
		(PF_DIRNAME, "p1", "Export destination directory", "/tmp"),
		(PF_STRING,  "p2", "Add post-fix to filename\n(optional)", "")
	],
	[],
	process_icon_buttons
)

main()
