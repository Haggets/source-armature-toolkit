# Valve Developer Toolkit
Blender plugin focused on bringing a variety of functions to fasten the workflow on working with Valve armatures, including both the normal and SFM type armatures.

## List of functions

### Armature renaming
Due to how the way the Source armature bones are named, including the "L" and "R" in the middle of the name rather than in the beginning or the end, it makes it so Blender is unable to detect the bones as pairs, which render any kind of symmetry option useless, including weight painting and posing.

This function allows for the position of the "L" and "R" to be temporarily placed after the name of the bone so it can be detected by Blender as pairs, allowing users to work smarter and faster instead of having to painfully mirror everything manually.

Remember to revert the name change before exporting.

### Constraint Symmetry
As mentioned previously, the way the bones are named disallow for symmetry, so naturally it is easy to assume that just by changing the placement of the "L" and "R" will allow for bone symmetry which will also allow for reshaping of the armature for characters that do not fit the standard body type. However, another quirk with the armatures that symmetry messes up is that opposite sides of the armature have different roll values (In a normal armature, those values are the same but one is positive and the other is negative), which completely mess up the bones on the other side if the pose is applied with those roll values changed.

This function adds constraints to the opposite side of the armature that allow for it to follow the other side while keeping corrected roll values, making the process a lot faster.

### Weight Armatures
Yet another quirk of the Source armature is that bones are not connected to eachother, instead, they're in "bubbles", and parented without connection, which is fine when animating it, but when you're building the vertex weights for a new character with said armature, the weights will be strangely distributed due to the bones not covering the actual length of the character, requiring a lot of manual tweaking that wouldn't be required with a normal armature.

This function procedurally creates a weight armature that connects all the bones it finds in a way that allows for a more convenient automatic vertex weighting, requiring less tweaking overall.

### Inverse Kinematics (Simple IK)
In a connected armature, when you try moving a bone that has a parent, it'll instead rotate it using the parent's tail as a pivot point, however, as the Source armature is not connected, it instead allows for the bone to actually move from its position, which in most cases is not the intended effect if you're trying to animate a realistic moving character.

This function simply adds IK constraints to the character's limbes (Hands, Feet), allowing for easier manipulation of them, which is ideal for simple animations.

### Inverse Kinematics (Advanced IK)
This functions is a heavy duty version of the previous function, instead creating a procedural armature with Rigify and retargetting the Source armature onto it, allowing for the usage of an animation ready armature, giving animators a WAY easier time animating characters, and allowing for a lot more flexibility overall.

Remember to bake the animation onto the Source armature before exporting, otherwise the animation will not show up in the game, that's due to it only following another armature's actions, it is not doing anything on its own.