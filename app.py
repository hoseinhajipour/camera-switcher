bl_info = {
    "name": "Camera Switcher",
    "author": "hosein hajipour",
    "version": (1, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Camera Tools",
    "description": "Manage and animate multiple cameras with transitions.",
    "warning": "",
    "doc_url": "",
    "category": "Camera",
}

import bpy

# Property group to store camera switch data
class CameraSwitchItem(bpy.types.PropertyGroup):
    camera_name: bpy.props.StringProperty(name="Camera")
    start_frame: bpy.props.IntProperty(name="Start Frame", default=1, min=1)
    show_details: bpy.props.BoolProperty(name="Show Details", default=False)  # Toggle for collapsible state

# Panel to display the camera switch list
class VIEW3D_PT_CameraSwitcher(bpy.types.Panel):
    """Creates a Panel in the 3D view sidebar"""
    bl_label = "Camera Switcher"
    bl_idname = "VIEW3D_PT_camera_switcher"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Camera Tools"

    def draw(self, context):
        layout = self.layout
        scene = context.scene

        layout.label(text="Camera Switch List:")
        row = layout.row()
        row.operator("camera.append_selected", text="Append Camera")

        row = layout.row()
        row.operator("camera.create_from_view", text="Create Camera from View")

        # Draw each camera in a collapsible accordion
        for index, cam in enumerate(scene.camera_switch_list):
            box = layout.box()
            row = box.row()

            # Toggle button for collapsible state
            icon = "TRIA_DOWN" if cam.show_details else "TRIA_RIGHT"
            row.prop(cam, "show_details", icon=icon, text="", emboss=False)

            # Camera name
            row.label(text=cam.camera_name)

            # Expanded section
            if cam.show_details:
                col = box.column()
                col.prop(cam, "start_frame", text="Start Frame")

                row = box.row()
                row.operator("camera.set_active", text="Set Active").camera_name = cam.camera_name
                row.operator("camera.remove_camera", text="Remove").index = index
        
        layout.separator()
        layout.prop(scene, "transition_frames", text="Transition Frames")
        layout.operator("camera.generate_animation", text="Generate Animation")


# Operator to append selected cameras to the list
class CAMERA_OT_AppendSelected(bpy.types.Operator):
    bl_idname = "camera.append_selected"
    bl_label = "Append Selected Camera"

    def execute(self, context):
        scene = context.scene
        selected_cameras = [obj for obj in scene.objects if obj.type == 'CAMERA' and obj.select_get()]
        
        for cam in selected_cameras:
            item = scene.camera_switch_list.add()
            item.camera_name = cam.name
            item.start_frame = scene.frame_start

        self.report({'INFO'}, "Selected cameras appended!")
        return {'FINISHED'}


# Operator to create a camera from the current 3D view
class CAMERA_OT_CreateFromView(bpy.types.Operator):
    bl_idname = "camera.create_from_view"
    bl_label = "Create Camera from View"

    def execute(self, context):
        # Create a new camera
        new_camera = bpy.data.cameras.new(name="Camera_From_View")
        new_camera_obj = bpy.data.objects.new(name="Camera_From_View", object_data=new_camera)

        # Link the camera to the scene collection
        context.collection.objects.link(new_camera_obj)

        # Set the new camera as the active camera
        context.scene.camera = new_camera_obj

        # Align the camera to the current 3D view
        bpy.ops.view3d.camera_to_view()

        # Add the new camera to the camera switch list
        item = context.scene.camera_switch_list.add()
        item.camera_name = new_camera_obj.name
        item.start_frame = context.scene.frame_start

        self.report({'INFO'}, "Camera created from current view!")
        return {'FINISHED'}


# Operator to remove a camera from the list
class CAMERA_OT_RemoveCamera(bpy.types.Operator):
    bl_idname = "camera.remove_camera"
    bl_label = "Remove Camera"

    index: bpy.props.IntProperty()

    def execute(self, context):
        scene = context.scene
        scene.camera_switch_list.remove(self.index)
        self.report({'INFO'}, "Camera removed from the list")
        return {'FINISHED'}


# Operator to set active camera
class CAMERA_OT_SetActive(bpy.types.Operator):
    bl_idname = "camera.set_active"
    bl_label = "Set Active Camera"

    camera_name: bpy.props.StringProperty()

    def execute(self, context):
        scene = context.scene
        cam = scene.objects.get(self.camera_name)

        if cam and cam.type == 'CAMERA':
            scene.camera = cam
            self.report({'INFO'}, f"Active camera set to {self.camera_name}")
        else:
            self.report({'ERROR'}, "Camera not found!")
        
        return {'FINISHED'}


# Operator to generate camera animation with transition frames
class CAMERA_OT_GenerateAnimation(bpy.types.Operator):
    bl_idname = "camera.generate_animation"
    bl_label = "Generate Camera Animation"

    def execute(self, context):
        scene = context.scene
        transition_frames = scene.transition_frames

        if len(scene.camera_switch_list) == 0:
            self.report({'WARNING'}, "No cameras in the list!")
            return {'CANCELLED'}

        # Create or get the master camera
        if "Master_Camera" not in scene.objects:
            master_cam = bpy.data.objects.new("Master_Camera", bpy.data.cameras.new("Master_Camera"))
            scene.collection.objects.link(master_cam)
        else:
            master_cam = scene.objects["Master_Camera"]

        # Clear previous keyframes
        master_cam.animation_data_clear()

        for i, switch in enumerate(scene.camera_switch_list):
            cam = bpy.data.objects.get(switch.camera_name)
            if cam:
                # Set initial position at start_frame
                master_cam.location = cam.location
                master_cam.rotation_euler = cam.rotation_euler
                master_cam.keyframe_insert(data_path="location", frame=switch.start_frame)
                master_cam.keyframe_insert(data_path="rotation_euler", frame=switch.start_frame)

                # Calculate transition frames
                if i < len(scene.camera_switch_list) - 1:
                    next_start_frame = scene.camera_switch_list[i + 1].start_frame
                    transition_start = max(next_start_frame - transition_frames, switch.start_frame)
                else:
                    transition_start = switch.start_frame + 50  # Default gap if no next camera

                # Keyframe transition at calculated frame
                master_cam.keyframe_insert(data_path="location", frame=transition_start)
                master_cam.keyframe_insert(data_path="rotation_euler", frame=transition_start)

                # Move to next camera position
                if i < len(scene.camera_switch_list) - 1:
                    next_cam = bpy.data.objects.get(scene.camera_switch_list[i + 1].camera_name)
                    if next_cam:
                        master_cam.location = next_cam.location
                        master_cam.rotation_euler = next_cam.rotation_euler
                        master_cam.keyframe_insert(data_path="location", frame=next_start_frame)
                        master_cam.keyframe_insert(data_path="rotation_euler", frame=next_start_frame)

        self.report({'INFO'}, "Camera animation generated!")
        return {'FINISHED'}


# Register/unregister functions
classes = (
    CameraSwitchItem,
    VIEW3D_PT_CameraSwitcher,
    CAMERA_OT_AppendSelected,
    CAMERA_OT_CreateFromView,
    CAMERA_OT_RemoveCamera,
    CAMERA_OT_SetActive,
    CAMERA_OT_GenerateAnimation,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.camera_switch_list = bpy.props.CollectionProperty(type=CameraSwitchItem)
    bpy.types.Scene.transition_frames = bpy.props.IntProperty(name="Transition Frames", default=10, min=1)

def unregister():
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.camera_switch_list
    del bpy.types.Scene.transition_frames


if __name__ == "__main__":
    register()
