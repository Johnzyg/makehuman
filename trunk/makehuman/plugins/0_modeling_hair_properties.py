#!/usr/bin/python
# -*- coding: utf-8 -*-
# We need this for gui controls

import gui3d, hair, font3d
from aljabr import vdist, vmul, vnorm, vsub, vadd

print 'hair properties imported'

# r, g, b between 0 and 255
def rgbToHsl(r, g, b):
    
    r /= 255.0
    g /= 255.0
    b /= 255.0
    
    M = max([r, g, b])
    m = min([r, g, b])
    
    c = M - m
    
    if M == m:
        h = 0
    elif M == r:
        h = (60 * ((g - b) / c) + 360) % 360
    elif M == g:
        h = 60 * ((b - r) / c) + 120
    else:
        h = 60 * ((r - g) / c) + 240
    
    l = (M + m) / 2.0
    
    if M == m:
        s = 0
    elif l <= 0.5:
        s = c / (2.0 * l)
    else:
        s = c / (2.0 - 2.0 * l)
    
    return map(round, [h, s * 100, l * 100])
    
# h between 0 and 359, s and l between 0 and 100
def hslToRgb(h, s, l):
    
    h /= 60.0
    s /= 100.0
    l /= 100.0
    
    c = (1.0 - abs(2.0 * l - 1.0)) * s
    
    x = c * (1.0 - abs(h % 2.0 - 1.0))
    
    if h < 1.0:
        rgb = [c, x, 0.0]
    elif h < 2.0:
        rgb = [x, c, 0.0]
    elif h < 3.0:
        rgb = [0.0, c, x]
    elif h < 4.0:
        rgb = [0.0, x, c]
    elif h < 5.0:
        rgb = [x, 0.0, c]
    else:
        rgb = [c, 0.0, x]
        
    m = l - c * 0.5
    
    return [int((c + m)*255) for c in rgb]

class Action:

    def __init__(self, human, before, after, postAction=None):
        self.name = 'Change hair color'
        self.human = human
        self.before = before
        self.after = after
        self.postAction = postAction

    def do(self):
        self.human.hairColor = self.after
        if self.postAction:
            self.postAction()
        return True

    def undo(self):
        self.human.hairColor = self.before
        if self.postAction:
            self.postAction()
        return True


class HairPropertiesTaskView(gui3d.TaskView):

    def __init__(self, category):        
        
        gui3d.TaskView.__init__(self, category, 'Hair')
        
        y = 80
        gui3d.GroupBox(self, [10, y, 9.0], 'Hair properties', gui3d.GroupBoxStyle._replace(height=25+36*7+38+6));y+=25

        #############
        #SLIDERS
        #############
        
        self.widthSlider = gui3d.Slider(self, [10, y, 9.3], 1.0, 0.3, 30.0, "Hair width: %.2f");y+=36
        
        self.redSlider = gui3d.Slider(self, [10, y, 9.01], 0, 0, 255, 'Red: 0',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36

        self.greenSlider = gui3d.Slider(self, [10, y, 9.02], 0, 0, 255, 'Green: 0',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36

        self.blueSlider = gui3d.Slider(self, [10, y, 9.03], 0, 0, 255, 'Blue: 0',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36
        
        self.hueSlider = gui3d.Slider(self, [10, y, 9.04], 0, 0, 359, 'Hue: %d');y+=36
        self.saturationSlider = gui3d.Slider(self, [10, y, 9.05], 0, 0, 100, 'Saturation: %d',
            gui3d.SliderStyle._replace(normal='color_slider_background.png'),
            gui3d.SliderThumbStyle._replace(normal='color_slider.png', focused='color_slider_focused.png'));y+=36
        self.lightnessSlider = gui3d.Slider(self, [10, y, 9.06], 0, 0, 100, 'Lightness: %d');y+=36

        mesh = gui3d.NineSliceMesh(112, 32, self.app.getThemeResource('images', 'color_preview.png'), [4,4,4,4])
        self.colorPreview = gui3d.Object(self, [18, y+2, 9.07], mesh)
                    
        @self.redSlider.event
        def onChanging(value):
            self.setColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])
            
        @self.redSlider.event
        def onChange(value):
            self.changeColor([value, self.greenSlider.getValue(), self.blueSlider.getValue()])

        @self.greenSlider.event
        def onChanging(value):
            self.setColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
            
        @self.greenSlider.event
        def onChange(value):
            self.changeColor([self.redSlider.getValue(), value, self.blueSlider.getValue()])
            
        @self.blueSlider.event
        def onChanging(value):
            self.setColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])

        @self.blueSlider.event
        def onChange(value):
            self.changeColor([self.redSlider.getValue(), self.greenSlider.getValue(), value])
            
        @self.hueSlider.event
        def onChanging(value):
            self.setColor(hslToRgb(value, self.saturationSlider.getValue(), self.lightnessSlider.getValue()), False)

        @self.hueSlider.event
        def onChange(value):
            self.changeColor(hslToRgb(value, self.saturationSlider.getValue(), self.lightnessSlider.getValue()), False)
            
        @self.saturationSlider.event
        def onChanging(value):
            self.setColor(hslToRgb(self.hueSlider.getValue(), value, self.lightnessSlider.getValue()), False)

        @self.saturationSlider.event
        def onChange(value):
            self.changeColor(hslToRgb(self.hueSlider.getValue(), value, self.lightnessSlider.getValue()), False)
            
        @self.lightnessSlider.event
        def onChanging(value):
            self.setColor(hslToRgb(self.hueSlider.getValue(), self.saturationSlider.getValue(), value), False)

        @self.lightnessSlider.event
        def onChange(value):
            self.changeColor(hslToRgb(self.hueSlider.getValue(), self.saturationSlider.getValue(), value), False)
            
        @self.widthSlider.event
        def onChanging(value):
            human = self.app.selectedHuman
            if human.hairObj and len(human.hairObj.verts) > 0: 
               hairWidthUpdate(human.scene, human.hairObj, widthFactor=self.widthSlider.getValue())
            #pass #Do something!

    def changeColor(self, color, syncHsl=True):
        
        human = self.app.selectedHuman
        action = Action(self.app.selectedHuman, human.hairColor, [c/255.0 for c in color], self.syncSliders)
        self.app.do(action)
        if human.hairObj:
            human.hairObj.facesGroups[0].setColor(color, syncHsl)

    def setColor(self, color, syncHsl=True):
        
        red, green, blue = color
        
        for g in self.colorPreview.mesh.facesGroups:
            g.setColor([red, green, blue, 255])
            
        f = self.redSlider.background.mesh.faces[0]
        f.color = [
            [0, green, blue, 255],
            [255, green, blue, 255],
            [255, green, blue, 255],
            [0, green, blue, 255]
        ]
        f.updateColors()
        
        f = self.greenSlider.background.mesh.faces[0]
        f.color = [
            [red, 0, blue, 255],
            [red, 255, blue, 255],
            [red, 255, blue, 255],
            [red, 0, blue, 255]
        ]
        f.updateColors()
        
        f = self.blueSlider.background.mesh.faces[0]
        f.color = [
            [red, green, 0, 255],
            [red, green, 255, 255],
            [red, green, 255, 255],
            [red, green, 0, 255]
        ]
        f.updateColors()
        
        h, s, l = rgbToHsl(red, green, blue)
        
        f = self.saturationSlider.background.mesh.faces[0]
        s0 = hslToRgb(h, 0, l)
        s1 = hslToRgb(h, 100, l)
        f.color = [
            s0 + [255],
            s1 + [255],
            s1 + [255],
            s0 + [255]
        ]
        f.updateColors()
        
        if syncHsl:
            self.hueSlider.setValue(h)
            self.saturationSlider.setValue(s)
            self.lightnessSlider.setValue(l)
        else:
            self.redSlider.setValue(red)
            self.greenSlider.setValue(green)
            self.blueSlider.setValue(blue)

    def onShow(self, event):
        gui3d.TaskView.onShow(self, event)
        self.widthSlider.setFocus()
        self.syncSliders()

    def syncSliders(self):
        color = [int(c*255) for c in self.app.selectedHuman.hairColor]
        self.redSlider.setValue(color[0])
        self.greenSlider.setValue(color[1])
        self.blueSlider.setValue(color[2])
        self.setColor(color)

category = None
taskview = None

def load(app):
    taskview = HairPropertiesTaskView(app.categories['Modelling'])
    print 'hair properties loaded'

def unload(app):
    print 'hair properties unloaded'

#obj = hair object
def hairWidthUpdate(scn, obj,res=0.04, widthFactor=1.0): #luckily both normal and vertex index of object remains the same!
  N=len(obj.verts)
  origWidth = vdist(obj.verts[1].co,obj.verts[0].co)/res
  diff= (widthFactor-origWidth)*res/2
  for i in xrange(0,N/2):
      vec=vmul(vnorm(vsub(obj.verts[i*2+1].co,obj.verts[i*2].co)), diff) 
      obj.verts[i*2].co=vsub(obj.verts[i*2].co,vec)
      obj.verts[i*2+1].co=vadd(obj.verts[i*2+1].co,vec)
      obj.verts[i*2].update(updateNor=0)
      obj.verts[i*2+1].update(updateNor=0)
