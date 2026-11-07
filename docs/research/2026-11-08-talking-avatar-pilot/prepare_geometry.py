"""Local image-derived mesh preparation. No keys, paid services or inference server.

The original fictional blonde is projected onto an inferred front surface.
This is a limited-view 3D portrait, not a complete 360 degree reconstruction.
"""
from pathlib import Path
import hashlib, json, urllib.request
import numpy as np
from PIL import Image, ImageFilter
from scipy.interpolate import LinearNDInterpolator, NearestNDInterpolator
from scipy.spatial import Delaunay
import cv2
import mediapipe as mp

ROOT = Path(__file__).resolve().parent
KIT = ROOT.parent / 'kit'
ASSETS = ROOT / 'assets'
MODELS = ROOT / 'build-models'
ASSETS.mkdir(exist_ok=True)
MODELS.mkdir(exist_ok=True)
urls = {
 'face_landmarker.task':'https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task',
 'selfie_multiclass.tflite':'https://storage.googleapis.com/mediapipe-models/image_segmenter/selfie_multiclass_256x256/float32/latest/selfie_multiclass_256x256.tflite',
 'hair_segmenter.tflite':'https://storage.googleapis.com/mediapipe-models/image_segmenter/hair_segmenter/float32/latest/hair_segmenter.tflite'
}
for name,url in urls.items():
    target = MODELS/name
    if not target.exists(): urllib.request.urlretrieve(url,target)

image = mp.Image.create_from_file(str(KIT/'face-a.png'))
opts=mp.tasks.vision.FaceLandmarkerOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELS/'face_landmarker.task')))
with mp.tasks.vision.FaceLandmarker.create_from_options(opts) as task:
    result=task.detect(image)
if len(result.face_landmarks)!=1: raise RuntimeError('Expected exactly one face')
lm=np.array([[p.x,p.y,p.z] for p in result.face_landmarks[0]])[:468]
(ROOT/'landmarks.json').write_text(json.dumps(lm.tolist()),encoding='utf-8')
opts=mp.tasks.vision.ImageSegmenterOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELS/'selfie_multiclass.tflite')),output_confidence_masks=True, output_category_mask=True)
with mp.tasks.vision.ImageSegmenter.create_from_options(opts) as task:
    seg=task.segment(image)
    bg=np.copy(seg.confidence_masks[0].numpy_view()).squeeze()
    categories=np.copy(seg.category_mask.numpy_view()).squeeze()
    body=np.sum([np.copy(seg.confidence_masks[i].numpy_view()).squeeze() for i in [2,3,4,5]],axis=0)
    clothing=np.copy(seg.confidence_masks[4].numpy_view()).squeeze()
opts=mp.tasks.vision.ImageSegmenterOptions(base_options=mp.tasks.BaseOptions(model_asset_path=str(MODELS/'hair_segmenter.tflite')),output_confidence_masks=True,output_category_mask=False)
with mp.tasks.vision.ImageSegmenter.create_from_options(opts) as task:
    hair=np.copy(task.segment(image).confidence_masks[1].numpy_view()).squeeze()

# Retain fine alpha at the hair boundary, with a short soft fade at the bust.
alpha=np.clip((np.clip(body+hair,0,1)-.28)/.56,0,1)
# Reject tiny disconnected background remnants without losing the connected hair.
count,labels,stats,_=cv2.connectedComponentsWithStats((alpha>.1).astype('uint8'),8)
main=1+int(np.argmax(stats[1:,cv2.CC_STAT_AREA]))
connected=(labels==main).astype('uint8')
connected=cv2.morphologyEx(connected,cv2.MORPH_CLOSE,np.ones((3,3),np.uint8))
alpha*=connected
height,width=alpha.shape
yy,xx=np.mgrid[0:height,0:width]
# Ben asked for a face, not a bust. Remove the jacket and feather the short
# neck under the chin while keeping the original hair silhouette.
neck_fade=np.clip((.705-yy/height)/.105,0,1)
neck_fade=neck_fade*neck_fade*(3-2*neck_fade)
hair_keep=np.clip((hair-.18)/.60,0,1)
alpha*=np.maximum(hair_keep,neck_fade)
alpha*=1-np.clip((clothing-.25)/.55,0,1)
# A small inset avoids the source window's pale-blue halo at widget size.
alpha=cv2.erode(alpha,np.ones((5,5),np.uint8))
alpha=cv2.GaussianBlur(alpha,(5,5),.8)
# Correct only the semi-transparent hair perimeter where the blue window bled
# into blonde fibres. Protect skin and the blue jacket completely.
rgb=np.asarray(Image.open(KIT/'face-a.png').convert('RGB')).astype('float32')
edge_distance=cv2.distanceTransform((alpha>.08).astype('uint8'),cv2.DIST_L2,3)
hair_edge=(edge_distance<16)&(yy<height*.705)&(body<.65)
blue_excess=np.maximum(rgb[:,:,2]-rgb[:,:,0]-5,0)
spill=np.clip(blue_excess/28,0,1)*hair_edge
alpha*=1-.92*spill
# Decontaminate residual coloured edge pixels from neighbouring opaque hair.
solid=(alpha>.97)&(hair>.80)
if np.any(solid):
    from scipy.ndimage import distance_transform_edt
    _,idx=distance_transform_edt(~solid,return_indices=True)
    edge_col=rgb[idx[0],idx[1]]
    amount=np.clip((1-alpha)*.75+spill*.55,0,.8)*hair_edge
    rgb=rgb*(1-amount[:,:,None])+edge_col*amount[:,:,None]
fade=np.clip((.77-yy/height)/.06,0,1)
alpha*=fade*fade*(3-2*fade)
rgba=np.zeros((height,width,4),dtype='uint8')
rgba[:,:,:3]=np.clip(rgb,0,255).astype('uint8')
rgba[:,:,3]=(alpha*255).astype('uint8')
rgba[rgba[:,:,3]==0,:3]=0
Image.fromarray(rgba).save(ASSETS/'portrait-cutout-v2.png',optimize=True)
Image.fromarray((alpha*255).astype('uint8')).save(ROOT/'portrait-mask.png')

# Reuse the exact existing closed-eye frame. This is a material overlay on the
# same shaped mesh, with a feathered alpha limited to the eye region.
closed=np.asarray(Image.open(KIT/'frame-BLINK.png').convert('RGBA')).copy()
eye_alpha=np.zeros((height,width),dtype='float32')
for cx,cy,rx,ry in [(459,345,54,35),(607,338,58,37)]:
    radius=np.sqrt(((xx-cx)/rx)**2+((yy-cy)/ry)**2)
    eye_alpha=np.maximum(eye_alpha,np.clip((1.22-radius)/.30,0,1))
closed[:,:,3]=(eye_alpha*255).astype('uint8')
closed[closed[:,:,3]==0,:3]=0
Image.fromarray(closed).save(ASSETS/'blink-overlay-v2.png',optimize=True)

# One connected photo-textured surface, with actual depth from MediaPipe facial
# landmarks, an independently curved hair/neck region and dedicated mouth seam.
# The extra grid provides smooth hair/neck curvature, avoiding a flat billboard.
grid=np.array([(x,y) for y in np.linspace(.006,.845,65) for x in np.linspace(.105,.91,61)])
face_hull=Delaunay(lm[:,:2])
grid=grid[face_hull.find_simplex(grid)<0]
xy=np.concatenate([lm[:,:2],grid])
interpolator=LinearNDInterpolator(lm[:,:2],lm[:,2])
depth=np.asarray(interpolator(xy))
outside=np.isnan(depth)
# Head's visible hair wraps backwards away from the facial nose/cheek plane.
gx,gy=xy[outside,0],xy[outside,1]
hair_curve=.045+.18*np.clip(((gx-.51)/.33)**2,0,1)+.065*np.clip(((gy-.36)/.38)**2,0,1)
neck_curve=.038+.11*np.clip(((gx-.52)/.38)**2,0,1)
depth[outside]=np.where(gy<.63,hair_curve,neck_curve)
# Smooth the transition at the face boundary by blending nearest landmark depth.
nearest=NearestNDInterpolator(lm[:,:2],lm[:,2])
from scipy.spatial import cKDTree
dist,_=cKDTree(lm[:,:2]).query(xy[outside])
blend=np.clip(dist/.075,0,1)
depth[outside]=nearest(xy[outside])*(1-blend)+depth[outside]*blend

tri=Delaunay(xy)
triangles=[]
inner=[78,191,80,81,82,13,312,311,310,415,308,324,318,402,317,14,87,178,88,95]
inner_poly=(lm[inner,:2]*1024).astype('float32')
for t in tri.simplices:
    center=xy[t].mean(axis=0)
    ix,iy=np.clip((center*1024).astype(int),0,1023)
    # Mask leaves a real mouth opening, hidden by the lip seam at neutral.
    mouth_inside=cv2.pointPolygonTest(inner_poly,(float(center[0]*1024),float(center[1]*1024)),False)>0
    if alpha[iy,ix]>.005 and not mouth_inside:
        triangles.append(t.tolist())

# Coordinates intentionally match glTF frontal +Z after Blender's axis export.
vertices=np.column_stack([(xy[:,0]-.505)*2,depth*2,(.42-xy[:,1])*2])
mouth=vertices.copy()
mx=float((lm[61,0]+lm[291,0])/2)
my=float((lm[13,1]+lm[14,1])/2)
for i,(x,y) in enumerate(xy):
    h=np.exp(-((x-mx)/.074)**4)
    # Lower lip and chin move ~5px; upper lip ~1px, no broad jaw flap.
    if y>=my:
        v=np.exp(-((y-(my+.018))/.052)**2)
        mouth[i,2]-=.010*h*v
        mouth[i,1]-=.0015*h*v
    else:
        v=np.exp(-((y-(my-.006))/.019)**2)
        mouth[i,2]+=.002*h*v

# A natural blink closes the actual eyelid/eye surface into its crease.
blink=vertices.copy()
for ids in ([33,160,158,133,153,144],[362,385,387,263,373,380]):
    ex=lm[ids,:2]
    xmin,xmax=ex[:,0].min(),ex[:,0].max()
    cy=(lm[ids[0],1]+lm[ids[3],1])/2+.001
    for i,(x,y) in enumerate(xy):
        if xmin-.012<x<xmax+.012 and abs(y-cy)<.028:
            edge=np.clip((x-xmin)/.012,0,1)*np.clip((xmax-x)/.012,0,1)
            band=np.clip(1-(abs(y-cy)-.009)/.018,0,1)
            weight=edge*band
            blink[i,2]=vertices[i,2]*(1-weight)+((.42-cy)*2)*weight

# A small recessed inner mouth surface appears only as lips part.
mouth_center=(lm[13,:2]+lm[14,:2])/2
mouth_depth=float((lm[13,2]+lm[14,2])/2)+.080
inner_vertices=[]
for t in np.linspace(0,2*np.pi,42,endpoint=False):
    x=mouth_center[0]+.060*np.cos(t)
    y=mouth_center[1]+.010*np.sin(t)
    inner_vertices.append([(x-.505)*2,mouth_depth*2,(.42-y)*2])

geometry={'vertices':vertices.tolist(),'triangles':triangles,'uv':np.column_stack([xy[:,0],1-xy[:,1]]).tolist(),
 'mouthOpen':mouth.tolist(),'blink':blink.tolist(),'mouthInterior':inner_vertices,
 'texture':'assets/portrait-cutout-v2.png','front':'glTF +Z','limits':'Single-photo front surface, keep head turns within +/-3 degrees.',
 'source':str(KIT/'face-a.png'),'landmarks':468,'vertices_count':len(vertices),'triangles_count':len(triangles)}
(ROOT/'geometry.json').write_text(json.dumps(geometry),encoding='utf-8')
receipt={'method':'MediaPipe landmarks plus inferred curved portrait perimeter, Blender mesh and morphs',
 'input_sha256':hashlib.sha256((KIT/'face-a.png').read_bytes()).hexdigest(),
 'models':{n:{'url':u,'sha256':hashlib.sha256((MODELS/n).read_bytes()).hexdigest()} for n,u in urls.items()},
 'package_version':mp.__version__,'geometry':{'landmarks':468,'vertices':len(vertices),'triangles':len(triangles)},
 'paid_services':0,'identity':'Original fictional blonde; no generated replacement identity',
 'limitations':'Inferred front surface and cutout hair; unseen sides/back are not reconstructed. Intended only for +/-3 degree turns.'}
(ROOT/'asset-provenance.json').write_text(json.dumps(receipt,indent=2),encoding='utf-8')
print(json.dumps(receipt['geometry']))
