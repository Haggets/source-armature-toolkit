import bpy
from .utils import generate_armature

def weight_armature(action): #Creates duplicate armature for more spread out weighting
        
    generate_armature('weight', action)

    if action == 0:
        print("Weight armature created!")
    else:
        print("Weight armature deleted")
