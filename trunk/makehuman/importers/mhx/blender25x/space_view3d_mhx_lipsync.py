""" 
**Project Name:**	  MakeHuman

**Product Home Page:** http://www.makehuman.org/

**Code Home Page:**	http://code.google.com/p/makehuman/

**Authors:**		   Thomas Larsson

**Copyright(c):**	  MakeHuman Team 2001-2010

**Licensing:**		 GPL3 (see also http://sites.google.com/site/makehumandocs/licensing)

**Coding Standards:**  See http://sites.google.com/site/makehumandocs/developers-guide

Abstract
Lipsync for the MHX rig and Blender 2.5x.
Version 0.3

"""

bl_info = {
	'name': 'MakeHuman lipsync',
	'author': 'Thomas Larsson',
	'version': '0.5',
	'blender': (2, 5, 6),
	"api": 34076,
	"location": "View3D > UI panel > MHX Mocap",
	"description": "Lipsync for the MHX rig",
	"warning": "",
	"category": "3D View"}

"""
Run from text window. 
Access from UI panel (N-key) when MHX rig is active.
"""

MAJOR_VERSION = 0
MINOR_VERSION = 5
BLENDER_VERSION = (2, 56, 0)

import bpy, os, mathutils
from mathutils import *
from bpy.props import *

theRig = None
theMesh = None

#
#	visemes
#

stopStaringVisemes = ({
	'Rest' : [
		('PMouth', (0,0)), 
		('PUpLip', (0,-0.1)), 
		('PLoLip', (0,0.1)), 
		('PJaw', (0,0.05)), 
		('PTongue', (0,0.0))], 
	'Etc' : [
		('PMouth', (0,0)),
		('PUpLip', (0,-0.1)),
		('PLoLip', (0,0.1)),
		('PJaw', (0,0.15)),
		('PTongue', (0,0.0))], 
	'MBP' : [('PMouth', (-0.3,0)),
		('PUpLip', (0,1)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.1)),
		('PTongue', (0,0.0))], 
	'OO' : [('PMouth', (-1.5,0)),
		('PUpLip', (0,0)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.2)),
		('PTongue', (0,0.0))], 
	'O' : [('PMouth', (-1.1,0)),
		('PUpLip', (0,0)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.5)),
		('PTongue', (0,0.0))], 
	'R' : [('PMouth', (-0.9,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0,0.2)),
		('PTongue', (0,0.0))], 
	'FV' : [('PMouth', (0,0)),
		('PUpLip', (0,0)),
		('PLoLip', (0,-0.8)),
		('PJaw', (0,0.1)),
		('PTongue', (0,0.0))], 
	'S' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0,0.05)),
		('PTongue', (0,0.0))], 
	'SH' : [('PMouth', (-0.6,0)),
		('PUpLip', (0,-0.5)),
		('PLoLip', (0,0.5)),
		('PJaw', (0,0)),
		('PTongue', (0,0.0))], 
	'EE' : [('PMouth', (0.3,0)),
		('PUpLip', (0,-0.3)),
		('PLoLip', (0,0.3)),
		('PJaw', (0,0.025)),
		('PTongue', (0,0.0))], 
	'AH' : [('PMouth', (-0.1,0)),
		('PUpLip', (0,-0.4)),
		('PLoLip', (0,0)),
		('PJaw', (0,0.35)),
		('PTongue', (0,0.0))], 
	'EH' : [('PMouth', (0.1,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0,0.2)),
		('PTongue', (0,0.0))], 
	'TH' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.5)),
		('PLoLip', (0,0.5)),
		('PJaw', (-0.2,0.1)),
		('PTongue', (0,-0.6))], 
	'L' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.2)),
		('PLoLip', (0,0.2)),
		('PJaw', (0.2,0.2)),
		('PTongue', (0,-0.8))], 
	'G' : [('PMouth', (0,0)),
		('PUpLip', (0,-0.1)),
		('PLoLip', (0,0.1)),
		('PJaw', (-0.3,0.1)),
		('PTongue', (0,-0.6))], 

	'Blink' : [('PUpLid', (0,1.0)), ('PLoLid', (0,-1.0))], 
	'UnBlink' : [('PUpLid', (0,0)), ('PLoLid', (0,0))], 
})

bodyLanguageVisemes = ({
	'Rest' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,-0.6)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'Etc' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,-0.4)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'MBP' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'OO' : [
		('PMouth', (-1.0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.4)), 
		('PTongue', (0,0))], 
	'O' : [
		('PMouth', (-0.9,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.8)), 
		('PTongue', (0,0))], 
	'R' : [
		('PMouth', (-0.5,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.2)), 
		('PLoLipMid', (0,0.2)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'FV' : [
		('PMouth', (-0.2,0)), 
		('PMouthMid', (0,1.0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (-0.6,-0.3)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'S' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.7)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'SH' : [
		('PMouth', (-0.8,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-1.0)), 
		('PLoLipMid', (0,1.0)), 
		('PJaw', (0,0)), 
		('PTongue', (0,0))], 
	'EE' : [
		('PMouth', (0.2,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.6)), 
		('PLoLipMid', (0,0.6)), 
		('PJaw', (0,0.05)), 
		('PTongue', (0,0))], 
	'AH' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.4)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.7)), 
		('PTongue', (0,0))], 
	'EH' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.6)), 
		('PJaw', (0,0.25)), 
		('PTongue', (0,0))], 
	'TH' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,0)), 
		('PLoLipMid', (0,0)), 
		('PJaw', (0,0.2)), 
		('PTongue', (1.0,1.0))], 
	'L' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.5)), 
		('PJaw', (0,-0.2)), 
		('PTongue', (1.0,1.0))], 
	'G' : [
		('PMouth', (0,0)), 
		('PMouthMid', (0,0)), 
		('PUpLipMid', (0,-0.5)), 
		('PLoLipMid', (0,0.5)), 
		('PJaw', (0,-0.2)), 
		('PTongue', (-1.0,0))], 

	'Blink' : [('PUpLid', (0,1.0)), ('PLoLid', (0,-1.0))], 
	'UnBlink' : [('PUpLid', (0,0)), ('PLoLid', (0,0))], 
})

#
#	mohoVisemes
#	magpieVisemes
#

mohoVisemes = dict({
	'rest' : 'Rest', 
	'etc' : 'Etc', 
	'AI' : 'AH', 
	'O' : 'O', 
	'U' : 'OO', 
	'WQ' : 'AH', 
	'L' : 'L', 
	'E' : 'EH', 
	'MBP' : 'MBP', 
	'FV' : 'FV', 
})

magpieVisemes = dict({
	"CONS" : "t,d,k,g,T,D,s,z,S,Z,h,n,N,j,r,tS", 
	"AI" : "i,&,V,aU,I,0,@,aI", 
	"E" : "eI,3,e", 
	"O" : "O,@U,oI", 
	"UW" : "U,u,w", 
	"MBP" : "m,b,p", 
	"L" : "l", 
	"FV" : "f,v", 
	"Sh" : "dZ", 
})

#
#	Expressions - the same as in read_expression.py
#

Expressions = [
	'smile',
	'hopeful',
	'innocent',
	'tender',
	'seductive',

	'grin',
	'excited',
	'ecstatic',

	'proud',
	'pleased',
	'amused',
	'laughing1',
	'laughing2',

	'so-so',
	'blue',
	'depressed',
	'sad',
	'distressed',
	'crying',
	'pain',

	'disappointed',
	'frustrated',
	'stressed',
	'worried',
	'scared',
	'terrified',

	'shy',
	'guilty',
	'embarassed',
	'relaxed',
	'peaceful',
	'refreshed',

	'lazy',
	'bored',
	'tired',
	'drained',
	'sleepy',
	'groggy',

	'curious',
	'surprised',
	'impressed',
	'puzzled',
	'shocked',
	'frown',
	'upset',
	'angry',
	'enraged',

	'skeptical',
	'vindictive',
	'pout',
	'furious',
	'grumpy',
	'arrogant',
	'sneering',
	'haughty',
	'disgusted',
]

#
#	setViseme(context, vis, setKey, frame):
#	setBoneLocation(context, pbone, loc, mirror, setKey, frame):
#

def getVisemeSet(context):
	if context.scene['MhxBodyLanguage'] == True:
		return bodyLanguageVisemes
	else:
		return stopStaringVisemes

def setViseme(context, vis, setKey, frame):
	global theRig
	pbones = theRig.pose.bones
	try:
		scale = pbones['PFace'].bone.length
	except:
		return
	visemes = getVisemeSet(context)
	for (b, (x, z)) in visemes[vis]:
		loc = mathutils.Vector((float(x),0,float(z)))
		try:
			pb = pbones[b]
		except:
			pb = None
			
		if pb:
			setBoneLocation(context, pb, scale, loc, False, setKey, frame)
		else:
			setBoneLocation(context, pbones[b+'_L'], scale, loc, False, setKey, frame)
			setBoneLocation(context, pbones[b+'_R'], scale, loc, True, setKey, frame)
	return

def setBoneLocation(context, pb, scale, loc, mirror, setKey, frame):
	if mirror:
		loc[0] = -loc[0]
	pb.location = loc*scale*0.2
	if setKey or context.scene['MhxSyncAutoKeyframe']:
		for n in range(3):
			pb.keyframe_insert('location', index=n, frame=frame, group=pb.name)
	return

#
#	openFile(context, filepath):
#	readMoho(context, filepath, offs):
#	readMagpie(context, filepath, offs):
#

def openFile(context, filepath):
	(path, fileName) = os.path.split(filepath)
	(name, ext) = os.path.splitext(fileName)
	return open(filepath, "rU")

def readMoho(context, filepath, offs):
	context.scene.objects.active = theRig
	bpy.ops.object.mode_set(mode='POSE')	
	fp = openFile(context, filepath)		
	for line in fp:
		words= line.split()
		if len(words) < 2:
			pass
		else:
			vis = mohoVisemes[words[1]]
			setViseme(context, vis, True, int(words[0])+offs)
	fp.close()
	setInterpolation(context.object)
	print("Moho file %s loaded" % filepath)
	return

def readMagpie(context, filepath, offs):
	context.scene.objects.active = theRig
	bpy.ops.object.mode_set(mode='POSE')	
	fp = openFile(context, filepath)		
	for line in fp: 
		words= line.split()
		if len(words) < 3:
			pass
		elif words[2] == 'X':
			vis = magpieVisemes[words[3]]
			setViseme(context, vis, True, int(words[0])+offs)
	fp.close()
	setInterpolation(context.object)
	print("Magpie file %s loaded" % filepath)
	return

#
#	setInterpolation(rig):
#

def setInterpolation(rig):
	if not rig.animation_data:
		return
	act = rig.animation_data.action
	if not act:
		return
	for fcu in act.fcurves:
		for pt in fcu.keyframe_points:
			pt.interpolation = 'LINEAR'
		fcu.extrapolation = 'CONSTANT'
	return
	
###################################################################################	
#	User interface
#
#	initInterface()
#

def initInterface(scn):
	bpy.types.Scene.MhxSyncAutoKeyframe = BoolProperty(
		name="Auto keyframe", 
		description="Auto keyframe",
		default=False)

	bpy.types.Scene.MhxBodyLanguage = BoolProperty(
		name="Body Language", 
		description="Use Body Language shapekey set",
		default=True)		

	if scn:
		scn['MhxSyncAutoKeyframe'] = False
		scn['MhxBodyLanguage'] = True

	#defineEnumButtons('Gaze', ['Gaze'], ['Head', 'World'])
	#defineEnumButtons('Master', ['Root', 'HandIK_L', 'HandIK_R', 'LegIK_L', 'LegIK_R'], ['Floor', 'Hips', 'Neck'])
	return

# Define viseme buttons

def defineVisemeButtons():
	visemes = bodyLanguageVisemes
	for vis in visemes.keys():
		expr = (
"class VIEW3D_OT_Mhx%sButton(bpy.types.Operator):\n" % vis +
"	bl_idname = 'view3d.mhx_%s'\n" % vis.lower() +
"	bl_label = '%s'\n" % vis +	
"	def invoke(self, context, event):\n" +
"		global bpy, mathutils\n" +
"		setViseme(context, '%s', False, context.scene.frame_current)\n" % vis +
"		return{'FINISHED'}\n"
		)
		# print(expr)
		exec(expr, globals(), locals())
	return

#
#	class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxInitInterfaceButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_init_interface"
	bl_label = "Initialize"
	bl_options = {'REGISTER'}

	def execute(self, context):
		import bpy
		initInterface(context.scene)
		print("Interface initialized")
		return{'FINISHED'}	

# 
#	class VIEW3D_OT_MhxLoadMohoButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxLoadMohoButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_load_moho"
	bl_label = "Moho (.dat)"
	filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
	startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

	def execute(self, context):
		import bpy, os, mathutils
		readMoho(context, self.properties.filepath, self.properties.startFrame-1)		
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}	

#
#	class VIEW3D_OT_MhxLoadMagpieButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxLoadMagpieButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_load_magpie"
	bl_label = "Magpie (.mag)"
	filepath = StringProperty(name="File Path", description="File path used for importing the file", maxlen= 1024, default= "")
	startFrame = IntProperty(name="Start frame", description="First frame to import", default=1)

	def execute(self, context):
		import bpy, os, mathutils
		readMagpie(context, self.properties.filepath, self.properties.startFrame-1)		
		return{'FINISHED'}	

	def invoke(self, context, event):
		context.window_manager.fileselect_add(self)
		return {'RUNNING_MODAL'}	


#
#	meshHasExpressions(mesh):
#	rigHasExpressions(rig):
#
	
def meshHasExpressions(mesh):
	return ('guilty' in mesh.data.shape_keys.keys.keys())

def rigHasExpressions(rig):
	return ('Pguilty' in rig.pose.bones.keys())

#
#	class VIEW3D_OT_MhxResetExpressionsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxResetExpressionsButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_reset_expressions"
	bl_label = "Reset expressions"

	def execute(self, context):
		global theMesh
		keys = theMesh.data.shape_keys
		if keys:
			for name in Expressions:
				try:
					keys.keys[name].value = 0.0
				except:
					pass
		print("Expressions reset")
		return{'FINISHED'}	

#
#	class VIEW3D_OT_MhxResetBoneExpressionsButton(bpy.types.Operator):
#

class VIEW3D_OT_MhxResetBoneExpressionsButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_reset_bone_expressions"
	bl_label = "Reset expressions"

	def execute(self, context):
		global theRig
		pbones = theRig.pose.bones
		if pbones:
			for name in Expressions:
				try:
					pb = pbones['P%s' % name]
					pb.location[1] = 0.0
				except:
					pass
		print("Expressions reset")
		return{'FINISHED'}
		
#
#	createDrivers(context):	
#
#	class VIEW3D_OT_MhxCreateDriversButton(bpy.types.Operator):
#

def createDrivers(context):		
	global theMesh, theRig
	keys = theMesh.data.shape_keys
	if keys:
		context.scene.objects.active = theRig
		bpy.ops.object.mode_set(mode = 'EDIT')
		ebones = theRig.data.edit_bones		
		pface = ebones['PFace']
		layers = 32*[False]
		layers[31] = True
		
		for name in Expressions:
			eb = ebones.new("P%s" % name)
			eb.head = pface.head
			eb.tail = pface.tail
			eb.parent = pface
			eb.layers = layers

		bpy.ops.object.mode_set(mode = 'POSE')
		for name in Expressions:			
			try:
				createDriver(name, keys)
			except:
				pass
	return
				
def createDriver(name, keys):
	global theRig
	print("Create driver %s" % name)
	fcu = keys.keys[name].driver_add('value')

	drv = fcu.driver
	drv.type = 'AVERAGE'
	drv.show_debug_info = True

	var = drv.variables.new()
	var.name = 'x'
	var.type = 'TRANSFORMS'
	
	trg = var.targets[0]
	trg.id = theRig
	trg.transform_type = 'LOC_Y'
	trg.bone_target = 'P%s' % name
	trg.use_local_space_transform = True
	
	#fmod = fcu.modifiers.new('GENERATOR')
	fmod = fcu.modifiers[0]
	fmod.coefficients = (0, 1.0)
	fmod.show_expanded = True
	fmod.mode = 'POLYNOMIAL'
	fmod.mute = False
	fmod.poly_order = 1

	return
	
class VIEW3D_OT_MhxCreateDriversButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_create_drivers"
	bl_label = "Create drivers"

	def execute(self, context):
		createDrivers(context)
		print("Drivers created")
		return{'FINISHED'}	

#
#	removeDrivers(context):		
#	class VIEW3D_OT_MhxRemoveDriversButton(bpy.types.Operator):
#

def removeDrivers(context):		
	global theMesh, theRig
	keys = theMesh.data.shape_keys
	if keys:
		context.scene.objects.active = theRig
		bpy.ops.object.mode_set(mode = 'EDIT')
		ebones = theRig.data.edit_bones				
		for name in Expressions:
			try:
				ebones.remove(ebones["P%s" % name])
			except:
				pass
		bpy.ops.object.mode_set(mode = 'POSE')
		for name in Expressions:			
			try:
				keys.keys[name].driver_remove('value')
				print("Removed driver %s" % name)
			except:
				pass
	return

class VIEW3D_OT_MhxRemoveDriversButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_remove_drivers"
	bl_label = "Remove drivers"

	def execute(self, context):
		removeDrivers(context)
		print("Drivers removed")
		return{'FINISHED'}	

#
#	setGlobals(context):
#

def setGlobals(context):
	global theRig, theMesh, theScale	
	if context.object.type == 'ARMATURE':
		theRig = context.object
		theMesh = None
		for child in theRig.children:
			if (child.type == 'MESH' and meshHasExpressions(child)):
				theMesh = child
				break
	elif context.object.type == 'MESH':
		if meshHasExpressions(context.object):
			theMesh = context.object
			theRig = theMesh.parent
		else:
			return
	else:
		return

	try:
		theRig.data.bones['PArmIK_L']
	except:
		theRig = None	
		
#
#	setAllFKIK(value):
#	class VIEW3D_OT_MhxSetAllFKButton(bpy.types.Operator):
#	class VIEW3D_OT_MhxSetAllIKButton(bpy.types.Operator):
#

def setAllFKIK(value):
	global theRig
	pbones = theRig.pose.bones
	for name in ['PArmIK', 'PLegIK']:
		for suffix in ['_L', '_R']:
			pbones[name+suffix].location[0] = value
	return

class VIEW3D_OT_MhxSetAllFKButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_set_all_fk"
	bl_label = "All FK"

	def execute(self, context):
		setAllFKIK(0.0)
		return{'FINISHED'}	

class VIEW3D_OT_MhxSetAllIKButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_set_all_ik"
	bl_label = "All IK"

	def execute(self, context):
		setAllFKIK(1.0)
		return{'FINISHED'}	


#
#	setAllFingers(value):
#	class VIEW3D_OT_MhxSetAllFingersOffButton(bpy.types.Operator):
#	class VIEW3D_OT_MhxSetAllFingersOnButton(bpy.types.Operator):
#

def setAllFingers(value):
	global theRig
	pbones = theRig.pose.bones
	for n in range(1,6):
		for suffix in ['_L', '_R']:
			pbones['PFinger-%d%s' % (n, suffix)].location[0] = value
	return

class VIEW3D_OT_MhxSetAllFingersOffButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_set_all_fingers_off"
	bl_label = "All off"

	def execute(self, context):
		setAllFingers(0.0)
		return{'FINISHED'}	

class VIEW3D_OT_MhxSetAllFingersOnButton(bpy.types.Operator):
	bl_idname = "view3d.mhx_set_all_fingers_on"
	bl_label = "All on"

	def execute(self, context):
		setAllFingers(0.7)
		return{'FINISHED'}	

#
#	setEnum(name, cnslist):
#	defineEnumButtons(name, bones, enums):
#
"""
def setEnum(name, cnslist):
	global theRig
	pb = theRig.pose.bones[name]
	for (cnsName, inf) in cnslist:
		pb.constraints[cnsName].influence = inf
	return	

def defineEnumButtons(name, bones, enums):
	for enum in enums:
		elist = []
		for enum1 in enums1:
			elist.append( ('%s' % enum1, (enum==enum1)*1) )
		expr = (
'class VIEW3D_OT_MhxSet%s%sButton(bpy.types.Operator):\n' % (name, enum) +
'	bl_idname = "view3d.mhx_set_%s_%s"\n' % (name.lower(), enum.lower()) +
'	bl_label = "%s"\n' % enum +
'	def execute(self, context):\n' +
'		for bone in %s:\n' % bones +
'			setEnum(name, %s)\n' % elist +
'		return{"FINISHED"}	\n'
		)
		print(expr)
		exec(expr)
	return
"""
#
#	class MhxDriversPanel(bpy.types.Panel):
#

class MhxDriversPanel(bpy.types.Panel):
	bl_label = "MHX Drivers"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		return None

	def draw(self, context):
		setGlobals(context)
		layout = self.layout
		layout.operator("view3d.mhx_init_interface")
		"""		
		if theRig:
			pbones = theRig.pose.bones
			layout.label("Arm and leg FK/IK")
			layout.prop(pbones['PArmIK_L'], 'location', index=0, text='Arm IK Left')
			layout.prop(pbones['PArmIK_R'], 'location', index=0, text='Arm IK Right')
			layout.prop(pbones['PLegIK_L'], 'location', index=0, text='Leg IK Left')
			layout.prop(pbones['PLegIK_R'], 'location', index=0, text='Leg IK Right')
			row = layout.row()
			row.operator("view3d.mhx_set_all_fk")
			row.operator("view3d.mhx_set_all_ik")

			layout.label("Finger control")
			fingers = ['Thumb', 'Index', 'Long', 'Ring', 'Pinky']
			for n in range(1,6):				
				row = layout.row()
				row.prop(pbones['PFinger-%d_L' % n], 'location', index=0, text='L '+fingers[n-1])
				row.prop(pbones['PFinger-%d_R' % n], 'location', index=0, text='R '+fingers[n-1])
			row = layout.row()
			row.operator("view3d.mhx_set_all_fingers_off")
			row.operator("view3d.mhx_set_all_fingers_on")

			layout.label("Gaze")
			row = layout.row()
			row.operator("view3d.mhx_set_gaze_head")
			row.operator("view3d.mhx_set_gaze_world")

			layout.label("Master")
			row = layout.row()
			row.operator("view3d.mhx_set_master_floor")
			row.operator("view3d.mhx_set_master_hips")
			row.operator("view3d.mhx_set_master_neck")

		"""

#
#	class MhxLipsyncPanel(bpy.types.Panel):
#

class MhxLipsyncPanel(bpy.types.Panel):
	bl_label = "MHX Lipsync"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		return context.object

	def draw(self, context):
		setGlobals(context)
		layout = self.layout
		layout.operator("view3d.mhx_init_interface")
		
		if theRig:
			layout.separator()
			layout.prop(context.scene, 'MhxSyncAutoKeyframe')
			layout.prop(context.scene, 'MhxBodyLanguage')
			layout.label(text="Visemes")
			row = layout.row()
			row.operator("view3d.mhx_rest")
			row.operator("view3d.mhx_etc")
			row.operator("view3d.mhx_ah")
			row = layout.row()
			row.operator("view3d.mhx_mbp")
			row.operator("view3d.mhx_oo")
			row.operator("view3d.mhx_o")
			row = layout.row()
			row.operator("view3d.mhx_r")
			row.operator("view3d.mhx_fv")
			row.operator("view3d.mhx_s")
			row = layout.row()
			row.operator("view3d.mhx_sh")
			row.operator("view3d.mhx_ee")
			row.operator("view3d.mhx_eh")
			row = layout.row()
			row.operator("view3d.mhx_th")
			row.operator("view3d.mhx_l")
			row.operator("view3d.mhx_g")
			layout.separator()
			row = layout.row()
			row.operator("view3d.mhx_blink")
			row.operator("view3d.mhx_unblink")
			layout.label(text="Load file")
			row = layout.row()
			row.operator("view3d.mhx_load_moho")
			row.operator("view3d.mhx_load_magpie")

#
#	class MhxExpressionsPanel(bpy.types.Panel):
#

class MhxExpressionsPanel(bpy.types.Panel):
	bl_label = "MHX Expressions"
	bl_space_type = "VIEW_3D"
	bl_region_type = "UI"
	
	@classmethod
	def poll(cls, context):
		return context.object

	def draw(self, context):
		setGlobals(context)
		layout = self.layout
		layout.operator("view3d.mhx_init_interface")
		
		if theRig and rigHasExpressions(theRig):
			layout.separator()
			layout.label(text="Expressions (driven)")
			layout.operator("view3d.mhx_reset_bone_expressions")
			layout.operator("view3d.mhx_remove_drivers")
			layout.separator()
			pbones = theRig.pose.bones
			for name in Expressions:
				try:
					pb = pbones['P%s' % name]
					layout.prop(pb, 'location', index=1, text=name)
				except:
					pass
		
		elif theMesh and meshHasExpressions(theMesh):	
			layout.separator()
			layout.label(text="Expressions")
			layout.operator("view3d.mhx_reset_expressions")
			layout.operator("view3d.mhx_create_drivers")
			layout.separator()
			keys = theMesh.data.shape_keys
			if keys:
				for name in Expressions:
					try:
						datum = keys.keys[name]
						layout.prop(datum, 'value', text=name)
					except:
						pass
		return

#
#	initialize and register
#

initInterface(bpy.context.scene)
defineVisemeButtons()

def register():
	pass

def unregister():
	pass

if __name__ == "__main__":
	register()


