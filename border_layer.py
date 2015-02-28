#!/usr/bin/env python

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.  
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#
# Border Layer
# 2004/02/13
# Werner Hartnagel
# www.dotmagic.de

from gimpfu import *

#have_gimp11 = gimp.major_version > 1 or \
#	      gimp.major_version == 1 and gimp.minor_version >= 1

def pyborder(img, layer, sborder, sblur, scolour, sopacity):
	# Disable Undo
	pdb.gimp_image_undo_group_start(img)
	fg_old = gimp.get_foreground()

	shadow = gimp.Layer(img, "shadow", layer.width, layer.height, RGBA_IMAGE, sopacity, NORMAL_MODE)
	img.add_layer(shadow, 0)
	pdb.gimp_edit_clear(shadow)
	gimp.set_foreground(scolour)
	pdb.gimp_selection_all(img)
	pdb.gimp_selection_shrink(img, sborder)
	pdb.gimp_selection_invert(img)
	pdb.gimp_selection_feather(img,sblur)
	pdb.gimp_edit_fill(shadow, FOREGROUND_FILL)
	

	pdb.gimp_selection_none(img)
	gimp.set_foreground(fg_old)

	# Enable Undo
	pdb.gimp_image_undo_group_end(img)

register(
	"python_fu_border",
	"Add a Layer with border",
	"Add a Layer with border",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2001",
	"<Image>/Python-Fu/Create Layers/Border Layer",
	"RGB*, GRAY*",
	[
		(PF_SLIDER, "border", "The Shadow Border", 3.0, (0, 30, 1.0)),
		(PF_SLIDER, "blur", "The Shadow Blur", 8.0, (0, 20, 0.1)),
		(PF_COLOUR, "colour", "The Shadow Color", (0,0,0)),
		(PF_SLIDER, "opacity", "The opacity", 90, (0, 100, 0.1)),
	],
	[],
	pyborder)

main()
