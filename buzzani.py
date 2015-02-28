#!/usr/bin/env python

# Gimp scanlines plugin for The Gimp 2.4 (compiled with --enable-python).

# Written by Werner Hartnagel 09/2007
# www.dotmagic.de

from gimpfu import *

def scanlines2(img, drawable, bg_col_x, bg_col_y, fill_pat, startplay):
	# Initial Suff
	img.undo_group_start()
	old_pat = pdb.gimp_context_get_pattern()

	# Active Layer
	frame0 = img.active_layer

	# Pattern Fill
	frame1 = frame0.copy()
	img.add_layer(frame1, 1)
	frame1.name = "Frame 1"
	pdb.gimp_context_set_pattern(fill_pat)
	pdb.gimp_edit_bucket_fill(frame1, PATTERN_BUCKET_FILL, COLOR_ERASE_MODE, 100, 75, False, bg_col_x, bg_col_y)

	# Blue Linar
	frame2 = frame0.copy()
	frame2.name = "Frame 2"
	img.add_layer(frame2, 2)
	pdb.plug_in_mblur(img, frame2, 0, 30, 270, img.width/2, img.height/2)

	# Blur Radial
	frame3 = frame0.copy()
	img.add_layer(frame3, 3)
	frame3.name = "Frame 3"
	pdb.plug_in_mblur(img, frame3, 1, 0, 90, img.width/2, img.height/2)

	# Blur Zoom
	frame4 = frame0.copy()
	frame4.name = "Frame 4"
	img.add_layer(frame4, 4)
	pdb.plug_in_mblur(img, frame4, 2, 30, 0, img.width/2, img.height/2)

	# Final Stuff
	pdb.gimp_context_set_pattern(old_pat)
	img.undo_group_end()

	# Animation Player
	if startplay:
		pdb.plug_in_animationplay(img, drawable)

register(
	"python_fu_buzz_animation",
	"Create a Buzz Animation",
	"Create a Animation with varius Layer Effects like blur, disortion",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2007",
	"<Image>/Python-Fu/Create Layers/Buzz Animation",
	"RGB*, GRAY*",
	[
		(PF_SPINNER, "bg_col_x", "Fill Color Position x", 20, (1, 101, 1)),
		(PF_SPINNER, "bg_col_y", "Fill Color Position y", 20, (1, 101, 1)),
		(PF_PATTERN, "fill_pat", "Fill Pattern", 'Electric Blue'),
		(PF_TOGGLE, "startplay", "Start Animation Player", 1)
	],
	[],
	scanlines2)

main()
