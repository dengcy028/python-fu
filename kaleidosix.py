#!/usr/bin/env python

#   Copyright (C) 2005  Werner Hartnagel <info@dotmagic.de>
#   based on Perl plugin from Magnus Enger
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
import sys, math

def python_fu_kaleidosix(old, drawable, width, height):
	
	# Find the area that has been selected in the original image
	old_is_sel, old_x1, old_y1, old_x2, old_y2 = pdb.gimp_selection_bounds(old)
	if  not old_is_sel:
		pdb.gimp_message("FATAL: Missing selection in old image!")
		#sys.exit(1)
	
	old_width = old_x2 - old_x1
	old_height = old_y2 - old_y1
	
	# Turn the initial selection into a rectangle with equal sides, pointing to the right
	xm = int(old_y1 + (old_height / 2))
	inner_width = int(math.sqrt((old_height**2)-((old_height/2)**2)))
	ym = int(old_x1 + inner_width)
	points = (old_x1, old_y1, ym, xm, old_x1, old_y2)
	
	pdb.gimp_free_select(old, 6, points, CHANNEL_OP_REPLACE, 0, 0, 0)
	
	# Copy the selected area
	pdb.gimp_selection_grow(old, 1)
	# gimp_selection_feather($old, 0);
	pdb.gimp_edit_copy(drawable)
	
	# Create a new image
	img = gimp.Image(width, height, RGB)
	# Disable Undo
#	img.undo_group_start()
	
	# Create a new layer and set the size of the layer = the size of the initial selection
	layer = gimp.Layer(img, "first", inner_width, old_y2-old_y1, 0, 100, 0)
	img.add_layer(layer, 0)
	layer.add_alpha()
	
	# Clear the layer of any initial garbage
	pdb.gimp_edit_clear(layer)
	
	# Add the copied selection to the layer, and the layer to the image
	layer.fill(3)
	pdb.gimp_edit_paste(layer, 1)
	pdb.gimp_floating_sel_anchor(pdb.gimp_image_get_floating_sel(img))
	move_down = (old_y2 - old_y1)/2
	layer.translate(0, move_down)
	
	# Create the mirrored layer
	mirror = gimp.Layer(img, "mirror", inner_width, old_y2-old_y1, 0, 100, 0)
	img.add_layer(mirror, 0)
	
	mirror.add_alpha()
	pdb.gimp_edit_clear(mirror)
	mirror.fill(3)
	pdb.gimp_edit_paste(mirror, 1)
	pdb.gimp_floating_sel_anchor(pdb.gimp_image_get_floating_sel(img))
	pdb.gimp_layer_translate(mirror, inner_width, move_down)
	
	#pdb.gimp_flip(mirror, 0)
	pdb.gimp_drawable_transform_flip_simple(mirror, ORIENTATION_HORIZONTAL, 1, 0, 0)
	
	# Make copies of the fist pair and rotate them
	
	# Merge the two layers
	combo = img.merge_visible_layers(1);
	
	# Make a copy for rotating
	copy1 = combo.copy(0)
	img.add_layer(copy1, 0)
	#pdb.gimp_rotate(copy1, 0, 2.094)
	pdb.gimp_drawable_transform_rotate_default(copy1, 2.094, 0, inner_width, old_y2-old_y1, 1, 0)
	pdb.gimp_selection_none(img)
	
	# Make a second copy for the second rotation
	copy2 = combo.copy(0)
	img.add_layer(copy2, 0)
	
	#pdb.gimp_rotate(copy2, 0, -2.094)
	pdb.gimp_drawable_transform_rotate_default(copy2, -2.094, 0, inner_width, old_y2-old_y1, 1, 0)
	pdb.gimp_selection_none(img)
	
	# Fill the available space with cells!
	
	# Turn all the "temporary" layers into one
	#cell = pdb.gimp_image_merge_visible_layers(img, 1)
	cell = img.merge_visible_layers(1)
	
	# Position the cells
	rows = int(width / old_height)+1
	cols = int(height / old_height)+1
	for i in range(0, rows):
		for j in range(0, cols):
			this_layer = cell.copy(0)
			img.add_layer(this_layer, 0)
			#my $offx;
			if i % 2 == 0:
				offx = 2*j -1
			else:
				offx = 2*j
			
			offy = 1.5*i -1
			# This feels like a bit of a hack, but it seems to work:
			pdb.gimp_layer_set_offsets(this_layer, (offx*inner_width)-offx, (offy*old_height)-(offy+6*i))

	
	#pdb.gimp_image_merge_visible_layers(img, 1)
	img.merge_visible_layers(1)
	disp1 = gimp.Display(img)

	# Enable Undo
#	img.undo_group_end()
	
# Register with The Gimp
register(
	"python_fu_kaleidosix",
	"Turn selection into tiled kaleidoscopic image",
	"Turn selection into tiled kaleidoscopic image",
	"Werner Hartnagel, Magnus Enger",
	"(c) 2005, Werner Hartnagel",
	"2005-08-25",
	"<Image>/Python-Fu/Patterns/Kaleidosix...",
	"*",
	[
		(PF_INT32, "width", "Width", 500),
		(PF_INT32, "height", "Height", 500),
	],
	[],
	python_fu_kaleidosix);

main()
