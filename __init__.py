bl_info = {
    "name": "Rivet Instancer",
    "author": "Jeremie Ferreira",
    "version": (1, 0, 0),
    "blender": (2, 80, 0),
    "location": "View3D > UI > Tool",
    "description": "Instanciate rivets along the selected edges of the selected object.",
    "warning": "",
    "doc_url": "",
    "category": "Object",
}

import bpy
import bmesh
from mathutils import Vector, Matrix

class EdgeData:
    """This class allow our algorithm to keep track of vertex order in
    an ordered array of edges"""
    def __init__(self, edge, v1, v2):
        self.edge = edge
        self.v1 = v1
        self.v2 = v2

class RivetData:
    """This class holds data for the rivet positions and normals"""
    def __init__(self, position, normal):
        self.position = position
        self.normal = normal

def show_message(icon = "INFO", title = "Info", message = "Information"):
    def draw(self, context):
        self.layout.label(text=message)
    print("\n{}: {}".format(icon, message))
    bpy.context.window_manager.popup_menu(draw, title = title, icon = icon)

def find_edge_chains(edges):
    """Find ordered lists of connected edges
    returns list[list[EdgeData]] the chains of ordered edges"""
    edges_array = edges.copy()
    chains = []

    while edges_array:
        current_chain = []
        e = edges_array.pop()
        (v1, v2) = e.verts[0], e.verts[1]
        current_chain.append(EdgeData(e, v1, v2))

        #find all connected edges in the following loop
        while True:
            #find the next connected edge and update v1 and v2
            for e2 in edges_array:
                (v3, v4) = e2.verts[0], e2.verts[1]
                if v1 == v3:
                    current_chain.insert(0, EdgeData(e2, v4, v3))
                    v1 = v4
                    edges_array.remove(e2)
                    break
                if v1 == v4:
                    current_chain.insert(0, EdgeData(e2, v3, v4))
                    v1 = v3
                    edges_array.remove(e2)
                    break
                if v2 == v3:
                    current_chain.append(EdgeData(e2, v3, v4))
                    v2 = v4
                    edges_array.remove(e2)
                    break
                if v2 == v4:
                    current_chain.append(EdgeData(e2, v4, v3))
                    v2 = v3
                    edges_array.remove(e2)
                    break
            else:
                #no more edge found in this chain (no 'break' above)
                break

        chains.append(current_chain)

    return chains

def create_rivets(context, rivet_object_name, spacing):
    """Instanciate rivets along the selected edges of the selected mesh"""
    try:
        rivet_object = bpy.data.objects[rivet_object_name]
    except:
        show_message("ERROR", "Object not found", "The Rivet object is not found {}.".format(rivet_object_name))
        return {'CANCELLED'}

    obj = context.object

    if obj is None:
        show_message("ERROR", "No object selected", "You should select an object")
        return {'CANCELLED'}

    if obj.mode == 'EDIT':
        bpy.ops.object.mode_set(mode='OBJECT')
    
    # Create a BMesh from the current object
    bm = bmesh.new()
    bm.from_mesh(obj.data)
    
    # Find all selected edges
    selected_edges = [e for e in bm.edges if e.select]

    if not selected_edges:
        show_message("ERROR", "No edges selected", "The object {} has no selected edges.".format(obj.name))
        return {'CANCELLED'}

    # Find edge chains
    edge_chains = find_edge_chains(selected_edges)
    
    # Iterate over each edge chain
    for chain in edge_chains:
        # Calculate positions along the edge chain
        rivets_data = []
        remaining_length = 0
        edge_counter = 0
        
        for edge_data in chain:
            edge = edge_data.edge
            edge_length = edge.calc_length()
            start_pos, end_pos = edge_data.v1, edge_data.v2
            direction = (edge.verts[0].normal + edge.verts[1].normal) * .5

            current_length = remaining_length
            while current_length <= edge_length:
                factor = current_length / edge_length
                position = start_pos.co.lerp(end_pos.co, factor)
                rivets_data.append(RivetData(position, direction))
                current_length += spacing
            
            remaining_length = current_length - edge_length

            edge_counter += 1

        # Place rivets at calculated positions
        for rivet_data in rivets_data:
            # Create a new instance of the rivet
            new_rivet = rivet_object.copy()
            new_rivet.data = rivet_object.data.copy()
            context.collection.objects.link(new_rivet)
            
            # Position the rivet
            new_rivet.location = obj.matrix_world @ rivet_data.position
            # Find normal and edge direction for orientation
            normal_vector = Vector((0, 0, 1)).rotation_difference(rivet_data.normal)
            new_rivet.rotation_euler = normal_vector.to_euler()
            
    # Update the mesh
    bm.free()
    bpy.ops.object.mode_set(mode='OBJECT')

    return {'FINISHED'}, None

class OBJECT_OT_AddRivets(bpy.types.Operator):
    bl_idname = "object.add_rivets"
    bl_description = "Instanciate rivets along the selected edges of the selected object"
    bl_label = "Generate Rivets"
    bl_options = {'REGISTER', 'UNDO'}

    rivet_object_name: bpy.props.StringProperty(
        name="Rivet Object Name",
        description="Name of the object to instanciate",
        default="RivetMaster"
    )

    spacing: bpy.props.FloatProperty(
        name="Spacing",
        description="Spacing between rivets",
        default=0.1,
        min=0.001,
    )

    def execute(self, context):
        create_rivets(context, self.rivet_object_name, self.spacing)
        return {'FINISHED'}

class VIEW3D_PT_AddRivetsPanel(bpy.types.Panel):
    bl_label = "Instanciate Rivets"
    bl_idname = "VIEW3D_PT_add_rivets"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = 'Tool'

    def draw(self, context):
        layout = self.layout
        layout.operator("object.add_rivets")

def menu_func(self, context):
    self.layout.operator(OBJECT_OT_AddRivets.bl_idname)

def register():
    bpy.utils.register_class(OBJECT_OT_AddRivets)
    bpy.utils.register_class(VIEW3D_PT_AddRivetsPanel)
    bpy.types.VIEW3D_MT_mesh_add.append(menu_func)


def unregister():
    bpy.utils.unregister_class(OBJECT_OT_AddRivets)
    bpy.utils.unregister_class(VIEW3D_PT_AddRivetsPanel)
    bpy.types.VIEW3D_MT_mesh_add.remove(menu_func)

if __name__ == "__main__":
    register()