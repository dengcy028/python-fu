#!/usr/bin/env python

# Gimp Halftone-Border plugin for The Gimp 2.6.x (Python-Fu Version).

# Written by Werner Hartnagel 06/2011
# www.pythonfu.sf.net

from gimpfu import *


def cubicbd(img, drawable, border_width, radius, blur, keep_mask):
	# Initial Suff
	width = drawable.width
	height = drawable.height
	img.undo_group_start()
	pdb.gimp_selection_none(img)

	x1 = border_width
	y1 = border_width
	wx = drawable.width - (2*border_width)
	wy = drawable.height - (2*border_width)

	pdb.gimp_rect_select(img, x1, y1, wx, wy, 0, False, 0)
	channel = pdb.gimp_selection_save(img)
	pdb.gimp_selection_none(img)
#	pdb.plug_in_gauss_rle2(img, channel, 1.6*border_width, 1.6*border_width)
	pdb.plug_in_cubism(img, channel, radius, 10.0, 0)

	if blur > 0:
		pdb.plug_in_gauss_rle2(img, channel, blur, blur)

	pdb.gimp_edit_copy(channel)
	mask = pdb.gimp_layer_create_mask(drawable, 6)
	pdb.gimp_layer_add_mask(img.layers[0], mask)
	pdb.gimp_edit_paste(mask,0)
	pdb.gimp_image_remove_channel(img, channel)
	pdb.gimp_floating_sel_anchor(pdb.gimp_image_get_floating_sel(img))

	if not keep_mask:
		pdb.gimp_image_remove_layer_mask(img, img.layers[0], 0)

	# Final Stuff
	img.undo_group_end()
	gimp.delete(img)

register(
	"python_fu_cubic_border",
	"Create a Cubic-Border",
	"Create a Cubic-Border with Scanlines using the foreground color",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2011",
	"<Image>/Python-Fu/Frame/Cubic-Border",
	"RGB*, GRAY*",
	[
		(PF_SPINNER, "border_width", "Border Width", 20, (10, 200, 1)),
		(PF_SPINNER, "radius_width", "Radius Width", 4, (2, 30, 1)),
		(PF_SPINNER, "blur_width", "Fade Background", 2, (0, 10, 1)),
        (PF_TOGGLE, "keep_mask", "Keep mask", False),
	],
	[],
	cubicbd)

main()
