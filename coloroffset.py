#!/usr/bin/env python

# Color Offsets plugin for The Gimp 2.3.x
# Written by Werner Hartnagel

from gimpfu import *

def color_offset(img, layer, offset_red_x, offset_red_y, offset_green_x, offset_green_y, offset_blue_x, offset_blue_y):
	# Disable Undo
	img.undo_group_start()

	# Create new image
	channels = pdb.plug_in_decompose(img, layer, "RGB", True)
	channel_img = channels[0]

	channel_list = channel_img.layers
	channel_num = 0
	col_offsets = ((int(offset_red_x),int(offset_red_y)),(int(offset_green_x),int(offset_green_y)),(int(offset_blue_x),int(offset_blue_y)))
	for curr_layer in channel_list:
		curr_layer.set_offsets(col_offsets[channel_num][0], col_offsets[channel_num][1])
#		pdb.gimp_image_resize_to_layers(channel_img)
		pdb.gimp_layer_resize_to_image_size(curr_layer)
		channel_num += 1
		print curr_layer

	# Create the Pattern Layer
#	pat_lay = gimp.Layer(img, "dot", img.width, img.height, RGBA_IMAGE, 100, NORMAL_MODE)
#	img.add_layer(pat_lay, 0)
#	pdb.gimp_edit_clear(pat_lay)

	pdb.plug_in_recompose(channel_img, channel_list[0])
	# Enable Undo
	img.undo_group_end()

# Register with The Gimp
register(
	"python_fu_color_offset",
	"color offset",
	"color offset",
	"Werner Hartnagel",
	"(c) 2006, Werner Hartnagel",
	"2006",
	"<Image>/Python-Fu/Effects/Color Offset",
	"RGB*",
	[
		(PF_SPINNER, "offset_r", "Red Channel Offset x", 0, (-150, 150, 1)),
		(PF_SPINNER, "offset_r", "Red Channel Offset y", 0, (-150, 150, 1)),
		(PF_SPINNER, "offset_g", "Green Channel Offset x", 10, (-150, 150, 1)),
		(PF_SPINNER, "offset_g", "Green Channel Offset y", 10, (-150, 150, 1)),
		(PF_SPINNER, "offset_b", "Blue Channel Offset x", -10, (-150, 150, 1)),
		(PF_SPINNER, "offset_b", "Blue Channel Offset y", -10, (-150, 150, 1)),
	],
	[],
	color_offset)

main()
