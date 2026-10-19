# My Pose Pack: custom Cyberpunk 2077 poses

A starter project for making your own poses and animations and playing them
in game through **Appearance Menu Mod (AMM)**.

## How it fits together

```
Blender (pose the rig) ──export .glb──▶ WolvenKit
                                          ├─ poses.anims      the pose data, one entry per pose
                                          ├─ poses.workspot   lists which anims can be played
                                          └─ poses.ent        component "amm_workspot_collab" → workspot
                                                 │ packed into an .archive
AMM .lua (this repo) ──entity_path──────────────┘ tells AMM the names and which rig they're for
```

**One rule above all:** every pose name has to be identical in four places:
the Blender action, the `.anims` file, the `.workspot` file and the `.lua`.
Use lowercase letters, digits and underscores, with no spaces.
`tools/check_names.py` checks this for you.

## What you need (Windows PC with the game)

| Tool | What it's for |
|---|---|
| [Cyber Engine Tweaks](https://www.nexusmods.com/cyberpunk2077/mods/107) | needed by AMM |
| [Appearance Menu Mod](https://www.nexusmods.com/cyberpunk2077/mods/790) | plays your poses in game |
| [WolvenKit](https://github.com/WolvenKit/WolvenKit) | exports rigs, builds `.anims/.workspot/.ent`, packs the `.archive` |
| [Blender](https://www.blender.org/) + the **Cyberpunk Blender add-on** (WolvenKit Blender IO Suite) | posing; use the Blender version the add-on's release notes ask for |

## Files in this repo

| Path | What it is |
|---|---|
| `mod/bin/x64/.../Collabs/Custom Poses/my_pose_pack.lua` | the AMM pose list. Copy it into your game folder at the same path |
| `blender/pose_helper.py` | Blender script: save the current pose as a correctly named action, reset to rest, list poses |
| `tools/check_names.py` | checks that names match between the `.lua` and WolvenKit's JSON exports |
| `wolvenkit/` | put your WolvenKit project here (see `.gitignore` for what's left out) |

## Step by step

### 1. Set up a WolvenKit project
1. Create a new WolvenKit project inside `wolvenkit/`.
2. Start from a **pose template**, not from scratch. The RED Modding wiki's AMM
   collab guide links a template project and the "Easy AMM Poses" tool. Copy
   the template's `.anims`, `.workspot` and `.ent` into your project under a
   folder of your own, for example `base\yourname\my_pose_pack\`.
3. Open the `.ent` and check that the `amm_workspot_collab` component's
   workspot points to **your** `.workspot`. Leave everything else as it is.

### 2. Get the rig into Blender
1. In WolvenKit, export the template `.anims` to `.glb` with the Export Tool.
   It comes out with the rig it targets (e.g. `woman_base`).
2. In Blender, import that `.glb` using the Cyberpunk add-on's importer
   (File > Import > Cyberpunk GLTF). Importing a body mesh as well makes
   posing much easier.

### 3. Pose in Blender
1. Scripting tab > Open `blender/pose_helper.py` > **Run Script**.
2. Select the armature, enter Pose Mode and pose it.
3. In the Python console:
   ```python
   new_pose("mpp_f_standing_01")   # saves the pose as an action with this name
   reset_pose()                    # back to neutral for the next one
   list_poses()                    # check names
   ```
   For a moving animation instead of a still pose, key the frames you want
   yourself in the Action Editor. The action name is still the animation name.
4. Export with the Cyberpunk add-on's glTF exporter (File > Export > Cyberpunk GLB),
   writing over the `.glb` WolvenKit exported in step 2.

### 4. Back into WolvenKit
1. **Import** the `.glb` with the Import Tool. Your actions become entries in
   the `.anims` file, replacing the template's pose data.
2. In the `.workspot`, find `workspotTree` > `finalAnimsets` and make sure the
   entries name your animations. Delete entries for rigs you don't use.
3. Right-click the `.anims` and `.workspot` > **Convert to JSON**, then run:
   ```
   python tools/check_names.py "mod/bin/x64/plugins/cyber_engine_tweaks/mods/AppearanceMenuMod/Collabs/Custom Poses/my_pose_pack.lua" path\to\poses.anims.json path\to\poses.workspot.json
   ```
4. **Pack** the project. WolvenKit writes an `.archive` to `archive/pc/mod/`
   in your game folder (or use Install to Game).

### 5. Edit the AMM .lua
Open `my_pose_pack.lua` and set:
- `modder`: your name
- `category`: the name you want in AMM's Poses tab
- `entity_path`: the `.ent` path from WolvenKit, with backslashes doubled
  (`base\\yourname\\my_pose_pack\\poses.ent`)
- `anims`: your pose names under the right rig key. The valid keys are
  `Woman Average`, `Man Average`, `Man Massive`, `Big`, `Fat`, `Child`,
  `Player Woman` and `Player Man`, and they're case- and space-sensitive.

Copy the `mod/` folder's contents into your Cyberpunk install folder.

### 6. Test
Start the game > CET overlay (`~`) > AMM > **Poses** tab > find your category >
pick a pose for V or a spawned NPC whose body matches the rig.

## When it doesn't work
- **Pose missing from AMM:** the `.lua` didn't load. Check the rig key spelling,
  then check `AppearanceMenuMod/AMM.log` / the CET console for errors.
- **Pose listed but V/NPC doesn't move:** a name mismatch (run `check_names.py`),
  a wrong `entity_path`, or the `.ent` still pointing at the template workspot.
- **Pose looks broken or twisted:** the pose was made on a different rig
  (e.g. a man pose played on a woman_base NPC).
- **Renamed a pose and AMM still shows the old one:** AMM caches poses in its
  database. Use AMM's settings to reset/refresh, or reinstall AMM's database.

## References
- RED Modding wiki: *Creating Animations: Poses for V & NPCs*, *Poses/Animations:
  make your own*, *AMM: Collab anims/poses* (wiki.redmodding.org)
- AMM's own template: `AppearanceMenuMod/Collabs/Custom Poses/pose_template.lua`
