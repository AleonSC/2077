-- AMM collab pose pack. Based on AMM's own Collabs/Custom Poses/pose_template.lua.
-- Every name below must match, character for character, the animation name
-- in your .anims file, the Blender action you exported, and the .workspot entry.
-- No spaces in names: use underscores (AMM shows them as spaces in the menu).
return {
  -- Your modder name (shown in AMM, also used to tell packs apart).
  modder = "YourName",

  -- Category shown in AMM's Poses tab. If another pack already uses it,
  -- AMM renames yours to "[modder] category".
  category = "My Pose Pack",

  -- Path of your .ent inside the .archive, as shown in WolvenKit.
  -- Backslashes must be doubled. The .ent needs a component named
  -- amm_workspot_collab whose workspot points at your .workspot.
  entity_path = "base\\yourname\\my_pose_pack\\poses.ent",

  -- Animations grouped by rig. Keys must be exactly one of AMM's rig names:
  --   "Woman Average" (woman_base)   "Man Average" (man_base)
  --   "Man Massive" (man_massive)    "Big" (man_big)   "Fat" (man_fat)
  --   "Child" (man_child)
  --   "Player Woman" (player_woman_skeleton)  "Player Man" (player_man_skeleton)
  -- Delete the rigs you don't make poses for.
  anims = {
    ["Woman Average"] = {
      "mpp_f_standing_01",
      "mpp_f_sitting_01",
    },
    ["Man Average"] = {
      "mpp_m_standing_01",
    },
  }
}
