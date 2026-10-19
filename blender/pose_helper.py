"""
Blender helper for making Cyberpunk 2077 poses.

Run it from Blender's Scripting tab (Text Editor > Open > Run Script) after
importing a rig with the Cyberpunk Blender add-on (WolvenKit Blender IO Suite).

What it does:
  * new_pose(name)    - makes a new Action called `name`, assigns it to the
                        selected armature and keys every bone at its current
                        pose. Pose the rig first, then call this.
  * reset_pose()      - puts every bone back to its rest pose so you can
                        start the next pose from neutral.
  * list_poses()      - prints all pose actions, flagging bad names.

The Action name is the animation name. It has to match the .anims entry,
the .workspot entry and the AMM .lua file exactly, so the name is checked
here before anything is created.

Example (in Blender's Python console, after running this script once):
    reset_pose()
    # ... pose the rig by hand ...
    new_pose("mpp_f_standing_01")
"""

import re

import bpy

# A pose is held still, so two identical keys are enough. Keep this matching
# the frame range the Cyberpunk add-on exports.
POSE_FRAMES = (0, 1)
VALID_NAME = re.compile(r"^[a-z0-9_]+$")


def _armature():
    obj = bpy.context.active_object
    if obj is None or obj.type != "ARMATURE":
        raise RuntimeError("Select the Cyberpunk armature (the rig) first.")
    return obj


def _check_name(name):
    if not VALID_NAME.match(name):
        raise ValueError(
            f"Bad pose name {name!r}: use lowercase letters, digits and "
            "underscores only (no spaces)."
        )


def new_pose(name):
    """Store the armature's current pose as a new Action called `name`."""
    _check_name(name)
    if name in bpy.data.actions:
        raise ValueError(f"An action called {name!r} already exists.")

    arm = _armature()
    if arm.animation_data is None:
        arm.animation_data_create()

    action = bpy.data.actions.new(name)
    # Keep the action in the .blend file even while it isn't assigned.
    action.use_fake_user = True
    arm.animation_data.action = action

    for frame in POSE_FRAMES:
        for bone in arm.pose.bones:
            bone.keyframe_insert("location", frame=frame)
            if bone.rotation_mode == "QUATERNION":
                bone.keyframe_insert("rotation_quaternion", frame=frame)
            else:
                bone.keyframe_insert("rotation_euler", frame=frame)
            bone.keyframe_insert("scale", frame=frame)

    bpy.context.scene.frame_start, bpy.context.scene.frame_end = POSE_FRAMES
    print(f"Saved pose {name!r} ({len(arm.pose.bones)} bones keyed).")
    return action


def reset_pose():
    """Clear the current pose back to the rig's rest position."""
    arm = _armature()
    if arm.animation_data is not None:
        arm.animation_data.action = None
    for bone in arm.pose.bones:
        bone.location = (0.0, 0.0, 0.0)
        bone.rotation_quaternion = (1.0, 0.0, 0.0, 0.0)
        bone.rotation_euler = (0.0, 0.0, 0.0)
        bone.scale = (1.0, 1.0, 1.0)
    print("Pose reset to rest.")


def list_poses():
    """Print every action in the file and flag names AMM would reject."""
    for action in bpy.data.actions:
        ok = "ok " if VALID_NAME.match(action.name) else "BAD"
        print(f"[{ok}] {action.name}")
