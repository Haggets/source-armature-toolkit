[![discord](https://img.shields.io/discord/693987167210438656.svg?style=flat&label=Discord&logo=discord&color=7289DA&json?)](https://discord.gg/kH99XSU)

# Source Armature Toolkit
Flexible multi-purpose Blender plugin focused on fastening the workflow of working with Source armatures.

# How to Install

The plugin is installed like any other; In the Blender preferences > Addons, install, and select the plugin in whatever folder you have it in.

![Addons page](/img/Install1.png)

![Plugin in Downloads folder](/img/Install2.png)

After enabling the plugin, a new panel will show up in the Object category.

![Plugin in Downloads folder](/img/PluginPanel.png)

You can either select an already created armature, or generate one from the list of games available, with additional parameters for each, and with the option between creating playermodel armatures and viewmodel armatures.
## List of functions

After selecting an armature, the following will happen.

### Bone Organization
Every bone in the armature will be divided by layer and color, giving each bone type a distinctive look as well as giving you the option of hiding or isolating certain bone types if other bone types are getting in your way.

* Layer 0 = Central bones
* Layer 1 = Left hand
* Layer 2 = Right hand
* Layer 3 = Left leg
* Layer 4 = Right Leg
* Layer 5 = Helper bones
* Layer 6 = Attachment bones
* Layer 7 = Weapon bones
* Layer 8 = Other bones
* Layer 9 = Custom bones

### Helper Bone Linking
Common helper bones (Such as the wrist, ulna, elbow, knee...) will be automatically setup in order to behave just like they would in engine, allowing you to visualize an accurate deformation of the character and giving more flexibility when animating them.

## Operations

Current list of functions available.

### Armature Rename
This function temporarily changes the position of side differentiators (L/R) to the end of the name so Blender is able to detect bones as pairs, allowing the use of symmetry options for modes such as weight painting, which otherwise would not be available (Since Blender only detects bones as pairs if the side differentiator is at the beginning or end of the name).

### Constraint Symmetry
Adds location and rotation constraints to the opposite side of a bone pair to allow mirrored armature reproportioning, keeping corrected roll values so animations play correctly on the edited armature in engine. Serves as a workaround to the pose symmetry options if using the Armature Rename function (Due to how Source doesn't use mirrored roll values, the rotation between 2 pairs will be misaligned without the use of constraints).

### Weight Armatures
Procedurally generates a duplicate of the selected armature with all the deformation bones connected, placing helper bones in their correct position too, and compensating if any are missing, allowing for a more convenient automatic vertex weighting and requiring less tweaking.

### Rigify Retarget
Procedurally generates a duplicate of the selected armature with all the important deformation bones connected and with Rigify parameters defined, allowing the creation (Or further parameter modification to your liking) of an animation ready armature which the original armature is retargeted to, meaning you can easily animate a character or viewmodel without ever having to touch the original armature and with the ability of being exportable back into Source, giving the user a lot more flexibility than with the standard armature (Since all the bones in the Rigify armature work, including the tweak bones). Additionally, if a character is defined, facial bones will be added onto the armature (Depending on which characters expressions are available), allowing you to modify a character's expressions within the armature without having to touch any sliders, although this is not exportable.
