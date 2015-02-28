#!/usr/bin/env python

# Gimp Cubic Patterns plugin for The Gimp 2.3.x (Python-Fu Version).
# Written by Werner Hartnagel

from gimpfu import *

def cubic_patterns(width, height, size, seamless):
	oldcolor = gimp.get_background()
	gimp.set_background((184,182,17))

	# Create new image
	img = gimp.Image(width, height, RGB)
	# Disable Undo
	img.undo_group_start()

	# Background Layer
	bg_layer = gimp.Layer(img, "Background", width, height, RGBA_IMAGE, 100, NORMAL_MODE)
	img.add_layer(bg_layer, 0)
	bg_layer.fill(BACKGROUND_FILL)

	layer = gimp.Layer(img, "Cubic Pattern", width, height, RGBA_IMAGE, 100, NORMAL_MODE)
	img.add_layer(layer, -1)
	pdb.gimp_image_set_active_layer(img, layer)
	draw = pdb.gimp_image_get_active_drawable(img)
	layer.fill(BACKGROUND_FILL)

	gimp.set_background((0,0,0))
	pdb.plug_in_cubism(img, layer, size, 1.6, 0)
	pdb.plug_in_edge(img, layer, 4, 0, 1)
	pdb.gimp_colorize(layer, 110, 80, 30)

	# Create seamless image?
	if (seamless):
		pdb.plug_in_make_seamless(img, draw)

	# Finish up
	gimp.set_background(oldcolor)

	# Enable Undo
	img.undo_group_end()

	disp1 = gimp.Display(img)

# Register with The Gimp
register(
	"python_fu_pattern_cubic",
	"Renders a Cubic Pattern useable for Background",
	"Renders a Cubic Pattern useable for Background",
	"Werner Hartnagel",
	"(c) 2006, Werner Hartnagel",
	"2006",
	"<Toolbox>/Xtns/Python-Fu/Patterns/Cubic Patterns",
	"",
	[
		[PF_INT32, "width", "Image Width", 256],
		[PF_INT32, "height", "Image Height", 256],
		(PF_SPINNER, "size", "The Diameter", 20, (3, 150, 1)),
		[PF_TOGGLE, "seamless", "Make Seamless", 0],
	],
	[],
	cubic_patterns)

main()
