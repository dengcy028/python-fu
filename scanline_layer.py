#!/usr/bin/env python

from gimpfu import *


def scanlines(img, layer, horizontal, bar_width, bar_space, opacity, blurlines, bar_inc, bar_steps, space_inc, space_steps):
	pdb.gimp_image_undo_group_start(img)
	fg_old = gimp.get_foreground()
	pdb.gimp_selection_none(img)
	scanlines = gimp.Layer(img, "scanlines", layer.width, layer.height, RGBA_IMAGE, opacity, NORMAL_MODE)
	img.add_layer(scanlines, 0)
	pdb.gimp_edit_clear(scanlines)
	max_x = scanlines.width
	max_y = scanlines.height
	unit_lenght = bar_width + bar_space
	bar_count = 0
	pos = 0
	if horizontal:
		max = max_y
	else:
		max = max_x
	while pos < max:
		bar_count = bar_count + 1
		if horizontal:
			pdb.gimp_rect_select(img, 0, pos, max_x, bar_width, 0, False, 0)
		else:
			pdb.gimp_rect_select(img, pos, 0, bar_width, max_y, 0, False, 0)
		if bar_inc and (bar_count % bar_steps==0):
			bar_width = bar_width + 1
			pos = pos - 1
			unit_lenght = bar_width + bar_space
		if space_inc and (bar_count % space_steps==0):
			bar_space = bar_space + 1
			pos = pos - 1
			unit_lenght = bar_width + bar_space
		pos = pos + unit_lenght
	pdb.gimp_edit_fill(scanlines, FOREGROUND_FILL)
	pdb.gimp_selection_none(img)
	if blurlines != 0:
	  pdb.plug_in_gauss_rle2(img, scanlines, blurlines, blurlines)
	# Restore Settings
	gimp.set_foreground(fg_old)
	pdb.gimp_image_undo_group_end(img)

register(
	"python_fu_scanline_layer",
	"Add a Layer with horizontal or vertical Lines using Foreground Color",
	"Add a Layer with horizontal or vertical Lines using Foreground Color.\n\nPlay with the Options and have Fun ;-]",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2001",
	"<Image>/Python-Fu/Create Layers/Scanline Layer",
	"RGB*, GRAY*",
	[
		(PF_BOOL, "Horizontal_Orientation", "Horizontal Orientation", 1),
		(PF_SPINNER, "Bar_Width", "Bar Width", 2, (1, 21, 1)),
		(PF_SPINNER, "Bar_space", "Bar Space", 2, (1, 21, 1)),
		(PF_SLIDER, "Opacity", "The Opacity", 100, (1, 100, 10)),
		(PF_SPINNER, "Blur_Lines", "Blur the Lines", 0, (0, 10, 1)),
		(PF_SPINNER, "Inc_Bar_Width", "Increase Bar Width", 0, (0, 10, 1)),
		(PF_SPINNER, "Inc_Bar_Steps", "Increase Width every x line", 0, (1, 30, 1)),
		(PF_SPINNER, "Inc_Space_Width", "Increase Space Width", 0, (0, 10, 1)),
		(PF_SPINNER, "Inc_Space_Steps", "Increase Space every x line", 0, (1, 30, 1))
	],
	[],
	scanlines)

main()
