import bpy
from bpy.props import IntProperty, StringProperty, PointerProperty, BoolProperty
from bpy.types import PropertyGroup
from bpy.app.handlers import persistent

bl_info = {
    "name":     "3Dcam engine custom properties helper",
    "author":   "Schnappy",
    "blender":  (2,79,0),
    "category": "Property helper",    
    "version":  (0,0,1),
    "location": "3D view > Object",
    "location": "Properties panel > Data",
    "description":  "Set/Unset/Copy flags easily"
}
# Based on https://blog.hamaluik.ca/posts/dynamic-blender-properties by Kenton Hamaluik
bpy.propertyGroupLayouts = {
    "Flags": [
            { "name": "isAnim",      "type": "boolean" },
            { "name": "isProp",      "type": "boolean" }, 
            { "name": "isRigidBody", "type": "boolean" }, 
            { "name": "isStaticBody","type": "boolean" }, 
            { "name": "isRound",     "type": "boolean" }, 
            { "name": "isPrism",     "type": "boolean" }, 
            { "name": "isActor",     "type": "boolean" }, 
            { "name": "isLevel",     "type": "boolean" }, 
            { "name": "isWall",      "type": "boolean" }, 
            { "name": "isBG",        "type": "boolean" }, 
            { "name": "isSprite",    "type": "boolean" }, 
            { "name": "isLerp",      "type": "boolean" }
        ],
    "Others": [
            { "name": "mass",        "type": "int" }
        ]
    }
# store keymaps here to access after registration
addon_keymaps = []                    
bpy.samplePropertyGroups = {}
last_selection = []
store_att_names = []

def getActiveObjProps(active_obj):
    object_custom_props = [prop for prop in store_att_names if prop in active_obj.data]
    return object_custom_props

def menu_func(self, context):
    self.layout.operator(copyCustomPropToSelection.bl_idname)

def copyCustomProps(context):
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

def updateCustomProps(self, context):
    global last_selection
    global store_att_names
    for att in store_att_names:
        if (att in last_selection.Flags): # and last_selection.Flags[att] :
            if ( att not in last_selection.data or 
                last_selection.Flags[att] != last_selection.data[att] ):
                last_selection.data[att] = last_selection.Flags[att]
        if (att in last_selection.Others):
            if ( att not in last_selection.data or 
                last_selection.Others[att] != last_selection.data[att] ):
                last_selection.data[att] = last_selection.Others[att]
@persistent
def selection_callback(scene):
    global last_selection
    global store_att_names
    if bpy.context.active_object != last_selection:
        last_selection = bpy.context.active_object
        for groupName, attributeDefinitions in bpy.propertyGroupLayouts.items():
            # build the attribute dictionary for this group
            attributes = {}
            for attributeDefinition in attributeDefinitions:
                attType = attributeDefinition['type']
                attName = attributeDefinition['name']
                store_att_names.append(attName)
                value = 0
                if last_selection:
                    if attName in last_selection.data:
                        value = last_selection.data[attName]
                if attType == 'boolean':
                    print(attName + ":" + str(value))
                    attributes[attName] = BoolProperty(name=attName, default=value, update=updateCustomProps )
                elif attType == 'int':
                    attributes[attName] = IntProperty(name=attName, default=value, update=updateCustomProps)
                elif attType == 'string':
                    attributes[attName] = StringProperty(name=attName, default=value, update=updateCustomProps)
                else:
                    raise TypeError('Unsupported type (%s) for %s on %s!' % (attType, attName, groupName))
            # now build the property group class
            propertyGroupClass = type(groupName, (PropertyGroup,), attributes)
            # register it with Blender
            bpy.utils.register_class(propertyGroupClass)
            # apply it to all Objects
            setattr(bpy.types.Object, groupName, PointerProperty(type=propertyGroupClass))
            # store it for later
            bpy.samplePropertyGroups[groupName] = propertyGroupClass

class copyCustomPropToSelection(bpy.types.Operator):
    """Copy last selected object's custom properties to other selected objects"""
    bl_idname = "object.copy_custom_properties"
    bl_label = "Copy custom properties to selection"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        copyCustomProps(context)
        return {'FINISHED'}
        
class customPropsPanel(bpy.types.Panel):
    bl_label = "3D Cam engine custom properties"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"

    def draw(self, context):
        layout = self.layout
        obj = context.object
        # use our layout definition to dynamically create our panel items
        for groupName, attributeDefinitions in sorted(bpy.propertyGroupLayouts.items()):
            # get the instance of our group
            # dynamic equivalent of `obj.samplePropertyGroup` from before
            propertyGroup = getattr(obj, groupName)
            # start laying this group out
            col = layout.column_flow(columns=2)
            col.label(groupName)
            i = 0
            # loop through all the attributes and show them
            for attributeDefinition in attributeDefinitions:
                if i == len(attributeDefinitions)/2:
                    col.label("")
                col.prop(propertyGroup, attributeDefinition["name"])
                i += 1
            # draw a separation between groups
            layout.separator()

def register():
    # register the panel class
    bpy.utils.register_class(customPropsPanel)
    bpy.app.handlers.scene_update_post.clear()
    bpy.app.handlers.scene_update_post.append(selection_callback)
    # copy helper
    bpy.utils.register_class(copyCustomPropToSelection)
    bpy.types.VIEW3D_MT_object.append(menu_func)
    # shortcut
    wm = bpy.context.window_manager
    km = wm.keyconfigs.addon.keymaps.new(name='Object Mode', space_type='EMPTY')
    kmi = km.keymap_items.new(copyCustomPropToSelection.bl_idname, 'P', 'PRESS', ctrl=False, shift=True)
    # ~ kmi.properties.total = 4
    addon_keymaps.append((km, kmi))

def unregister():
    # unregister the panel class
    bpy.utils.unregister_class(customPropsPanel)
    # unregister our components
    try:
        for key, value in bpy.samplePropertyGroups.items():
            delattr(bpy.types.Object, key)
            bpy.utils.unregister_class(value)
    except UnboundLocalError:
        pass
    bpy.samplePropertyGroups = {}
    # copy helper
    bpy.utils.unregister_class(copyCustomPropToSelection)
    bpy.types.VIEW3D_MT_object.remove(menu_func)
    # handle the keymap
    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
    addon_keymaps.clear()

if __name__ == "__main__":
    register()
