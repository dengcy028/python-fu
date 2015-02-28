#!/usr/bin/env python

#   Written by Werner Hartnagel
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

def aquabutt2(string, font, size, antialias, colorfn1, colorfn2, colorfg1, colorfg2, colorbg, optical_top):
	oldfg = gimp.get_foreground()
	oldbg = gimp.get_background()

	image1 = gimp.Image(255,255, RGB)
	image1.disable_undo()
	makebutton(image1, string, font, size, antialias, colorfn1, colorfg1, colorbg, optical_top)
	image1.enable_undo()
	disp1 = gimp.Display(image1)


	image2 = gimp.Image(255,255, RGB)
	image2.disable_undo()
	makebutton(image2, string, font, size, antialias, colorfn2, colorfg2, colorbg, optical_top)
	image2.enable_undo()
	disp2 = gimp.Display(image2)

	gimp.set_foreground(oldfg)
	gimp.set_background(oldbg)

def makebutton (image, string, font, size, antialias, colorfn, colorfg, colorbg, optical_top):
	radius = 4

	gimp.set_foreground(colorfn)
	textlayer = pdb.gimp_text_fontname(image, None, radius*2, radius*2, string, -1, antialias, size, PIXELS, font)
	width = (textlayer.width+radius*4)*1.5
	height = (textlayer.height+radius*4)*1.7

	x = width*0.07
	y = height*0.2
	d = height-y*2.5
	pdb.gimp_image_resize(image, width, height, 0, 0)

	# Set new selections for the fore and background-color.
	gimp.set_foreground(colorfg)
	gimp.set_background((0xff,0xff,0xff))
	background = gimp.Layer(image, "Background", width, height, RGBA_IMAGE, 100, NORMAL_MODE)
	base = gimp.Layer(image, "Base", width, height, RGBA_IMAGE, 90, NORMAL_MODE)
	shadow = gimp.Layer(image, "Shadow", width, height, RGBA_IMAGE, 70, NORMAL_MODE)
	reflection = gimp.Layer(image, "Top Reflect", width, height, RGBA_IMAGE, optical_top, SCREEN_MODE)
	light = gimp.Layer(image, "light", width, height, RGBA_IMAGE, 100, OVERLAY_MODE)

	image.add_layer(reflection, 1)
	image.add_layer(light,   2)
	image.add_layer(base,  3)
	image.add_layer(shadow, 4)
	image.add_layer(background,  5)
	center_lay(image, textlayer)

	pdb.gimp_edit_clear(reflection)
	pdb.gimp_edit_clear(light)
	pdb.gimp_edit_clear(base)
	pdb.gimp_edit_clear(shadow)
	pdb.gimp_edit_clear(background)

	# fill the background
	gimp.set_foreground(colorbg)
	pdb.gimp_edit_fill(background, 0)  #0 == GIMP_FOREGROUND_FILL

	# make base of the button
	maskbase=pdb.gimp_layer_create_mask(base, 2)
	pdb.gimp_layer_add_mask(base, maskbase)
#	image.add_layer_mask(base, maskbase)
	pdb.gimp_edit_clear(maskbase)

	gimp.set_foreground((0xff,0xff,0xff))
	pdb.gimp_edit_fill(maskbase, 0)
	selzone(image, x, y, d)
	gimp.set_foreground(colorfg)
	pdb.gimp_edit_fill(base, 0)

	pdb.gimp_selection_shrink(image, 58)
	gimp.set_foreground((0xa0,0xa0,0xa0))
	pdb.gimp_edit_fill(maskbase, 0)
	pdb.gimp_selection_none(image)
	pdb.plug_in_gauss_rle2(image, maskbase, 74,74)
	pdb.gimp_drawable_set_visible(maskbase, 0)

	# Make shadow
	selzone(image, x, y, d)
	pdb.gimp_selection_translate(image, 0, d/4)
	gimp.set_foreground(colorfg)
	pdb.gimp_edit_fill(shadow, 0)
	pdb.gimp_selection_none(image)
	pdb.plug_in_gauss_rle2(image, shadow, d/4, d/4)
	gimp.set_foreground(colorfg)

	maskshadow=pdb.gimp_layer_create_mask(shadow, 2)
	pdb.gimp_layer_add_mask(shadow, maskshadow)
#	image.add_layer_mask(shadow, maskshadow)
	pdb.gimp_edit_clear(maskshadow)
	gimp.set_foreground((0x00,0x00,0x00))
	pdb.gimp_edit_fill(maskshadow, 0)
	selzone(image, x, y, d)
	pdb.gimp_selection_invert(image)
	pdb.gimp_edit_clear(maskshadow)
	pdb.gimp_drawable_set_visible(maskshadow, 0)

	#make light
	pdb.gimp_selection_none(image)
	gimp.set_foreground((0x00,0x00,0x00))
	pdb.gimp_edit_fill(light, 0)
	selzone(image, x, y, d)
	pdb.gimp_selection_shrink(image, d/5)
	pdb.gimp_selection_translate(image, 0, d/4)
	gimp.set_foreground((0xff,0xff,0xff))
	pdb.gimp_edit_fill(light, 0)
	pdb.gimp_selection_none(image)
	pdb.plug_in_gauss_rle2(image, light, d/4, d/4)


	#Top reflect
	pdb.gimp_rect_select(image, x+d/2, y+height*0.04, width-(x+d/2)*2, d/3.5, 2, 0, 0)
	rect_sel = pdb.gimp_selection_save(image)
	pdb.gimp_selection_none(image)
	pdb.plug_in_gauss_iir(image, rect_sel, d/4, 1, 1)
	pdb.gimp_levels(rect_sel, 0, 123, 133, 1.0, 0, 255)
	pdb.gimp_selection_load(rect_sel)
	pdb.gimp_image_remove_channel(image, rect_sel)
	gimp.set_foreground((0x00, 0x00, 0x00))
	pdb.gimp_edit_blend(reflection,1,0,0,100,0,0,0,0,0,0,0,width-x*2-d,y+d/2.5,width-x*2-d,y+d/15)
#	pdb.gimp_perspective(reflection,0,x+d/2,y+height*0.04, width-(x+d/2),y+height*0.04, x+d/4,y+d/3.5,width-(x+d/4),y+d/3.5 )
	pdb.gimp_drawable_transform_perspective_default(reflection,x+d/2,y+height*0.04, width-(x+d/2),y+height*0.04, x+d/4,y+d/3.5,width-(x+d/4),y+d/3.5, False, False)
	pdb.gimp_floating_sel_anchor(pdb.gimp_image_get_floating_sel(image))
	pdb.plug_in_gauss_rle2(image, reflection, d/20, d/20)

def selzone (img, x, y, d):
	pdb.gimp_ellipse_select(img, x, y, d, d, 2, 1, 0, 0)
	pdb.gimp_ellipse_select(img, img.width-x-d, y, d, d, 0, 1, 0, 0)
	pdb.gimp_rect_select(img, x+d/2, y, img.width-x*2-d, d, 0, 0, 0)

def center_lay(img, drw):
	off_w = (pdb.gimp_image_width(img) - pdb.gimp_drawable_width(drw)) / 2
	off_h = (pdb.gimp_image_height(img) - pdb.gimp_drawable_height(drw)) / 2
	pdb.gimp_layer_set_offsets(drw, off_w, off_h)


register(
	"python_fu_aquabutt2",
	"Make a Aqua Style Button V2",
	"Make a Aqua Style Button V2 (based on perl-fu from Denis Bodor)",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2003",
	"<Toolbox>/Xtns/Python-Fu/Web-Tools/Buttons/AquaButt2",
	"",
	[
		(PF_STRING, "String", "string", "The Gimp"),
		(PF_FONT, "Font", "Font", "Sans Bold"),
		(PF_SPINNER, "Font_Size", "Size", 14, (0, 1000, 1)),
		(PF_TOGGLE, "Antialias", "Antialias ", 0),
		(PF_COLOR, 'Font_Color1', 'Font color (Active) ', (0,0,0)),
		(PF_COLOR, 'Font_Color2', 'Font color ', (0,0,255)),
		(PF_COLOR, 'Button_Color1', 'Button color (Active) ', (0x53,0x93,0xd9)),
		(PF_COLOR, 'Button_Color2', 'Button color ', (0xd9,0xd9,0xd9)),
		(PF_COLOR, 'Background_Color',  'Background color ', (0xff,0xff,0xff)),
		(PF_SLIDER, 'Optical_Top', 'Top Reflection Optical ', 50, (0, 100, 1))
	],
	[],
	aquabutt2)

main()
