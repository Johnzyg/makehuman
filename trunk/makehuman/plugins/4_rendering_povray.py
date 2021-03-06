#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 
**Project Name:**      MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**    http://code.google.com/p/makehuman/

**Authors:**           Marc Flerackers

**Copyright(c):**      MakeHuman Team 2001-2013

**Licensing:**         AGPL3 (see also http://www.makehuman.org/node/318)

**Coding Standards:**  See http://www.makehuman.org/node/165

Abstract
--------

TODO
"""

import sys
import os

# We need this for rendering
import mh2povray

# We need this for gui controls
import gui3d
import gui

class PovrayTaskView(gui3d.TaskView):

    def __init__(self, category):
        gui3d.TaskView.__init__(self, category, 'Povray')
        
        # for path to PovRay binaries file
        binary = ''

        bintype = []
        pathBox = self.addLeftWidget(gui.GroupBox('Povray  bin  path'))
        # this part load old settings values for next session; str(povray_bin)
        povray_bin = gui3d.app.settings.get('povray_bin', '')
        self.path= pathBox.addWidget(gui.TextEdit(str(povray_bin)), 0, 0, 1, 2)
        self.browse = pathBox.addWidget(gui.BrowseButton('dir'), 1, 0, 1, 1)
        self.browse.setPath(povray_bin)
        if sys.platform == 'win32':
            self.browse.setFilter('Executable programs (*.exe);;All files (*.*)')
        
        #
        if os.name == 'nt':
            #
            if os.environ['PROCESSOR_ARCHITECTURE'] == 'x86':
                self.win32sse2Button = pathBox.addWidget(gui.CheckBox('Use SSE2 bin', True))
        #
        @self.path.mhEvent
        def onChange(value):
            gui3d.app.settings['povray_bin'] = 'Enter your path' if not value else str(value)

        @self.browse.mhEvent
        def onClicked(path):
            if os.path.isdir(path):
                gui3d.app.settings['povray_bin'] = path
                self.path.setText(path)
        #------------------------------------------------------------------------------------
        filter = []
        # Options box
        optionsBox = self.addLeftWidget(gui.GroupBox('Options'))
        self.doSubdivide = optionsBox.addWidget(gui.CheckBox('Subdivide mesh', True))
        self.useSSS = optionsBox.addWidget(gui.CheckBox('Use S.S. Scattering', True))
        self.SSSA = optionsBox.addWidget(gui.Slider(value=0.3, label="SSS Amount"))
        self.AA = optionsBox.addWidget(gui.Slider(value=0.4, label="AntiAliasing"))

        materialsBox = self.addRightWidget(gui.GroupBox('Materials'))
        self.skinoil = materialsBox.addWidget(gui.Slider(value=0.4, label="Skin oil"))
        self.rough = materialsBox.addWidget(gui.Slider(value=0.5, label="Skin roughness"))
        self.wrinkles = materialsBox.addWidget(gui.Slider(value=0.2, label="Skin wrinkles"))
        self.hairSpec = materialsBox.addWidget(gui.CheckBox('Hair shine', False))
        self.hspecA = materialsBox.addWidget(gui.Slider(value=0.5, label="Shine strength"))
        self.hairThick = materialsBox.addWidget(gui.Slider(value=0.67, label="Hair thickness"))

        # box
        #optionsBox = self.addLeftWidget(gui.GroupBox('Options'))
        
        #Buttons
        # Simplified the gui a bit for the average user. Uncomment to clutter it up with developer - useful stuff.
        #source=[]
        #self.iniButton = optionsBox.addWidget(gui.RadioButton(source, 'Use ini settings'))
        #self.guiButton = optionsBox.addWidget(gui.RadioButton(source, 'Use gui settings', selected = True))
        #format=[]
        #self.arrayButton = optionsBox.addWidget(gui.RadioButton(format, 'Array  format'))
        #self.mesh2Button = optionsBox.addWidget(gui.RadioButton(format, 'Mesh2 format', selected = True))
        #action=[]
        #self.exportButton = optionsBox.addWidget(gui.RadioButton(action , 'Export only', selected = True))
        #self.exportandrenderButton = optionsBox.addWidget(gui.RadioButton(action , 'Export and render'))
        self.renderButton = optionsBox.addWidget(gui.Button('Render'))
        
        #        
        @self.renderButton.mhEvent
        def onClicked(event):            
            
            reload(mh2povray)  # Avoid having to close and reopen MH for every coding change (can be removed once testing is complete)
            # it is necessary to put this code here, so that it is executed with the 'renderButton.event'
            if os.name == 'nt':
                #
                if os.environ['PROCESSOR_ARCHITECTURE'] == "x86":
                    binary = 'win32'
                    #
                    if self.win32sse2Button.selected:
                        binary = 'win32sse2'
                #
                else:
                    binary = 'win64'
            # for Ubuntu.. atm
            if sys.platform == 'linux2':
                binary = 'linux'
            #
            mh2povray.povrayExport(gui3d.app.selectedHuman.mesh, gui3d.app,
                                   {'source':'gui',         # 'ini' if self.iniButton.selected else 'gui',
                                    'format':'mesh2',       # 'array' if self.arrayButton.selected else 'mesh2',
                                    'action':'render',      # 'export' if self.exportButton.selected else 'render',
                                    'subdivide':True if self.doSubdivide.selected else False,
                                    'AA': 0.5-0.49*self.AA.getValue(),
                                    'bintype': binary,
                                    'SSS': True if self.useSSS.selected else False,
                                    'SSSA': 6*self.SSSA.getValue(), # power of 2
                                    'skinoil': 0.001 *(10**(4*self.skinoil.getValue())), # exponential slider
                                    'rough':0.001 *(10**(2*self.rough.getValue())), # exponential slider
                                    'wrinkles': 0.5*self.wrinkles.getValue(),
                                    'hairSpec':True if self.hairSpec.selected else False,
                                    'hspecA': 0.1*(10**(2*self.hspecA.getValue())), # exponential slider
                                    'hairThin': 5**(2*(1-self.hairThick.getValue()))}) # exponential slider 

    def onShow(self, event):
        self.renderButton.setFocus()
        gui3d.TaskView.onShow(self, event)

# This method is called when the plugin is loaded into makehuman
# The app reference is passed so that a plugin can attach a new category, task, or other GUI elements


def load(app):
    category = app.getCategory('Rendering')
    taskview = category.addTask(PovrayTaskView(category))

# This method is called when the plugin is unloaded from makehuman
# At the moment this is not used, but in the future it will remove the added GUI elements


def unload(app):
    pass
