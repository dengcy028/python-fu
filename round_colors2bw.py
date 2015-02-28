#!/usr/bin/env python

# based on Tutorial from: http://gug.sunsite.dk/tutorials/tomcat4/

from gimpfu import *

def round_colors2bw(img, layer, rblur, in_low, in_high):
	# Disable Undo
	img.undo_group_start()
	lay_round = layer.copy()
	
	img.add_layer(lay_round, 0)
	if not pdb.gimp_drawable_is_gray(lay_round):
		pdb.gimp_desaturate(lay_round)
	pdb.plug_in_gauss_iir2(img, lay_round, rblur, rblur)
	pdb.gimp_levels(lay_round, 0, 119, 135, 1.0, 0, 255)
	pdb.gimp_drawable_set_name(lay_round, "Round Image")
	
	# Enable Undo
	img.undo_group_end()

register(
	"python_fu_round_colors2bw",
	"Copy a the current (Grayscale) Layer and highpass/lowpass the Gray Values.",
	"Copy a the current (Grayscale) Layer and highpass/lowpass the Gray Values.",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"12-27-2001",
	"<Image>/Python-Fu/Create Layers/Highpass-Lowpass Gray Values",
	"RGB*, GRAY*",
	[
		(PF_SLIDER, "rblur", "The Round Value", 20, (5, 40, 0.1)),
		(PF_SLIDER, "in_low", "Intensity of lowest Input", 119, (0, 255, 1)),
		(PF_SLIDER, "in_high", "Intensity of highest Input", 135, (0, 255, 1)),
	],
	[],
	round_colors2bw)

main()
