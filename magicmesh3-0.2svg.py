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

# http://www.phobeus.de/hosting/pixelpracht/downloads/hexcoordsTut_e.htm


from gimpfu import *
import math

class SVGMesh:
	def __init__(self, filename, width, height, space):
		self.filename = filename
		self.markup = ""
		self.width = width
		self.height = height
		self.space = space
		self.row = 0

	def addCircle(self, cx, cy, diameter, fill, opacity, stroke, stroke_width):
		r = diameter/2
		self.markup = self.markup + "<circle cx=\"%s\" cy=\"%s\" r=\"%s\" style=\"stroke:%s;stroke-width:%spx;fill:%s;" % (cx, cy, r, stroke, stroke_width, fill)
		if opacity != 1:
			self.markup = self.markup + "fill-opacity:%.2f;" % opacity
		self.markup = self.markup + '"/>\n'

	def addRect(self, cx, cy, r, fill, opacity, stroke, stroke_width):
		self.markup = self.markup + "<rect x=\"%s\" y=\"%s\" width=\"%s\" height=\"%s\" style=\"stroke:%s;stroke-width:%spx;fill:%s;" % (cx,cy,r,r,stroke,stroke_width,fill)
		if opacity != 1:
			self.markup = self.markup + "fill-opacity:%.2f;" % opacity
		self.markup = self.markup + '"/>\n'

	def addHexagon(self, cx, cy, d, fill, opacity, stroke, stroke_width):
		r = d / 2
		s = r / math.cos(math.radians(30))
		h = math.sin(math.radians(30)) * s
		b = s + (2 * h)
		a = 2 * r
		shape = []
		shape.append({'x': cx+r,	'y': cy })
		shape.append({'x': cx+r+r,	'y': cy+h })
		shape.append({'x': cx+r+r,	'y': cy+h+s })
		shape.append({'x': cx+r,	'y': cy+b })
		shape.append({'x': cx,		'y': cy+h+s })
		shape.append({'x': cx,		'y': cy+h })
		self.markup = self.markup + '<polygon style="stroke:%s;stroke-width:%spx;fill:%s;' % (stroke,stroke_width,fill)
		if opacity != 1:
			self.markup = self.markup + "fill-opacity:%.2f;" % opacity
		self.markup = self.markup + '" points="'
		for pos in shape:
			if self.row % 2 == 0:
				px = pos['x'] + r + (self.space / 2)
				py = pos['y']
			else:
				px = pos['x']
				py = pos['y']

		#	self.markup = self.markup + str(int(round(px))) + ',' + str(int(round(py))) + ' '
			self.markup = self.markup + "%.0f,%.0f " % (px,py)

		self.markup = self.markup + '"/>\n'

	def __del__(self):
		self.markup = '<?xml version="1.0" standalone="no"?>\n<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" \n"http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">\n\n<svg width="'+str(self.width)+'" height="'+str(self.height)+'" version="1.1" xmlns="http://www.w3.org/2000/svg">\n\n' + self.markup + '\n</svg>'
		f = open(self.filename, "w")
		f.write(self.markup)
		f.close()

def pyMagicmeshSVG(img, layer, svg_filename, shape, diameter, sspace, sborder, opacity, transparent_bg):

	# Vars
	diameter = int(diameter)
	sspace = int(sspace)
	sborder = int(sborder)
	sradius = diameter / 2
	max_w = img.width # - (img.width % (diameter+sspace))+sspace
	max_h = img.height # - (img.height % (diameter+sspace))+sspace
	if shape == "hexagon":
		s = sradius / math.cos(math.radians(30))
		h = math.sin(math.radians(30)) * s
		b = s + (2 * h)
		diameter_w = diameter
		diameter_h = b
		offsetY = h
	else:
		diameter_w = diameter
		diameter_h = diameter
		offsetY = 0

#	max_svg_w = (diameter + 2*sspace) * int(max_x(b + sspace))
#	max_svg_h = (b + sspace) * int(max_x(b + sspace))
	mySVG = SVGMesh(svg_filename, max_w, max_h, sspace)

	for pos_y in xrange(int(sspace+(diameter_h/2)), int(max_h-(diameter_h/2)), int(diameter_h+sspace-offsetY)):
		mySVG.row = mySVG.row + 1
		for pos_x in xrange(sspace+sradius, max_w-sradius, diameter_w+sspace):
			av_color = pdb.gimp_image_pick_color(img, layer, pos_x, pos_y, 1, 1, diameter)
			fillcolor = "rgb(%i,%i,%i)" % (av_color.r*255, av_color.g*255, av_color.b*255)
			if opacity:
				gray_color = 0.3*av_color[0] + 0.59*av_color[1] + 0.11*av_color[2]
				opacity_value = round(gray_color / 255, 2)
			else:
				opacity_value = 1

			if shape == "dots":
				mySVG.addCircle(pos_x, pos_y, diameter, fillcolor, opacity_value, "black", sborder)
			elif shape == "rect":
				mySVG.addRect(pos_x-sradius, pos_y-sradius, diameter, fillcolor, opacity_value, "black", sborder)
			elif shape == "hexagon":
				mySVG.addHexagon(pos_x-sradius, pos_y-sradius, diameter, fillcolor, opacity_value, "black", sborder)

	del mySVG
	svgdata = pdb.gimp_file_load(svg_filename, svg_filename)
	if not transparent_bg:
		svgdata.flatten()
	disp1 = gimp.Display(svgdata)


register(
	"python_fu_magicmesh3_svg",
	"dotsvg",
	"dotsvg",
	"Werner Hartnagel",
	"Werner Hartnagel",
	"2006",
	"<Image>/Python-Fu/Create Layers/Magicmesh3 (SVG)",
	"RGB*, GRAY*",
	[
		(PF_STRING, "svg_filename", "Filename to export", "/tmp/dotsvg.svg"),
		(PF_RADIO, "Shape", "The format of the images", "dots", (("dots", "dots"), ("rect", "rect"), ("hexagon", "hexagon"))),
		(PF_SPINNER, "Diameter", "The Diameter", 20, (3, 150, 1)),
		(PF_SPINNER, "space", "The Space", 5, (0, 50, 1)),
		(PF_SPINNER, "border", "Border around the dots", 0, (0, 10, 1)),
		(PF_TOGGLE, 'opacity', 'Oppacity dots', 0),
		(PF_TOGGLE, 'transparent_bg', 'Transparent Background', 0)
	],
	[],
	pyMagicmeshSVG)

main()
