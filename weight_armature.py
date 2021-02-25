import bpy
from .functions import generate_armature

def weight_armature(action): #Creates duplicate armature for more spread out weighting
        
    generate_armature('weight', action)
    print("Weight armature created!")
