#!/usr/bin/env python

# Water paint effect script  for GIMP 2.3
#   <Image>/Python-Fu/Effects/Water Paint Effect...
# 
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
from gimpfu import *

def python_fu_water_paint_effect(img, inDrawable, inEffect, inEdges, doMerge):
	# Disable Undo
	pdb.gimp_image_undo_group_start(img)
	
	pdb.plug_in_gauss_iir2(img, inDrawable, inEffect, inEffect)
	theNewlayer = inDrawable.copy()
	img.add_layer(theNewlayer, -1)
	#pdb.plug_in_laplace(1, img, theNewlayer)
	pdb.plug_in_edge(img, theNewlayer, inEdges, 1, 5)  # SMEAR & GRADIENT
	pdb.gimp_layer_set_mode(theNewlayer, SUBTRACT_MODE)
	if doMerge:
		pdb.gimp_image_merge_down(img, theNewlayer, EXPAND_AS_NECESSARY)
	
	# Enable Undo
	pdb.gimp_image_undo_group_end(img)


register(
	"python_fu_water_paint",
	"Draw with water paint effect",
	"Draw with water paint effect",
	"Werner Hartnagel, Iccii",
	"(c) 2005, Werner Hartnagel, Iccii",
	"2005-09-13",
	"<Image>/Python-Fu/Effects/Water-Paint-Effect...",
	"RGB*, GRAY*",
	[
		(PF_ADJUSTMENT, 'inEffect', 'Effect Size ',	5, (1,32,1)),
		(PF_ADJUSTMENT, 'inEdges', 'Edges ',	2, (1,6,1)),
		(PF_TOGGLE, 'merge_layers', 'Merge Layers', 1)
	],
	[],
	python_fu_water_paint_effect)

main()

