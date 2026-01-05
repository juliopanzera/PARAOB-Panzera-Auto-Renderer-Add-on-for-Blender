bl_info = {
    "name": "Panzera Auto-Renderer Add-on for Blender",
    "author": "Júlio Panzera-Gonçalves",
    "version": (1, 33),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Render > Panzera Auto-Renderer Add-on for Blender",
    "description": "Renders selected standardized viewpoints (front, back, left, right, top, bottom and oblique) of 3D models with customization options",
    "category": "Render",
}

import bpy
import os
import mathutils
from bpy.props import (
    StringProperty, BoolProperty, IntProperty, EnumProperty,
    FloatProperty, FloatVectorProperty
)
from bpy.types import Operator, Panel, PropertyGroup

# =========================================================
# PROPERTIES
# =========================================================

class RenderViewsProperties(PropertyGroup):

    use_transparent_bg: BoolProperty(name="Transparent Background", default=False)

    background_color: FloatVectorProperty(
        name="Background Color",
        subtype='COLOR',
        size=4,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0, 1.0)
    )

    resolution_presets: EnumProperty(
        name="Presets",
        items=[
            ('720', "1280 x 720 (HD)", ""),
            ('SQ1', "1080 x 1080 (Square 1:1)", ""),
            ('1080', "1920 x 1080 (Full HD)", ""),
            ('SQ2', "2048 x 2048 (Square 2K)", ""),
            ('4K', "3840 x 2160 (4K UHD)", ""),
            ('8K', "7680 x 4320 (8K)", ""),
            ('CUST', "Custom", "")
        ],
        default='1080'
    )

    render_width: IntProperty(name="Width", default=1920, min=1)
    render_height: IntProperty(name="Height", default=1080, min=1)

    light_type: EnumProperty(
        name="Light Type",
        items=[
            ('SUN', "Sun", ""),
            ('POINT', "Point", ""),
            ('AREA', "Area", ""),
            ('SPOT', "Spot", "")
        ],
        default='SUN'
    )

    light_energy: FloatProperty(name="Light Intensity", default=1.0, min=0.0, max=10.0)

    light_color: FloatVectorProperty(
        name="Light Color",
        subtype='COLOR',
        size=3,
        min=0.0,
        max=1.0,
        default=(1.0, 1.0, 1.0)
    )

    camera_distance_front: FloatProperty(name="Front", default=5.0, min=0.1)
    camera_distance_back: FloatProperty(name="Back", default=5.0, min=0.1)
    camera_distance_left: FloatProperty(name="Left", default=5.0, min=0.1)
    camera_distance_right: FloatProperty(name="Right", default=5.0, min=0.1)
    camera_distance_top: FloatProperty(name="Top", default=5.0, min=0.1)
    camera_distance_bottom: FloatProperty(name="Bottom", default=5.0, min=0.1)
    camera_distance_perspective: FloatProperty(name="Oblique", default=3.0, min=0.1)

    output_path: StringProperty(
        name="Output Folder",
        subtype='DIR_PATH',
        default=os.path.join(os.path.expanduser("~"), "Desktop", "Panzera Auto-Renderer Add-on for Blender")
    )

    render_front: BoolProperty(name="Front", default=True)
    render_back: BoolProperty(name="Back", default=True)
    render_left: BoolProperty(name="Left", default=True)
    render_right: BoolProperty(name="Right", default=True)
    render_top: BoolProperty(name="Top", default=True)
    render_bottom: BoolProperty(name="Bottom", default=True)
    render_perspective: BoolProperty(name="Oblique", default=True)

    show_info_section: BoolProperty(default=False)
    show_output_settings: BoolProperty(default=True)
    show_light_settings: BoolProperty(default=True)
    show_camera_settings: BoolProperty(default=True)
    show_views_to_render: BoolProperty(default=True)
    show_background_settings: BoolProperty(default=True)
    show_before_render_section: BoolProperty(default=False)
    show_resolution_settings: BoolProperty(default=True)

# =========================================================
# RESOLUTION PRESET OPERATOR
# =========================================================

class RENDER_OT_apply_resolution_preset(Operator):
    bl_idname = "render.apply_resolution_preset"
    bl_label = "Apply Preset"

    def execute(self, context):
        props = context.scene.render_views_props

        presets = {
            '720': (1280, 720),
            'SQ1': (1080, 1080),
            '1080': (1920, 1080),
            'SQ2': (2048, 2048),
            '4K': (3840, 2160),
            '8K': (7680, 4320)
        }

        if props.resolution_presets in presets:
            props.render_width, props.render_height = presets[props.resolution_presets]

        return {'FINISHED'}

# =========================================================
# RESET TO DEFAULTS OPERATOR
# =========================================================

class RENDER_OT_reset_defaults(Operator):
    bl_idname = "render.reset_defaults"
    bl_label = "RESET TO DEFAULTS"
    bl_description = "Reset all settings to their default values"

    def execute(self, context):
        props = context.scene.render_views_props

        props.use_transparent_bg = False
        props.background_color = (1.0, 1.0, 1.0, 1.0)
        props.resolution_presets = '1080'
        props.render_width = 1920
        props.render_height = 1080

        props.light_type = 'SUN'
        props.light_energy = 1.0
        props.light_color = (1.0, 1.0, 1.0)

        props.camera_distance_front = 5.0
        props.camera_distance_back = 5.0
        props.camera_distance_left = 5.0
        props.camera_distance_right = 5.0
        props.camera_distance_top = 5.0
        props.camera_distance_bottom = 5.0
        props.camera_distance_perspective = 3.0

        props.output_path = os.path.join(os.path.expanduser("~"), "Desktop", "Panzera Auto-Renderer Add-on for Blender")

        props.render_front = True
        props.render_back = True
        props.render_left = True
        props.render_right = True
        props.render_top = True
        props.render_bottom = True
        props.render_perspective = True

        props.show_info_section = False
        props.show_output_settings = True
        props.show_light_settings = True
        props.show_camera_settings = True
        props.show_views_to_render = True
        props.show_background_settings = True
        props.show_before_render_section = False
        props.show_resolution_settings = True

        self.report({'INFO'}, "Settings reset to defaults")
        return {'FINISHED'}

# =========================================================
# WORLD BACKGROUND CONFIGURATION
# =========================================================

def setup_world_background(color=(1,1,1,1), use_transparent=False):
    world = bpy.context.scene.world
    if not world:
        world = bpy.data.worlds.new("World")
        bpy.context.scene.world = world

    world.use_nodes = True
    nodes = world.node_tree.nodes
    links = world.node_tree.links

    nodes.clear()
    output_node = nodes.new(type='ShaderNodeOutputWorld')

    bg_node = nodes.new(type='ShaderNodeBackground')
    if use_transparent:
        bg_node.inputs['Color'].default_value = (0,0,0,1)
        bg_node.inputs['Strength'].default_value = 0
        bpy.context.scene.render.film_transparent = True
    else:
        bg_node.inputs['Color'].default_value = color
        bg_node.inputs['Strength'].default_value = 1.0
        bpy.context.scene.render.film_transparent = False

    links.new(bg_node.outputs[0], output_node.inputs['Surface'])

# =========================================================
# RENDER OPERATOR
# =========================================================

class RENDER_OT_views(Operator):
    bl_idname = "render.views"
    bl_label = "RENDER VIEWPOINTS"
    bl_description = "Render selected standardized viewpoints of the model"

    def execute(self, context):
        props = context.scene.render_views_props
        scene = context.scene

        raw_name = bpy.path.display_name_from_filepath(bpy.data.filepath) if bpy.data.filepath else "untitled"
        os.makedirs(props.output_path, exist_ok=True)

        scene.render.engine = 'CYCLES'
        scene.cycles.samples = 128

        scene.render.resolution_x = max(1, int(props.render_width))
        scene.render.resolution_y = max(1, int(props.render_height))
        scene.render.resolution_percentage = 100

        camera_created = False
        cam_data_created = None
        if "Camera" not in bpy.data.objects:
            cam_data = bpy.data.cameras.new(name="Camera")
            cam_obj = bpy.data.objects.new("Camera", cam_data)
            context.collection.objects.link(cam_obj)
            camera_created = True
            cam_data_created = cam_data
        else:
            cam_obj = bpy.data.objects["Camera"]

        scene.camera = cam_obj

        light_created = False
        light_data_created = None
        if "Light" not in bpy.data.objects:
            light_data = bpy.data.lights.new(name="Light", type=props.light_type)
            light_obj = bpy.data.objects.new("Light", light_data)
            context.collection.objects.link(light_obj)
            light_created = True
            light_data_created = light_data
        else:
            light_obj = bpy.data.objects["Light"]

        light_obj.data.type = props.light_type
        light_obj.location = (5, -5, 5)
        light_obj.data.energy = props.light_energy
        try:
            light_obj.data.color = props.light_color
        except:
            pass
        light_obj.data.shadow_soft_size = 1.0

        views = {
            "1_front":   (props.render_front,  (0, -props.camera_distance_front, 0)),
            "2_back":    (props.render_back,   (0,  props.camera_distance_back,  0)),
            "3_left":    (props.render_left,   (-props.camera_distance_left, 0, 0)),
            "4_right":   (props.render_right,  ( props.camera_distance_right, 0, 0)),
            "5_top":     (props.render_top,    (0, 0, props.camera_distance_top)),
            "6_bottom":  (props.render_bottom, (0, 0, -props.camera_distance_bottom)),
            "7_oblique": (props.render_perspective, (
                props.camera_distance_perspective,
                -props.camera_distance_perspective,
                props.camera_distance_perspective
            )),
        }

        model_center = mathutils.Vector((0,0,0))

        created_objects = []

        for view_name, (enabled, cam_location) in views.items():
            if not enabled:
                continue

            cam_obj.location = cam_location
            cam_obj.data.lens = 20
            direction = model_center - cam_obj.location
            cam_obj.rotation_euler = direction.to_track_quat('-Z', 'Y').to_euler()

            # Configura background via World node
            setup_world_background(color=props.background_color, use_transparent=props.use_transparent_bg)
            bg_plane_obj = None

            temp_light_data = bpy.data.lights.new(name=f"TempLightData_{view_name}", type=props.light_type)
            temp_light_obj = bpy.data.objects.new(f"TempLight_{view_name}", temp_light_data)
            context.collection.objects.link(temp_light_obj)
            created_objects.append(temp_light_obj)

            temp_light_obj.location = cam_location
            temp_light_obj.rotation_euler = cam_obj.rotation_euler
            temp_light_obj.data.energy = props.light_energy
            try:
                temp_light_obj.data.color = props.light_color
            except:
                pass
            temp_light_obj.data.shadow_soft_size = 1.0

            res_str = f"{scene.render.resolution_x}x{scene.render.resolution_y}"
            base_filename = f"{raw_name}_{view_name}_{props.light_type}_{res_str}"

            file_index = 1
            filepath = os.path.join(props.output_path, f"{base_filename}.png")
            while os.path.exists(filepath):
                filepath = os.path.join(props.output_path, f"{base_filename}_{file_index}.png")
                file_index += 1

            scene.render.filepath = filepath
            bpy.ops.render.render(write_still=True)

            try:
                if temp_light_obj.name in bpy.data.objects:
                    bpy.data.objects.remove(temp_light_obj, do_unlink=True)
                if temp_light_data.name in bpy.data.lights:
                    bpy.data.lights.remove(temp_light_data)
            except Exception:
                pass

        try:
            if camera_created:
                if scene.camera == cam_obj:
                    scene.camera = None
                if cam_obj.name in bpy.data.objects:
                    bpy.data.objects.remove(cam_obj, do_unlink=True)
                if cam_data_created and cam_data_created.name in bpy.data.cameras:
                    bpy.data.cameras.remove(cam_data_created)
        except Exception:
            pass

        try:
            if light_created:
                if light_obj.name in bpy.data.objects:
                    bpy.data.objects.remove(light_obj, do_unlink=True)
                if light_data_created and light_data_created.name in bpy.data.lights:
                    bpy.data.lights.remove(light_data_created)
        except Exception:
            pass

        def draw_popup(self, context):
            self.layout.label(text="Rendering complete!")
        bpy.context.window_manager.popup_menu(draw_popup, title="Panzera Auto-Renderer", icon='RENDER_RESULT')

        self.report({'INFO'}, "Rendering complete!")

        return {'FINISHED'}

# =========================================================
# PERSONAL LINK OPERATOR
# =========================================================

class RENDER_OT_open_personal_link(Operator):
    bl_idname = "wm.open_personal_link"
    bl_label = "Visit Developer Page"

    def execute(self, context):
        import webbrowser
        webbrowser.open("http://lattes.cnpq.br/5054228929856492")
        return {'FINISHED'}

# =========================================================
# UI PANEL
# =========================================================

class RENDER_PT_views_panel(Panel):
    bl_label = "Panzera Auto-Renderer Add-on for Blender"
    bl_idname = "RENDER_PT_views_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Image Auto-Renderer'

    def draw(self, context):
        layout = self.layout
        props = context.scene.render_views_props

        layout.separator()
        layout.separator()

        # INFO SECTION
        box = layout.box()
        row = box.row()
        row.prop(props, "show_info_section", icon="TRIA_DOWN" if props.show_info_section else "TRIA_RIGHT", emboss=False, text="ADD-ON INFORMATION", toggle=True)

        if props.show_info_section:
            col = box.column(align=True)
            col.label(text=f"Name: {bl_info.get('name', 'Unknown')}")
            col.label(text="Description: Renders selected standardized viewpoints of 3D models.")
            col.label(text=f"Version: {'.'.join(map(str, bl_info.get('version', (0, 0))))}")
            col.label(text=f"Copyright © 2025, {bl_info.get('author', 'Unknown')}")
            col.separator()
            col.separator()
            col.separator()
            col.separator()
            col.operator("wm.open_personal_link", text="Visit Developer Page", icon='LINKED')

        layout.separator()
        layout.separator()

        # BEFORE RENDER SECTION
        box = layout.box()
        row = box.row()
        row.prop(props, "show_before_render_section", icon="TRIA_DOWN" if props.show_before_render_section else "TRIA_RIGHT", emboss=False, text="BEFORE RENDERING, MAKE SURE TO:", toggle=True)

        if props.show_before_render_section:
            box.label(text="• center the 3D model at the origin (0, 0, 0).")
            box.label(text="• correctly orient the 3D model on the x, y and z axes (-Y axis corresponds to the front viewpoint).")
            box.label(text="• delete any lights or cameras present in the scene (so they don't conflict with the ones that will be automatically added by the add-on).")
            box.label(text="• delete all keyframes associated with changing the position, rotation or size of an object (the presence of keyframes may result in misplaced objects).")
            box.label(text="• adjust the camera distance (incorrect camera distances can result in renders with too small, too large or cropped 3D models).")
            box.label(text="• adjust the light settings (sun is the default type of light and intensities superior than 1.5 may result in high exposure).")

        layout.separator()
        layout.separator()

        # OUTPUT FOLDER SECTION
        box = layout.box()
        row = box.row()
        row.prop(props, "show_output_settings", icon="TRIA_DOWN" if props.show_output_settings 
                 else "TRIA_RIGHT", emboss=False, text="OUTPUT FOLDER", toggle=True)

        if props.show_output_settings:
            box.prop(props, "output_path")

        layout.separator()
        layout.separator()

        # RESOLUTION SECTION
        box = layout.box()
        row = box.row()
        row.prop(props, "show_resolution_settings", icon="TRIA_DOWN" if props.show_resolution_settings else "TRIA_RIGHT", emboss=False, text="RENDERING RESOLUTION", toggle=True)

        if props.show_resolution_settings:
            col = box.column(align=True)
            row = col.row(align=True)
            row.prop(props, "resolution_presets", text="Preset")
            
            col.separator()
            
            row = col.row(align=True)
            row.operator("render.apply_resolution_preset", text="Apply")

            col.separator()
            col.separator()
            col.separator()
            col.separator()
            col.prop(props, "render_width")
            col.prop(props, "render_height")
            col.separator()
            col.separator()
            col.separator()
            col.separator()
            col.label(text="TIP: set custom values and choose 'Custom' preset to keep them.")
            col.label(text="ATTENTION: Higher resolutions require a lot of memory and time to perform the rendering task.")

        layout.separator()
        layout.separator()

        # LIGHT SETTINGS
        box = layout.box()
        row = box.row()
        row.prop(props, "show_light_settings", icon="TRIA_DOWN" if props.show_light_settings else "TRIA_RIGHT", emboss=False, text="LIGHT SETTINGS", toggle=True)

        if props.show_light_settings:
            col = box.column(align=True)
            col.prop(props, "light_type")
            col.separator()
            col.separator()
            col.separator()
            col.separator()
            col.prop(props, "light_energy")
            col.separator()
            col.separator()
            col.separator()
            col.separator()
            col.prop(props, "light_color")

        layout.separator()
        layout.separator()

        # CAMERA SETTINGS
        box = layout.box()
        row = box.row()
        row.prop(props, "show_camera_settings", icon="TRIA_DOWN" if props.show_camera_settings else "TRIA_RIGHT", emboss=False, text="CAMERA DISTANCE", toggle=True)

        if props.show_camera_settings:
            col = box.column(align=True)
            col.prop(props, "camera_distance_front")
            col.prop(props, "camera_distance_back")
            col.prop(props, "camera_distance_left")
            col.prop(props, "camera_distance_right")
            col.prop(props, "camera_distance_top")
            col.prop(props, "camera_distance_bottom")
            col.prop(props, "camera_distance_perspective")

        layout.separator()
        layout.separator()

        # VIEWPOINTS TO RENDER
        box = layout.box()
        row = box.row()
        row.prop(props, "show_views_to_render", icon="TRIA_DOWN" if props.show_views_to_render else "TRIA_RIGHT", emboss=False, text="VIEWPOINTS TO RENDER", toggle=True)

        if props.show_views_to_render:
            row = box.row(align=True)
            col1 = row.column(align=True)
            col2 = row.column(align=True)
            col1.prop(props, "render_front")
            col1.prop(props, "render_back")
            col1.prop(props, "render_left")
            col1.prop(props, "render_right")
            col2.prop(props, "render_top")
            col2.prop(props, "render_bottom")
            col2.prop(props, "render_perspective")

        layout.separator()
        layout.separator()

        # BACKGROUND SETTINGS
        box = layout.box()
        row = box.row()
        row.prop(props, "show_background_settings", icon="TRIA_DOWN" if props.show_background_settings else "TRIA_RIGHT", emboss=False, text="BACKGROUND SETTINGS", toggle=True)

        if props.show_background_settings:
            col = box.column(align=True)
            col.prop(props, "use_transparent_bg")
            if not props.use_transparent_bg:
                col.separator()
                col.separator()
                col.separator()
                col.separator()
                col.prop(props, "background_color")
                col.separator()
                col.separator()
                col.separator()
                col.separator()
                col.label(text="ATTENTION: changing the background color may affect 3D model's color too.")

        layout.separator()
        layout.separator()
        
        row = layout.row()
        row.scale_y = 2.0
        row.operator("render.reset_defaults", text="RESET SETTINGS", icon="FILE_REFRESH")
        
        layout.separator()

        row = layout.row()
        row.scale_y = 2.5
        row.operator("render.views", text="RENDER SELECTED VIEWPOINTS", icon="RENDER_RESULT")
        

# =========================================================
# REGISTER
# =========================================================

classes = [
    RenderViewsProperties,
    RENDER_OT_apply_resolution_preset,
    RENDER_OT_views,
    RENDER_OT_reset_defaults,
    RENDER_OT_open_personal_link,
    RENDER_PT_views_panel,
]

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    bpy.types.Scene.render_views_props = bpy.props.PointerProperty(type=RenderViewsProperties)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    del bpy.types.Scene.render_views_props

if __name__ == "__main__":
    register()
