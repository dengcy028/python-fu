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
# Color Contur
# 2004/02/13
# Werner Hartnagel
# www.dotmagic.de


from gimpenums import *
from gimpfu import *

def colorcontour(img, layer, blur):
	# Disable Undo
	img.undo_group_start()

	# Make the Contrast Mask
	contrast_mask = layer.copy(1)
	img.add_layer(contrast_mask, 0)
	contrast_mask.name = "Contrast Mask"
	pdb.gimp_desaturate(contrast_mask)
	pdb.plug_in_gauss_iir2(img, contrast_mask, blur, blur)
	contrast_mask.mode = MULTIPLY_MODE
	pdb.gimp_invert(contrast_mask)
	pdb.plug_in_edge(img, contrast_mask, 2, 1, 1)
	
	# Enable Undo
	img.undo_group_end()

register(
	"python_fu_colorcontour",
	"Color Contur.",
	"Color Contur.",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2004",
	"<Image>/Python-Fu/Create Layers/Color Contour",
	"RGB*, GRAY*",
	[
		(PF_SPINNER, "blur", "Contour Width", 10, (0, 31, 1)),
	],
	[],
	colorcontour)

main()
