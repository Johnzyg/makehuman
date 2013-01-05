#!/usr/bin/python
# -*- coding: utf-8 -*-

"""
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Manuel Bastioni, Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import mh
import gui
import gui3d
import humanmodifier

class GroupBoxRadioButton(gui.RadioButton):
    def __init__(self, task, group, label, groupBox, selected=False):
        super(GroupBoxRadioButton, self).__init__(group, label, selected)
        self.groupBox = groupBox
        self.task = task

    def onClicked(self, event):
        self.task.groupBox.showWidget(self.groupBox)

class FaceSlider(humanmodifier.ModifierSlider):
    def __init__(self, modifier, image, view):

        super(FaceSlider, self).__init__(min=-1.0, max=1.0, modifier=modifier, image=image)

        self.view = getattr(gui3d.app, view)

    def onFocus(self, event):
        super(FaceSlider, self).onFocus(event)
        if gui3d.app.settings.get('cameraAutoZoom', True):
            self.view()
        
class FaceSlider2(humanmodifier.ModifierSlider):
    def __init__(self, modifier, image, view):

        super(FaceSlider2, self).__init__(min=0.0, max=1.0, modifier=modifier, image=image)

        self.view = getattr(gui3d.app, view)

    def onFocus(self, event):
        super(FaceSlider2, self).onFocus(event)
        if gui3d.app.settings.get('cameraAutoZoom', True):
            self.view()

class FaceTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Face')

        features = [
            ('head', [('data/targets/head/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/head/images/', i[3]) for i in
                [   
                    ('head-age', 'less', 'more', 'frontView'),
                    ('head-angle', 'in', 'out', 'rightView'), 
                    ('head-scale-depth', 'less', 'more', 'rightView'),
                    ('head-scale-horiz', 'less', 'more', 'frontView'),
                    ('head-scale-vert', 'more', 'less', 'frontView'),
                    ('head-trans', 'in', 'out', 'frontView'),
                    ('head-trans', 'down', 'up', 'frontView'),
                    ('head-trans', 'forward', 'backward', 'rightView'),
                          
                                                      
                ]]), 
            ('neck', [('data/targets/neck/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/neck/images/', i[3]) for i in
                [  
                    ('neck-scale-depth', 'less', 'more', 'rightView'),
                    ('neck-scale-horiz', 'less', 'more', 'frontView'),
                    ('neck-scale-vert', 'more', 'less', 'frontView'),
                    ('neck-trans', 'in', 'out', 'frontView'),
                    ('neck-trans', 'down', 'up', 'frontView'),
                    ('neck-trans', 'forward', 'backward', 'rightView'),
                          
                                                      
                ]]),
            ('right eye', [('data/targets/eyes/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/eyes/images/', i[3]) for i in
                [
                    ('r-eye-height1', 'min', 'max', 'frontView'),
                    ('r-eye-height2', 'min', 'max', 'frontView'),
                    ('r-eye-height3', 'min', 'max', 'frontView'),
                    ('r-eye-push1', 'in', 'out', 'frontView'),
                    ('r-eye-push2', 'in', 'out', 'frontView'),
                    ('r-eye-move', 'in', 'out', 'frontView'),
                    ('r-eye-move', 'up', 'down', 'frontView'),
                    ('r-eye', 'small', 'big', 'frontView'),
                    ('r-eye-corner1', 'up', 'down', 'frontView'),
                    ('r-eye-corner2', 'up', 'down', 'frontView')
                ]]),
            ('left eye', [('data/targets/eyes/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/eyes/images/', i[3]) for i in
                [
                    ('l-eye-height1', 'min', 'max', 'frontView'),
                    ('l-eye-height2', 'min', 'max', 'frontView'),
                    ('l-eye-height3', 'min', 'max', 'frontView'),
                    ('l-eye-push1', 'in', 'out', 'frontView'),
                    ('l-eye-push2', 'in', 'out', 'frontView'),
                    ('l-eye-move', 'in', 'out', 'frontView'),
                    ('l-eye-move', 'up', 'down', 'frontView'),
                    ('l-eye', 'small', 'big', 'frontView'),
                    ('l-eye-corner1', 'up', 'down', 'frontView'),
                    ('l-eye-corner2', 'up', 'down', 'frontView'),
                ]]),
            ('nose features', [('data/targets/nose/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/nose/images/', i[3]) for i in
                [
                    ('nose', 'compress', 'uncompress', 'rightView'),
                    ('nose', 'convex', 'concave', 'rightView'),
                    ('nose', 'moregreek', 'lessgreek', 'rightView'),                    
                    ('nose', 'morehump', 'lesshump', 'rightView'),
                    ('nose', 'potato', 'point', 'rightView'),                    
                    ('nose-nostrils', 'point', 'unpoint', 'frontView'),
                    ('nose-nostrils', 'up', 'down', 'rightView'),
                    ('nose-point', 'up', 'down', 'rightView'),
                ]]),
            ('nose size details', [('data/targets/nose/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/nose/images/', i[3]) for i in
                [
                    ('nose-nostril-width', 'min', 'max', 'frontView'), 
                    ('nose-height', 'min', 'max', 'rightView'),                   
                    ('nose-width1', 'min', 'max', 'frontView'),
                    ('nose-width2', 'min', 'max', 'frontView'),
                    ('nose-width3', 'min', 'max', 'frontView'),
                    ('nose-width', 'min', 'max', 'frontView'),
                                        
                ]]),
            ('nose size and pos', [('data/targets/nose/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/nose/images/', i[3]) for i in
                [
                    ('nose-trans', 'up', 'down', 'frontView'),
                    ('nose-trans', 'forward', 'backward', 'rightView'),
                    ('nose-trans', 'in', 'out', 'frontView'),
                    ('nose-scale-vert', 'incr', 'decr', 'frontView'),
                    ('nose-scale-horiz', 'incr', 'decr', 'frontView'),
                    ('nose-scale-depth', 'incr', 'decr', 'rightView'),
                ]]),
            ('mouth size and pos', [('data/targets/mouth/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/mouth/images/', i[3]) for i in
                [
                    ('mouth-scale-horiz', 'incr', 'decr', 'frontView'),
                    ('mouth-scale-vert', 'incr', 'decr', 'frontView'),
                    ('mouth-scale-depth', 'incr', 'decr', 'rightView'),
                    ('mouth-trans', 'in', 'out', 'frontView'),
                    ('mouth-trans', 'up', 'down', 'frontView'),
                    ('mouth-trans', 'forward', 'backward', 'rightView'),
                ]]),
            ('mouth size details', [('data/targets/mouth/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/mouth/images/', i[3]) for i in
                [
                    ('mouth-lowerlip-height', 'min', 'max', 'frontView'),
                    ('mouth-lowerlip-middle', 'up', 'down', 'frontView'),
                    ('mouth-lowerlip-width', 'min', 'max', 'frontView'),            
                    ('mouth-upperlip-height', 'min', 'max', 'frontView'),              
                    ('mouth-upperlip-width', 'min', 'max', 'frontView'),        
                ]]),
            ('mouth features', [('data/targets/mouth/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/mouth/images/', i[3]) for i in
                [
                    ('mouth-lowerlip-ext', 'up', 'down', 'frontView'),
                    ('mouth-angles', 'up', 'down', 'frontView'),                    
                    ('mouth-lowerlip-middle', 'up', 'down', 'frontView'),                    
                    ('mouth-lowerlip', 'deflate', 'inflate', 'rightView'),
                    ('mouth-philtrum', 'up', 'down', 'frontView'),
                    ('mouth-philtrum', 'increase', 'decrease', 'rightView'),                    
                    ('mouth-upperlip', 'deflate', 'inflate', 'rightView'),
                    ('mouth-upperlip-ext', 'up', 'down', 'frontView'),                    
                    ('mouth-upperlip-middle', 'up', 'down', 'frontView'),                    
                ]]),
            ('right ear', [('data/targets/ears/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/ears/images/', i[3]) for i in
                [                   
                    ('r-ear', 'backward', 'forward', 'rightView'),
                    ('r-ear', 'big', 'small', 'rightView'),
                    ('r-ear', 'down', 'up', 'rightView'),
                    ('r-ear-height', 'min', 'max', 'rightView'),
                    ('r-ear-lobe', 'min', 'max', 'rightView'),
                    ('r-ear', 'pointed', 'triangle', 'rightView'),
                    ('r-ear-rot', 'backward', 'forward', 'rightView'),
                    ('r-ear', 'square', 'round', 'rightView'),
                    ('r-ear-width', 'max', 'min', 'rightView'),
                    ('r-ear-wing', 'out', 'in', 'frontView'),
                    ('r-ear-flap', 'out', 'in', 'frontView'),
                ]]),
            ('left ear', [('data/targets/ears/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/ears/images/', i[3]) for i in
                [
                    ('l-ear', 'backward', 'forward', 'leftView'),
                    ('l-ear', 'big', 'small', 'leftView'),
                    ('l-ear', 'down', 'up', 'leftView'),
                    ('l-ear-height', 'min', 'max', 'leftView'),
                    ('l-ear-lobe', 'min', 'max', 'leftView'),
                    ('l-ear', 'pointed', 'triangle', 'leftView'),
                    ('l-ear-rot', 'backward', 'forward', 'leftView'),
                    ('l-ear', 'square', 'round', 'leftView'),
                    ('l-ear-width', 'max', 'min', 'leftView'),
                    ('l-ear-wing', 'out', 'in', 'frontView'),
                    ('l-ear-flap', 'out', 'in', 'frontView'),       
                ]]),
            ('chin', [('data/targets/chin/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), i[0], i[1], i[2], 'data/targets/chin/images/', i[3]) for i in
                [
                    ('chin', 'in', 'out', 'rightView'),
                    ('chin-width', 'min', 'max', 'frontView'),
                    ('chin-height', 'min', 'max', 'frontView'),
                    ('chin', 'squared', 'round', 'frontView'),
                    ('chin', 'prognathism1', 'prognathism2', 'rightView'),

                ]]),
            ('cheek', [
                (
                    'data/targets/cheek/${ethnic}/${gender}_${age}/%s-${value}.target' % (i[0]), 
                    i[0], i[1], i[2], 'data/targets/cheek/images/', i[3]
                ) for i in [
                      ('l-cheek', 'in', 'out', 'frontView'),
                      ('l-cheek-bones', 'out', 'in', 'frontView'),
                      ('r-cheek', 'in', 'out', 'frontView'),
                      ('r-cheek-bones', 'out', 'in', 'frontView'),
                      ]
                    ]
                    )
            ]
            
        features2 = [
            ('head shape', [('data/targets/head/${ethnic}/${gender}_${age}/%s.target' % (i[0]), i[0], 'data/targets/head/images/', i[1]) for i in
                [   
                    ('head-oval', 'frontView'),    
                    ('head-round', 'frontView'), 
                    ('head-rectangular', 'frontView'), 
                    ('head-square', 'frontView'), 
                    ('head-triangular', 'frontView'), 
                    ('head-invertedtriangular', 'frontView'), 
                    ('head-diamond', 'frontView'), 
                    
                       
                          
                                                      
                ]])            
            ]

        self.groupBoxes = []
        self.radioButtons = []
        self.sliders = []

        self.modifiers = {}

        self.categoryBox = self.addRightWidget(gui.GroupBox('Category'))
        self.groupBox = self.addLeftWidget(gui.StackedBox())
        
        for name, templates in features2:

            for index, template in enumerate(templates):

                if index % 12 == 0:

                    if len(templates) <= 12:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 12 + 1)

                    # Create box
                    box = self.groupBox.addWidget(gui.GroupBox(title))
                    self.groupBoxes.append(box)

                    # Create radiobutton
                    radio = self.categoryBox.addWidget(GroupBoxRadioButton(self, self.radioButtons, title, box, selected=len(self.radioButtons) == 0))

                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicModifier2(template[0])
                modifierName = template[1]
                clashIndex = 0
                while modifierName in self.modifiers:
                    modifierName = '%s%d' % (template[1], clashIndex)
                    clashIndex+=1

                #self.modifiers['%s%d' % (name, index + 1)] = modifier
                self.modifiers[modifierName] = modifier

                slider = box.addWidget( (FaceSlider2(modifier, '%s%s.png' % (template[2], template[1]), template[3])))
                 
                self.sliders.append(slider)

        for name, templates in features:            

            for index, template in enumerate(templates):

                if index % 12 == 0:

                    if len(templates) <= 12:
                        title = name.capitalize()
                    else:
                        title = '%s %d' % (name.capitalize(), index / 12 + 1)

                    # Create box
                    box = self.groupBox.addWidget(gui.SliderBox(title))
                    self.groupBoxes.append(box)

                    # Create radiobutton
                    radio = self.categoryBox.addWidget(GroupBoxRadioButton(self, self.radioButtons, title, box, selected=len(self.radioButtons) == 0))

                # Create sliders
                modifier = humanmodifier.GenderAgeEthnicAsymmetricModifier(template[0], 'value', template[2], template[3], False)
                modifierName = template[1]
                clashIndex = 0
                while modifierName in self.modifiers:
                    modifierName = '%s%d' % (template[1], clashIndex)
                    clashIndex+=1
                self.modifiers[modifierName] = modifier

                slider = box.addWidget(FaceSlider(modifier, '%s%s-%s-%s.png' % (template[4], template[1], template[2], template[3]), template[5]))
                self.sliders.append(slider)

        self.groupBox.showWidget(self.groupBoxes[0])

    def getModifiers(self):
        return self.modifiers;

    # return list of pairs of modifier names for symmetric body parts
    def getSymmetricModifierPairNames(self):
        pairs = []
        for modifierName in self.modifiers:
            if modifierName.startswith("r-"):
                baseModifierName = modifierName[2:]
                oppModifierName = "l-"+baseModifierName
                pair = { 'left': modifierName,
                        'right': oppModifierName }
                pairs.append(pair)

        return pairs;

    # return list of singular modifier names
    def getSingularModifierNames(self):
        modifiers = [] 
        for modifierName in self.modifiers:
            if not modifierName.startswith("r-") and not modifierName.startswith("l-"):
                modifiers.append(modifierName)

        return modifiers;

    def onShow(self, event):

        gui3d.TaskView.onShow(self, event)

        if gui3d.app.settings.get('cameraAutoZoom', True):
            gui3d.app.setFaceCamera()

        for slider in self.sliders:
            slider.update()

    def onHumanChanged(self, event):

        human = event.human

        for slider in self.sliders:
            slider.update()

    def loadHandler(self, human, values):

        if values[0] == 'face':
            modifier = self.modifiers.get(values[1].replace("-", " "), None)
            if modifier:
                modifier.setValue(human, float(values[2]))

    def saveHandler(self, human, file):

        for name, modifier in self.modifiers.iteritems():
            value = modifier.getValue(human)
            if value:
                file.write('face %s %f\n' % (name.replace(" ", "-"), value))

def load(app):
    category = app.getCategory('Modelling')
    taskview = category.addTask(FaceTaskView(category))

    app.addLoadHandler('face', taskview.loadHandler)
    app.addSaveHandler(taskview.saveHandler)

def unload(app):
    pass


