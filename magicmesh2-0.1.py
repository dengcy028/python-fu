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

def pymagicmesh2(img, layer, format, sradius, sspace, is_mask):
	sradius = int(sradius)
	sspace = int(sspace)
	if format == "png":
		pydotimage(img, layer, sradius, sspace, is_mask)
	else:
		pydotimage_svg(img, layer, sradius, sspace, is_mask)


def pydotimage(img, layer, sradius, sspace, is_mask):
	# Disable Undo
	img.undo_group_start()

	# Vars
	pat_width = (2*sradius) + (2*sspace)
	pat_height = pat_width
	dot_width = 2*sradius
	fg_old = gimp.get_foreground()	# Save FG Color

	# Create pixelized Copy from org. Layer
	dotimage = layer.copy()
	img.add_layer(dotimage, 0)
	dotimage.name = "Dot Layer"

	# Create the Pattern Layer
	pat_lay = gimp.Layer(img, "dot", pat_width, pat_height, RGBA_IMAGE, 100, NORMAL_MODE)
	img.add_layer(pat_lay, 0)
	pdb.gimp_edit_clear(pat_lay)

	# Pixelize the Layer
	#pdb.plug_in_pixelize2(img, dotimage, pat_width, pat_height)
	pdb.plug_in_pixelize(img, dotimage, pat_width)

	# Draw the Pattern Layer
	pdb.gimp_ellipse_select(img, sspace, sspace, dot_width, dot_width, CHANNEL_OP_REPLACE, 0, 0, 0)
	pdb.gimp_edit_fill(pat_lay, 0)
	#pdb.plug_in_tile(img, pat_lay, 2*pat_width, 2*pat_height, FALSE)
	pdb.plug_in_tile(img, pat_lay, img.width, img.height, False)

	if is_mask:
		if not dotimage.has_alpha:
			dotimage.add_alpha()
		pat_mask = pdb.gimp_layer_create_mask(pat_lay, ADD_ALPHA_MASK)
		pdb.gimp_layer_add_mask(dotimage, pat_mask)
		img.remove_layer(pat_lay)

	# Restore FG Color
	pdb.gimp_selection_none(img)
	gimp.set_foreground(fg_old)
	# Enable Undo
	img.undo_group_end()

def pydotimage_svg(img, layer, sradius, sspace, is_mask):
	pdb.gimp_image_undo_group_start(img)

	# Vars
	pat_width = (2*sradius) + (2*sspace)
	pat_height = pat_width
	dot_width = 2*sradius
	fg_old = gimp.get_foreground()	# Save FG Color

	# Create pixelized Copy from org. Layer
	dotimage = layer.copy()
	img.add_layer(dotimage, 0)
	dotimage.name = "Dot Layer"

	# Create the Pattern Layer
	pat_lay = gimp.Layer(img, "dot", pat_width, pat_height, RGBA_IMAGE, 100, NORMAL_MODE)
	img.add_layer(pat_lay, 0)
	pdb.gimp_edit_clear(pat_lay)

	# Pixelize the Layer
	#pdb.plug_in_pixelize2(img, dotimage, pat_width, pat_height)
	pdb.plug_in_pixelize(img, dotimage, pat_width)

	# Draw the Pattern Layer
	pdb.gimp_ellipse_select(img, sspace, sspace, dot_width, dot_width, CHANNEL_OP_REPLACE, 0, 0, 0)
	pdb.gimp_edit_fill(pat_lay, 0)
	#pdb.plug_in_tile(img, pat_lay, 2*pat_width, 2*pat_height, FALSE)
	pdb.plug_in_tile(img, pat_lay, img.width, img.height, False)

	if is_mask:
		if not dotimage.has_alpha:
			dotimage.add_alpha()
		pat_mask = pdb.gimp_layer_create_mask(pat_lay, ADD_ALPHA_MASK)
		pdb.gimp_layer_add_mask(dotimage, pat_mask)
		img.remove_layer(pat_lay)

	# Restore FG Color
	pdb.gimp_selection_none(img)
	gimp.set_foreground(fg_old)
	pdb.gimp_image_undo_group_end(img)

register(
	"python_fu_magicmesh2",
	"pymagicmesh2",
	"pymagicmesh2",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2005",
	"<Image>/Python-Fu/Create Layers/Magicmesh2 (With Mask)",
	"RGB*, GRAY*",
	[
		(PF_RADIO, "image_extension", "The format of the images: {svg, png}", "png", (("svg", "svg"), ("png", "png"))),
		(PF_SPINNER, "radius", "The Radius", 5, (3, 30, 1)),
		(PF_SPINNER, "space", "The Space", 2, (1, 30, 1)),
		(PF_TOGGLE, "is_mask", "Layer Mask", 1)
	],
	[],
	pymagicmesh2)

main()
