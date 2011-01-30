#
#	Body bone definitions 
#

import mhx_rig
from mhx_rig import *

BodyJoints = [
	('hips-tail',			'o', ('pelvis', [0,-1.0,0])),
	('mid-uplegs',			'l', ((0.5, 'l-upper-leg'), (0.5, 'r-upper-leg'))),

	('chest-front',			'v', 7292),
	('r-rib-top',			'v', 3667),
	('r-rib-bot',			'v', 3400),
	('r-breast1',			'v', 3559),
	('r-breast2',			'v', 2944),
	('r-breast',			'l', ((0.4, 'r-breast1'), (0.6, 'r-breast2'))),
	('r-tit',				'v', 3718),
	('r-stomach',			'v', 6568),
	('r-hip',				'v', 6563),

	('l-rib-top',			'v', 10134),
	('l-rib-bot',			'v', 10361),
	('l-breast1',			'v', 10233),
	('l-breast2',			'v', 10776),
	('l-breast',			'l', ((0.4, 'l-breast1'), (0.6, 'l-breast2'))),
	('l-tit',				'v', 10115),
	('l-hip',				'v', 6749),
	('l-stomach',			'v', 6744),

	('mid-rib-top',			'l', ((0.5, 'r-rib-top'), (0.5, 'l-rib-top'))),
	('mid-rib-bot',			'l', ((0.5, 'r-rib-bot'), (0.5, 'l-rib-bot'))),
	('mid-stomach',			'l', ((0.5, 'r-stomach'), (0.5, 'l-stomach'))),
	('mid-hip',				'l', ((0.5, 'r-hip'), (0.5, 'l-hip'))),

	('abdomen-front',		'v', 7359),
	('abdomen-back',		'v', 7186),
	('stomach-top',			'v', 7336),
	('stomach-bot',			'v', 7297),
	('stomach-front',		'v', 7313),
	('stomach-back',		'v', 7472),

	('penis-tip',			'v', 7415),
	('r-penis',				'v', 2792),
	('l-penis',				'v', 7448),
	('penis-root',			'l', ((0.5, 'r-penis'), (0.5, 'l-penis'))),
	('scrotum-tip',			'v', 7444),
	('r-scrotum',			'v', 2807),
	('l-scrotum',			'v', 7425),
	('scrotum-root',		'l', ((0.5, 'r-scrotum'), (0.5, 'l-scrotum'))),

	('r-toe-1-1',			'j', 'r-toe-1-1'),
	('l-toe-1-1',			'j', 'l-toe-1-1'),
	('mid-feet',			'l', ((0.5, 'l-toe-1-1'), (0.5, 'r-toe-1-1'))),
	('floor',				'o', ('mid-feet', [0,-0.3,0])),
]

BodyHeadsTails = [
	('MasterFloor',			'floor', ('floor', zunit)),
	('MasterHips',			'pelvis', ('pelvis', zunit)),
	('MasterNeck',			'neck', ('neck', zunit)),

	('Root',				'spine3', ('spine3',[0,-1,0])),
	('Hips',				'pelvis', 'hips-tail'),
	('Hip_L',				'spine3', 'r-upper-leg'),
	('Hip_R',				'spine3', 'l-upper-leg'),

	('Spine1',				'spine3', 'spine2'),
	('Spine2',				'spine2', 'spine1'),
	('Spine3',				'spine1', 'neck'),
	('SpineTop',			'neck', ('neck', yunit)),
	('Neck',				'neck', 'head'),
	('Head',				'head', 'head-end'),

	('DefSpine1',			'spine3', 'spine2'),
	('DefSpine2',			'spine2', 'spine1'),
	('DefSpine3',			'spine1', 'neck'),

	('Rib',					'mid-rib-top', 'mid-rib-bot'),
	('StomachUp',			'mid-rib-bot', 'stomach-front'),
	('StomachLo',			'mid-hip', 'stomach-front'),
	('StomachTarget',		'stomach-front', ('stomach-front', zunit)),
	('Breathe',				'mid-rib-bot', ('mid-rib-bot', zunit)),
	('Breast_L',			'r-breast', 'r-tit'),
	('Breast_R',			'l-breast', 'l-tit'),

	('Penis',				'penis-root', 'penis-tip'),
	('Scrotum',				'scrotum-root', 'scrotum-tip'),
]

BodyArmature = [
	('MasterFloor',		0.0, None, F_WIR, L_MAIN, NoBB),
	('MasterHips',		0.0, None, F_WIR+F_HID, L_MAIN, NoBB),
	('MasterNeck',		0.0, None, F_WIR+F_HID, L_MAIN, NoBB),

	('Root',			0.0, Master, F_WIR, L_MAIN+L_SPINE, NoBB),
	('Hips',			0.0, 'Root', F_DEF+F_WIR, L_DEF+L_SPINE, NoBB),
	('Hip_L',			0.0, 'Hips', 0, L_HELP, NoBB),
	('Hip_R',			0.0, 'Hips', 0, L_HELP, NoBB),

	('Spine1',			0.0, 'Root', F_WIR, L_SPINE, NoBB),
	('Spine2',			0.0, 'Spine1', F_WIR, L_SPINE, NoBB),
	('Spine3',			0.0, 'Spine2', F_WIR, L_SPINE, NoBB),
	('SpineTop',		0.0, 'Root', F_WIR, L_SPINE, NoBB ),

	('DefSpine1',		0.0, 'Root', F_DEF, L_DEF, (0,1,3) ),
	('DefSpine2',		0.0, 'DefSpine1', F_DEF+F_CON, L_DEF, (1,1,3) ),
	('DefSpine3',		0.0, 'DefSpine2', F_DEF+F_CON, L_DEF, (1,1,3) ),

	('Neck',			0.0, 'DefSpine3', F_DEF+F_CON+F_WIR, L_SPINE+L_HEAD+L_DEF, (1,1,3) ),
	('Head',			0.0, 'Neck', F_DEF+F_WIR, L_SPINE+L_HEAD+L_DEF, NoBB),

	('Rib',				0.0, 'DefSpine3', F_DEF+F_WIR, L_DEF, NoBB),
	('Breast_L',		-45*D, 'Rib', F_DEF, L_TORSO+L_DEF, NoBB),
	('Breast_R',		45*D, 'Rib', F_DEF, L_TORSO+L_DEF, NoBB),
	('Breathe',			0.0, 'Rib', F_DEF+F_WIR, L_TORSO, NoBB),
	('StomachUp',		0.0, 'Rib', F_DEF, L_DEF, NoBB),
	('StomachLo',		0.0, 'Hips', F_DEF, L_DEF, NoBB),
	('StomachTarget',	0, 'DefSpine1', F_WIR, L_TORSO, NoBB),

	('Penis',			0.0, 'Hips', F_DEF, L_DEF+L_TORSO, (1,5,1) ),
	('Scrotum',			0.0, 'Hips', F_DEF, L_DEF+L_TORSO, NoBB),
]

#
#	BodyWritePoses(fp):
#

def BodyWritePoses(fp):
	addPoseBone(fp,  'MasterFloor', 'MHMaster', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'MasterHips', 'MHMaster', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'MasterNeck', 'MHMaster', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), P_HID, [])

	addPoseBone(fp,  'Root', 'MHRoot', 'Master', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, mhx_rig.rootChildOfConstraints)

	addPoseBone(fp,  'Hips', 'MHCircle20', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-50*D,40*D, -45*D,45*D, -16*D,16*D), (1,1,1)])])

	addPoseBone(fp,  'Hip_L', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	addPoseBone(fp,  'Hip_R', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Control spine
	addPoseBone(fp,  'Spine1', 'MHCircle10', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,90*D, -60*D,60*D, -60*D,60*D), (1,1,1)])])

	addPoseBone(fp,  'Spine2', 'MHCircle10', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-90*D,70*D, -20*D,20*D, -50*D,50*D), (1,1,1)])])

	addPoseBone(fp,  'Spine3', 'MHCircle10', 'Spine', (1,1,1), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-20*D,20*D, 0,0, -20*D,20*D), (1,1,1)]),
		 #('IK', 0, 1, ['IK', None, 2, None, (True, False,True)])
		])

	addPoseBone(fp,  'SpineTop', 'MHCube025', 'Spine', (0,0,0), (0,0,0), (1,1,1), (1,1,1), 0, [])

	# Deform spine
	addPoseBone(fp,  'DefSpine1', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH, 
		[('CopyRot', 0, 1, ['Rot', 'Spine1', (1,1,1), (0,0,0), False])])

	addPoseBone(fp,  'DefSpine2', None, None, (1,1,1), (0,0,0), (1,1,1), (1,1,1), P_STRETCH,
		[('CopyRot', 0, 1, ['Rot', 'Spine2', (1,1,1), (0,0,0), False])])

	addPoseBone(fp,  'DefSpine3', None, None, (0,0,0), (0,1,0), (1,1,1), (1,1,1), P_STRETCH,
 		[('SplineIK', 0, 0, ['SplineIK', '%sSpineCurve' % mh2mhx.theHuman, 3]),
		 ('CopyRot', 0, 1, ['Rot', 'Spine3', (1,1,1), (0,0,0), False])])

	# Neck and head
	addPoseBone(fp,  'Neck', 'MHNeck', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -45*D,45*D, -60*D,60*D), (1,1,1)])])

	addPoseBone(fp,  'Head', 'MHHead', 'Spine', (1,1,1), (0,0,0), (1,1,1), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', (-60*D,40*D, -60*D,60*D, -45*D,45*D), (1,1,1)])])

	# Stomach
	addPoseBone(fp,  'StomachTarget', 'MHCube01', None, (0,0,0), (1,1,1), (0,0,0), (1,1,1), 0, 
		[('LimitDist', 0, 1, ['LimitDist', 'DefSpine1', 'INSIDE'])])

	addPoseBone(fp,  'StomachLo', None, None, (1,1,1), (0,1,0), (1,1,1), (1,1,1), 0, 
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 0]),
		 ('CopyScale', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	addPoseBone(fp,  'StomachUp', None, None, (1,1,1), (1,1,1), (1,1,1), (1,1,1), 0,
		[('StretchTo', 0, 1, ['Stretch', 'StomachTarget', 0]),
		 ('CopyScale', C_OW_LOCAL+C_TG_LOCAL, 1, ['CopyScale', 'StomachTarget', (1,0,1), False]),
		])

	addPoseBone(fp,  'Breathe', 'MHCube01', None, (1,1,0), (1,1,1), (1,1,1), (1,1,1), 0, [])

	limBreastRot = (-45*D,45*D, -10*D,10*D, -20*D,20*D)
	limBreastScale =  (0.8,1.25, 0.7,1.5, 0.8,1.25)

	addPoseBone(fp,  'Breast_L', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, 
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'Breast_R', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0,
 		[('LimitRot', C_OW_LOCAL, 1, ['LimitRot', limBreastRot, (1,1,1)]),
		 ('LimitScale', C_OW_LOCAL, 1, ['Scale', limBreastScale, (1,1,1)])	])

	addPoseBone(fp,  'Penis', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

	addPoseBone(fp,  'Scrotum', None, None, (1,1,1), (0,0,0), (0,0,0), (1,1,1), 0, [])

	return

#
#	BodyWriteCurves(fp):
#

def BodyWriteCurves(fp):
	addCurve(fp, 'SpineCurve', ['Root', 'Spine1', 'Spine2', 'Spine3', 'SpineTop'])
	return

#
#	BodyProperties
#	BodyPropDrivers
#

BodyProperties = [
	('Root_parent', D_ENUM, ["Floor","Hips","Neck"], ['name="Master"', 'description=""'] ),
	('Spine_IK', D_BOOL, False, ['name="Spine_IK"']),
]

MasterDrivers = [('Floor', 'x==0'), ('Hips', 'x==1'), ('Neck', 'x==2')]

BodyPropDrivers = [
	('DefSpine3', 'Spine_IK', D_BOOL, ['SplineIK']),
	('DefSpine1', 'Spine_IK', D_BOOLINV, ['Rot']),
	('DefSpine2', 'Spine_IK', D_BOOLINV, ['Rot']),
	('DefSpine3', 'Spine_IK', D_BOOLINV, ['Rot']),
]

"""
	('Root', 'Root_parent', D_ENUM, MasterDrivers),
	('ElbowIK_L', 'Root_parent', D_ENUM, MasterDrivers),
	('ElbowIK_R', 'Root_parent', D_ENUM, MasterDrivers),
	('WristIK_L', 'Root_parent', D_ENUM, MasterDrivers),
	('WristIK_R', 'Root_parent', D_ENUM, MasterDrivers),
	('LegIK_L', 'Root_parent', D_ENUM, MasterDrivers),
	('LegIK_R', 'Root_parent', D_ENUM, MasterDrivers),
]
"""
#
#	BodyShapeDrivers
#	Shape : (driver, channel, coeff)
#

BodyShapeDrivers = {
	'BreatheIn' : ('Breathe', 'LOC_Z', ('0', '2.0')), 
}

#
#	BodyShapeKeyScale = {
#

BodyShapeKeyScale = {
	'BreatheIn'			: ('spine1', 'neck', 1.89623),
	'BicepFlex'			: ('r-uparm-front', 'r-uparm-back', 0.93219),
}


