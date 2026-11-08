"""Build an editable Blender asset and a browser GLB from prepared geometry.

Palette: original NadLan portrait and ink #0F2233, sea #2F6F86, mist #D3DCE2.
UI face IBM Plex Sans is handled by the web widget. No cream/gold design accents.
This retains the subject's photographic colours and isolated silhouette rather
than generic AI cards or replacement identity. Offline, free and local.
"""
from pathlib import Path
import bpy, json, math, struct
from mathutils import Vector

ROOT=Path(__file__).resolve().parent
data=json.loads((ROOT/'geometry.json').read_text(encoding='utf-8'))
bpy.ops.wm.read_factory_settings(use_empty=True)
mesh=bpy.data.meshes.new('NadLan portrait shaped surface')
# Reverse projected Delaunay winding to face toward Blender -Y.
mesh.from_pydata(data['vertices'],[],[list(reversed(t)) for t in data['triangles']])
mesh.update()
obj=bpy.data.objects.new('NadLan_Advisor',mesh)
bpy.context.collection.objects.link(obj)
uv=mesh.uv_layers.new(name='Original portrait projection')
for polygon in mesh.polygons:
    polygon.use_smooth=True
    for li in polygon.loop_indices:
        vi=mesh.loops[li].vertex_index
        uv.data[li].uv=data['uv'][vi]
obj.shape_key_add(name='Basis')
for name in ['mouthOpen','blink']:
    k=obj.shape_key_add(name=name)
    for v,co in zip(k.data,data[name]): v.co=co
    k.value=0
obj['identity']='Original fictional blonde from kit/face-a.png'
obj['reconstruction']='Image-derived front surface, not a full 360 degree head'
obj['intended_turn_limit_degrees']=3

mat=bpy.data.materials.new('Original portrait, unlit')
mat.use_nodes=True
nodes=mat.node_tree.nodes
nodes.clear()
out=nodes.new('ShaderNodeOutputMaterial')
shader=nodes.new('ShaderNodeBsdfPrincipled')
shader.inputs['Roughness'].default_value=1
shader.inputs['Specular IOR Level'].default_value=0
shader.inputs['Emission Strength'].default_value=1
tex=nodes.new('ShaderNodeTexImage')
tex.image=bpy.data.images.load(str(ROOT/data['texture']))
tex.image.pack()
mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Base Color'])
mat.node_tree.links.new(tex.outputs['Color'],shader.inputs['Emission Color'])
mat.node_tree.links.new(tex.outputs['Alpha'],shader.inputs['Alpha'])
mat.node_tree.links.new(shader.outputs[0],out.inputs['Surface'])
mat.surface_render_method='DITHERED'
mat.use_transparency_overlap=False
mat.use_backface_culling=False
obj.data.materials.append(mat)

# The original closed-eye artwork sits on the same 3D surface, with feathered
# alpha. Runtime crossfades this material at a blink, instead of stretching iris.
blinkmesh=mesh.copy()
blinkmesh.name='Closed eyelid shaped surface'
overlay=bpy.data.objects.new('BlinkOverlay',blinkmesh)
bpy.context.collection.objects.link(overlay)
overlay.shape_key_clear()
for vert in blinkmesh.vertices: vert.co.y-=.001
blinkmesh.materials.clear()
blinkmat=mat.copy()
blinkmat.name='BlinkOverlay'
blinktex=next(n for n in blinkmat.node_tree.nodes if n.type=='TEX_IMAGE')
blinktex.image=bpy.data.images.load(str(ROOT/'assets'/'blink-overlay-v2.png'))
blinktex.image.pack()
blinkmesh.materials.append(blinkmat)
overlay.hide_render=True

inner=bpy.data.meshes.new('Inner mouth cavity')
inner.from_pydata(data['mouthInterior'],[],[list(reversed(range(len(data['mouthInterior']))))])
inner.update()
cavity=bpy.data.objects.new('Mouth_cavity',inner)
bpy.context.collection.objects.link(cavity)
mouthmat=bpy.data.materials.new('Soft mouth interior')
mouthmat.use_nodes=True
pn=mouthmat.node_tree.nodes.get('Principled BSDF')
pn.inputs['Base Color'].default_value=(.055,.018,.025,1)
pn.inputs['Roughness'].default_value=1
pn.inputs['Emission Color'].default_value=(.055,.018,.025,1)
pn.inputs['Emission Strength'].default_value=.8
cavity.data.materials.append(mouthmat)

camdata=bpy.data.cameras.new('Front preview')
cam=bpy.data.objects.new('Front preview',camdata)
bpy.context.collection.objects.link(cam)
cam.location=(0,-5,.10)
cam.rotation_euler=(Vector((0,0,.10))-cam.location).to_track_quat('-Z','Y').to_euler()
camdata.type='ORTHO'
camdata.ortho_scale=1.68
scene=bpy.context.scene
scene.camera=cam
scene.render.engine='BLENDER_EEVEE'
scene.render.resolution_x=640
scene.render.resolution_y=720
scene.render.resolution_percentage=100
scene.render.image_settings.file_format='PNG'
scene.render.film_transparent=True
scene.view_settings.view_transform='Standard'
scene.view_settings.look='None'
scene.view_settings.exposure=0
scene.view_settings.gamma=1
scene.render.filepath=str(ROOT/'assets'/'blender-v2-front.png')
bpy.ops.wm.save_as_mainfile(filepath=str(ROOT/'nadlan-advisor-v2.blend'))
for item in bpy.context.selected_objects: item.select_set(False)
obj.select_set(True)
cavity.select_set(True)
overlay.select_set(True)
bpy.context.view_layer.objects.active=obj
bpy.ops.export_scene.gltf(filepath=str(ROOT/'assets'/'nadlan-advisor-v2.glb'),export_format='GLB',use_selection=True,export_apply=False,export_animations=False,export_morph=True,export_morph_normal=False,export_image_format='AUTO',export_yup=True)
# Standards-compliant unlit material keeps the original likeness in all runtimes.
glb=ROOT/'assets'/'nadlan-advisor-v2.glb'
raw=glb.read_bytes()
n=struct.unpack_from('<I',raw,12)[0]
gltf=json.loads(raw[20:20+n])
for material in gltf['materials']:
    if material['name'] in ['Original portrait, unlit','BlinkOverlay']:
        material['extensions']={'KHR_materials_unlit':{}}
        material['alphaMode']='BLEND'
        material.pop('emissiveTexture',None)
        material.pop('emissiveFactor',None)
        if material['name']=='BlinkOverlay':
            material['pbrMetallicRoughness']['baseColorFactor']=[1,1,1,0]
gltf.setdefault('extensionsUsed',[]).append('KHR_materials_unlit')
j=json.dumps(gltf,separators=(',',':')).encode('utf-8')
j+=b' '*((-len(j))%4)
tail=raw[20+n:]
glb.write_bytes(struct.pack('<4sII',b'glTF',2,20+len(j)+len(tail))+struct.pack('<I4s',len(j),b'JSON')+j+tail)
bpy.ops.render.render(write_still=True)
obj.data.shape_keys.key_blocks['mouthOpen'].value=.8
scene.render.filepath=str(ROOT/'assets'/'blender-v2-speaking.png')
bpy.ops.render.render(write_still=True)
obj.data.shape_keys.key_blocks['mouthOpen'].value=0
overlay.hide_render=False
scene.render.filepath=str(ROOT/'assets'/'blender-v2-blink.png')
bpy.ops.render.render(write_still=True)
overlay.hide_render=True
for angle in [-3,3,25]:
    for item in [obj,overlay,cavity]: item.rotation_euler.z=math.radians(angle)
    scene.render.filepath=str(ROOT/'assets'/('blender-v2-angle-'+str(angle)+'.png'))
    bpy.ops.render.render(write_still=True)
# Separate wireframe evidence makes the real (but inferred) surface depth
# inspectable. It is not a promise of a reconstructed back or unseen anatomy.
for item in [obj,overlay,cavity]: item.rotation_euler.z=math.radians(25)
wiremat=bpy.data.materials.new('Mesh proof, NadLan sea')
wiremat.use_nodes=True
wn=wiremat.node_tree.nodes
wn.clear()
wo=wn.new('ShaderNodeOutputMaterial')
we=wn.new('ShaderNodeEmission');we.inputs['Color'].default_value=(.184,.435,.525,1)
wt=wn.new('ShaderNodeBsdfTransparent')
ww=wn.new('ShaderNodeWireframe');ww.use_pixel_size=True;ww.inputs['Size'].default_value=.85
wm=wn.new('ShaderNodeMixShader')
wiremat.node_tree.links.new(ww.outputs[0],wm.inputs[0])
wiremat.node_tree.links.new(wt.outputs[0],wm.inputs[1])
wiremat.node_tree.links.new(we.outputs[0],wm.inputs[2])
wiremat.node_tree.links.new(wm.outputs[0],wo.inputs[0])
obj.data.materials.clear();obj.data.materials.append(wiremat)
cavity.hide_render=True
scene.render.filepath=str(ROOT/'assets'/'blender-v2-wireframe.png')
bpy.ops.render.render(write_still=True)
print('NADLAN_ASSET_READY',str(glb))
