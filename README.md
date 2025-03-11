# BlendHeck

This is a Blender Addon to work with Vivify (for now), a Beat Saber mod made by [Aeroluna](https://github.com/aeroluna)

I work on this addon on my **free time**, so don't expect it to be perfect right now (as it is the first release).

Feel free to open an issue if you find a bug or have a suggestion, I will try to work on it when I have time.

**Please take time to read the whole [wiki](https://github.com/M4NIK0/BlendHeck/wiki) if you are unsure about how to use the add-on.**

## Installation

Download the latest release from the [releases page](https://github.com/M4NIK0/BlendHeck) and install it in Blender:

```
Edit -> Preferences -> Add-ons -> Install from disk (from the top right corner)
Select the downloaded zip file -> Enable the Add-on (if not already enabled at install)
```

## Quick start

All documentation is available in the repo [wiki](https://github.com/M4NIK0/BlendHeck/wiki), but here is a quick start guide

In the main viewport, on the right, you will find a new panel called "Vivify".

The panel provides the following options:
- Add custom path data for the add-on to use for future export
- Export all paths from the scene to the map
- Export all paths from selected objects to the map
- Select the target map file
- Load the target map file (see all defined paths in pointsDefinitions)
- Save the target map file
- Enable/Disable save on blend file save (requires restart of Blender to take effect for now -_-)

### Path properties

This panel consists of the following properties for each object and their paths:

#### What kind of path should I use?

It depends on what you need, if you have a series of keyframes (you should read Blender documentation and play with it a bit if you don't know what keyframes are) you can use the "Keyframes" path, it will mark a series of keyframes (for a single property) as a path.

- Start frame/End frame: The range of frames to consider for the path
- Property: The property to consider for the path (Position/Rotation/Scale)
- Export: If the path should be exported to the map (it will not export or update anything if this is disabled)

If you use a curve or a complex path with some weird shape or some specific interpolation, you can use the "Curve/Custom" path and configure it, it will take a series of evenly spaced points from the curve and use them as a path.

- Start frame/End frame: The range of frames to consider for the path
- Steps: The number of points to take from the curve (more points means a more accurate path but also more points to process)
- Export: If the path should be exported to the map (it will not export or update anything if this is disabled)
- Export Position/Rotation/Scale: If the path should be exported for the given property (Position/Rotation/Scale)

For example, if you want to export a custom path/curve with only the position, you can disable the other properties.

### Map data

Once a map is loaded, you can manipulate (mostly see and delete for now) all pointsDefinitions in the map:

- Remove the selected path with the remove "X" button
- Preview the selected path with the "Preview" button (it will show the path in the 3D viewport)\
--> **PREVIEW IS NOT IMPLEMENTED YET AS WELL AS PATH EDIT** <--

#### Exporting paths

Once your paths are defined, you can export them to the currently loaded map file with the "Export all paths" (or "Export selected paths) button.

Once your paths are exported, you **must** save the map file with the "Save map file" button (or save the blend file if you have enabled the "Save on blend file save" option).

## Known issues

- The preview button is not implemented yet (*i'm lazy*, or simply work on my **free time**)
- The "Save on blend file save" option requires a restart of Blender to take effect (it's a limitation of the current implementation, maybe because *i'm dumb*)

## License

This add-on is licensed under the GNU General Public License v2.0 or later and is based on the Blender Add-on Template by Maddison Hellstrom.

## Credits

- [Aeroluna](https://github.com/aeroluna) (Vivify mod author)
- [Swifter](https://github.com/Swifter1243) (Remapper author and providing really useful information and examples)
