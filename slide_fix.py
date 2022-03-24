import maya.cmds as cmds
import get_ctrl


def slide_fix(L_foot, R_foot):
    # foot status:
    # 0 contact
    # 1 on_the_ground
    # 2 off_the_ground
    # 3 in_the_air
    foot_IK_list = [L_foot, R_foot]

    # start time of playback
    start = cmds.playbackOptions(q=1, min=1)
    # end time of playback
    end = cmds.playbackOptions(q=1, max=1)

    first_frame = cmds.keyframe(L_foot, query=True, timeChange=True)[0]
    last_frame = cmds.keyframe(L_foot, query=True, timeChange=True)[-1]

    value_needed = ['tx', 'ty', 'tz', 'rx', 'ry', 'rz']

    for foot in foot_IK_list:
        # store temp data
        # foot_position_dict--> {'tx':0, 'ty':0, 'tz':0, 'rx':0, 'ry':0, 'rz':0}
        foot_position_dict = {}
        foot_down = 0
        for frame in range(int(start), int(end)+1):
            #set keys on TY of every frame
            foot_TY_name = foot + '.translateY'
            current_foot_TY_value = cmds.getAttr(foot_TY_name, time=frame)
            cmds.setKeyframe(foot, at="ty", time=frame, value=current_foot_TY_value)

            TY_value = cmds.keyframe(foot, at='ty', query=True, index=(frame - 1, frame), valueChange=True)[0]
            TY_value = round(TY_value, 1)

            # contact frame --> store keyframe value
            # translate y == 0 and it's first frame down
            if TY_value == 0 and foot_down == 0:
                for i in range(0, 6):
                    foot_position_dict[value_needed[i]] = \
                        cmds.keyframe(foot, at=value_needed[i], query=True, index=(frame - 1, frame), valueChange=True)[0]

                foot_down = 1

            # foot on the ground --> pin the foot
            # translate y == 0 and it's not the first frame down
            elif TY_value == 0 and foot_down == 1:
                # frame 1 --> store value
                if frame == 1:
                    for i in range(0, 6):
                        foot_position_dict[value_needed[i]] = \
                            cmds.keyframe(foot, at=value_needed[i], query=True, index=(frame - 1, frame),
                                          valueChange=True)[0]
                # not frame 1 --> set keys on foot_IK
                else:
                    for i in range(0, 6):
                        cmds.setKeyframe(foot, at=value_needed[i],
                                         value=foot_position_dict[value_needed[i]], time=frame)

            # off the ground
            # translate y != 0 and the previous frame is on the ground
            elif TY_value != 0 and foot_down == 1:
                foot_down = 0

            # in the air --> no need to do anything


def fix_execute():
    rig_main = cmds.ls(selection=True)
    ch_ctrl = get_ctrl.ctrl_needed(rig_main)
    # ch_ctrl--> {"Namespace_1":{"head":"Namespace_1:Head_ctrl", ....},...}
    for ch in ch_ctrls:
        slide_fix(ch_ctrls[ch]["L_foot_IK"], ch_ctrls[ch]["R_foot_IK"])

# def fix_execute():
#     selected = cmds.ls(selection=True)
#     slide_fix(selected[0], selected[1])




