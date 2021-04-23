[![discord](https://img.shields.io/discord/693987167210438656.svg?style=flat&label=Discord&logo=discord&color=7289DA&json?)](https://discord.gg/kH99XSU)

# Valve Armature Toolkit
Blender plugin focused on bringing a variety of functions to fasten the workflow of working with Valve armatures. (This does not include SFM armatures)

## List of functions

After selecting an armature, the following will happen...

### Bone Organization
Every bone in the armature will be divided by group, moving each group to their corresponding bone layer as well as giving them a specific color to make each group stand out, all of which can be hidden individually by simply deselecting their bone layer.

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

### Procedural Bone Linking
Every helper bone with a function (Such as the wrist, ulna, elbow, knee...) will be linked to their driver bone just like it would in Source, allowing to visualize their deformation as well as allowing more flexible animation of the character.

## Operations

### Armature renaming
Due to how the way the Source armature bones are named (L/R not at the end or start, but at the middle of the name), Blender is unable to detect bones as pairs, disabling any kind of symmetry options.

This function temporarily changes the position of L/R to the end of the name so Blender is able to detect bones as pairs, allowing the use of symmetry options for workloads such as weight painting, saving yourself the trouble of having to do work twice.

### Constraint Symmetry
Adds constraints to the opposite side of a pair to allow mirrored armature reproportioning, keeping corrected roll values meaning that animations will play correctly on the reproportioned armature.

### Weight Armatures
Procedurally generates a duplicate of the selected armature with all the bones (That should deform) connected, and helper bones in their correct position, compensating if any are missing, allowing for a more convenient automatic vertex weighting, requiring less tweaking.

### Rigify Retarget
Procedurally generates a duplicate of the selected armature with all the important bones connected and with Rigify parameters defined, allowing the creation (Or further parameter modification to your liking) of an animation ready armature which the original armature is retargeted to, meaning you can easily animate a character or viewmodel without ever having to touch the original armature and with the ability of being exportable back into Source, giving the user a lot of flexibility (Since all the bones in the Rigify armature work, including the tweak bones whose motion can also be exported). Additionally, you also have the ability to modify a character's facial flexes within the armature in a really intuitive way (Although not exportable)

# How to Install

The plugin is installed like any other, you go to the Blender preferences, Addons, click on install, and select the plugin

![Addons page](/img/Install1.png)

![Plugin in Downloads folder](/img/Install2.png)

After enabling the plugin, a new panel will show up in the Armature Data tab (When selecting an armature)

![Plugin in Downloads folder](/img/PluginPanel.png)

And now you're free to select the armature you want to modify. The operations you use will only apply to the armature you're currently selecting. Armatures generated from that armature will not show up in the armature selection list to avoid it getting cluttered.