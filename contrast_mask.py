#!/usr/bin/env python

# Contrast Mask - Based on the Idea from Eric R. Jeschke (http://redskiesatnight.com/)
# 2004 Werner Hartnagel

from gimpenums import *
from gimpfu import *


def contrast_mask(img, layer, opacity, blur):
	# Disable Undo
	pdb.gimp_image_undo_group_start(img)

	# Make the Contrast Mask
	contrast_mask = layer.copy(1)
	img.add_layer(contrast_mask, 0)
	contrast_mask.name = "Contrast Mask"
	pdb.gimp_desaturate(contrast_mask)
	pdb.plug_in_gauss_iir2(img, contrast_mask, blur, blur)
	contrast_mask.mode = OVERLAY_MODE
	pdb.gimp_invert(contrast_mask)
	contrast_mask.opacity = opacity
	
	# Enable Undo
	pdb.gimp_image_undo_group_end(img)

register(
	"python_fu_contrast_mask",
	"Brings out details in an image that may be washed out or lost in shadow.",
	"Brings out details in an image that may be washed out or lost in shadow.",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2004",
	"<Image>/Python-Fu/Create Layers/Contrast Mask",
	"RGB*, GRAY*",
	[
		(PF_SLIDER, "opacity", "Mask Opacity", 75, (1, 101, 1)),
		(PF_SPINNER, "blur", "Sharpness", 10, (0, 31, 1)),
	],
	[],
	contrast_mask)

main()
