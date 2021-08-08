import bpy 

bl_info = {
    "name":     "Copy custom properties",
    "author":   "Schnappy",
    "blender":  (2,79,0),
    "category": "Property helper",    
    "version":  (0,0,1),
    "location": "3D view > Object",
    "description":  "Copy custom property from last selected object to other objects in selection"
}
# store keymaps here to access after registration
addon_keymaps = []
custom_props = [    'isAnim',
                    'isProp',
                    'isRigidBody',
                    'isStaticBody',
                    'isRound',
                    'isPrism',
                    'isActor',
                    'isLevel',
                    'isWall',
                    'isBG',
                    'isSprite',
                    'mass',
                    'restitution',
                    'lerp'
                    ]

def getActiveObjProps(active_obj):
    object_custom_props = [prop for prop in custom_props if prop in active_obj.data]
    return object_custom_props

def main(context):
    # get active object
    active_obj = bpy.context.active_object
    # get active object's custom properties
    active_obj_custom_props = getActiveObjProps(active_obj)
    # get selected objects
    selection = bpy.context.selected_objects
    # discriminates against active_obj
    selection = [obj for obj in selection if obj != active_obj]
    # for each object that's not active object, add custom prop
    for obj in selection:
        for prop in active_obj_custom_props:
            obj.data[prop] = active_obj.data[prop]

class copyCustomPropToSelection(bpy.types.Operator):
    """Copy last selected object's custom properties to other selected objects"""
    bl_idname = "object.copy_custom_properties"
    bl_label = "Copy custom properties to selection"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def menu_func(self, context):
    self.layout.operator(copyCustomPropToSelection.bl_idname)

def register():
    bpy.utils.register_class(copyCustomPropToSelection)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    
    # shortcut
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')

    kmi = km.keymap_items.new(copyCustomPropToSelection.bl_idname, 'P', 'PRESS', ctrl=False, shift=True)
    # ~ kmi.properties.total = 4
    addon_keymaps.append((km, kmi))

def unregister():
    bpy.utils.unregister_class(copyCustomPropToSelection)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
