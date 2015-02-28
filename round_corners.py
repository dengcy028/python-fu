#!/usr/bin/env python
#
#   Written by Werner Hartnagel 2005
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

def round_corners(img, layer, border, round, brush):
	# Disable Undo
	pdb.gimp_image_undo_group_start(img)

	# Vars
	fg_old = gimp.get_foreground()	# Save FG Color
	brush_old = pdb.gimp_context_get_brush()

	if not layer.has_alpha:
		layer.add_alpha()
	
	# Create the Pattern Layer
	border_lay = gimp.Layer(img, "border", layer.width, layer.height, RGBA_IMAGE, 100, NORMAL_MODE)
	img.add_layer(border_lay, 0)
	pdb.gimp_edit_clear(border_lay)

	# Draw the Pattern Layer
	pdb.gimp_selection_all(img)
	pdb.gimp_selection_shrink(img, border)
	pdb.script_fu_selection_rounded_rectangle(img, border_lay, round, 0)
	pdb.gimp_selection_feather(img,2)
	pdb.gimp_selection_invert(img)
	pdb.gimp_context_set_brush(brush)
	pdb.gimp_edit_stroke(border_lay)
	#pdb.plug_in_gauss_iir2(img, border_lay, 2, 2)
	pdb.gimp_edit_clear(layer)
	
	# Restore FG Color
	pdb.gimp_selection_none(img)
	pdb.gimp_context_set_brush(brush_old)
	gimp.set_foreground(fg_old)
	
	# Enable Undo
	pdb.gimp_image_undo_group_end(img)

register(
	"python_fu_round_corners",
	"Round the Corners",
	"Round the Corners",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2005",
	"<Image>/Python-Fu/Borders/Round Corners",
	"RGB*, GRAY*",
	[
		(PF_SPINNER, "border", "The Border", 4, (2, 30, 1)),
		(PF_SPINNER, "round", "The Round Corners in %", 8, (1, 30, 1)),
		(PF_BRUSH, "brush", "Brush", "Circle Fuzzy (03)")
	],
	[],
	round_corners)

main()
