#!/usr/bin/env python

#   Gimp-Python - allows the writing of Gimp plugins in Python.
#   Copyright (C) 2005  Werner Hartnagel <info@dotmagic.de>
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

from gimpfu import *
import random


def getGrayValue(rgb):
	return (0.30 * rgb[0]) + (0.59 * rgb[1]) + (0.11 * rgb[2])

def getInvertValue(rgb):
	return (255-rgb[0], 255-rgb[1], 255-rgb[2])

def py_magicmesh(img, layer, dot_shape, min_radius, max_radius, sspace, dot_matrix):
	# Disable Undo
	img.undo_group_start()
	
	# Save the org. colors
	fg_old = gimp.get_foreground()

	# Create the Layer for the Mesh.
	dotimage = gimp.Layer(img, "dotimage", layer.width, layer.height, RGBA_IMAGE, 100, NORMAL_MODE)
	img.add_layer(dotimage, 0)
	pdb.gimp_layer_set_offsets(dotimage, layer.offsets[0], layer.offsets[1])
	pdb.gimp_edit_clear(dotimage)
	
	# Set some defaults
	max_x = layer.width + layer.offsets[0]
	max_y = layer.height + layer.offsets[1]
	dot_width = 2*max_radius
	pat_width = 2*max_radius + sspace
	mspace = (pat_width - dot_width) / 2
	sspace = sspace / 2
	
	for pos_x in range(sspace+layer.offsets[0], max_x-max_radius, pat_width):
		for pos_y in range(sspace+layer.offsets[0], max_y-max_radius, pat_width):
			if dot_matrix == "regular":
				diameter = dot_width
				av_color = pdb.gimp_image_pick_color(img, layer, pos_x+mspace, pos_y+mspace, 1, 1, diameter)
				
			elif dot_matrix == "random":
				diameter = round(random.randint(2*min_radius, 2*max_radius))
				mspace = (pat_width - diameter) / 2
				av_color = pdb.gimp_image_pick_color(img, layer, pos_x+mspace, pos_y+mspace, 1, 1, diameter)
				
			elif dot_matrix == "value":
			#	print pos_x, pos_y
				av_color = pdb.gimp_image_pick_color(img, layer, pos_x+mspace, pos_y+mspace, 1, 1, dot_width)
				gray_val = getGrayValue(av_color)
				gray_multi = (255-gray_val) / 255
				
				diameter = int(gray_multi * (max_radius - min_radius)) + min_radius
				diameter = diameter * 2
				mspace = (pat_width - diameter) / 2
				#if diameter > 10:
				#	print gray_multi, (255-gray_val) / 255
				#	print diameter, mspace, diameter+mspace, pat_width
				
			if dot_shape == "circle":
				pdb.gimp_ellipse_select(img, pos_x+mspace, pos_y+mspace, diameter, diameter, CHANNEL_OP_REPLACE, True, 0, 0)
			else:
				pdb.gimp_rect_select(img, pos_x+mspace, pos_y+mspace, diameter, diameter, CHANNEL_OP_REPLACE, 0, 0)

			gimp.set_foreground(av_color)
			pdb.gimp_edit_fill(dotimage, 0)
			
	#pdb.plug_in_colorify(img, layer, scolour)
	pdb.gimp_selection_none(img)
	gimp.set_foreground(fg_old)

	# Enable Undo
	img.undo_group_end()

register(
	"python_fu_magicmesh",
	"Create a Mesh with dots or rectangle based on the colors of the current Layer.",
	"magicmesh v0.2",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2005-08-25",
	"<Image>/Python-Fu/Create Layers/Magicmesh",
	"RGB*, GRAY*",
	[
		(PF_RADIO, "dot_shape", "Dot Shape: ", "circle", (("circle", "circle"), ("rectangle", "rectangle"))),
		(PF_SPINNER, "min_radius", "Min. Radius: ", 3, (1, 20, 1)),
		(PF_SPINNER, "max_radius", "Max. Radius: ", 9, (1, 20, 1)),
		(PF_SPINNER, "space", "Space between dots: ", 2, (0, 20, 1)),
		(PF_RADIO, "dot_matrix", "The Matrix is: ", "regular", (("regular", "regular"), ("random", "random"), ("value", "value")))
	],
	[],
	py_magicmesh)

main()
