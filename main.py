from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D,Text,Image
import numpy as np
import OpenGL.GL as GL
import pyrr


def main():
    bolt = ["sprites/bolt/bolt2.png","sprites/bolt/bolt1.png"]
    reloadbolt = ["sprites/bolt/bolt_reload0.png","sprites/bolt/bolt_reload1.png","sprites/bolt/bolt_reload2.png","sprites/bolt/bolt_reload3.png","sprites/bolt/bolt_reload4.png","sprites/bolt/bolt_reload5.png","sprites/bolt/bolt_reload6.png","sprites/bolt/bolt_reload7.png","sprites/bolt/bolt_reload8.png","sprites/bolt/bolt_reload9.png","sprites/bolt/bolt_reload10.png"]
    gun = ["gun1.png","gun.png"]
    reloadglock = ["gun.png","sprites/reload0.png","sprites/reload1.png","sprites/reload2.png","sprites/reload3.png","sprites/reload4.png","sprites/reload5.png","sprites/reload6.png","sprites/reload7.png","sprites/reload8.png","sprites/reload9.png","sprites/reload10.png","gun.png"]
    etatgun =1
    ammo = 10
    viewer = ViewerGL(gun , etatgun,ammo,reloadglock,bolt,reloadbolt)
    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
    programIMG_id= glutils.create_program_from_file('image.vert', 'image.frag')

    m = Mesh.load_obj('doom_voxel_marines.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([3, 3, 3, 1]))
    tr = Transformation3D()
    tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    tr.translation.z = -5
    tr.rotation_center.z = 0.2
    texture = glutils.load_texture('doom_voxel_marines.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    viewer.add_object(o)

    m = Mesh()
    p0, p1, p2, p3 = [-25, 0, -25], [25, 0, -25], [25, 0, 25], [-25, 0, 25]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('grass.jpg')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    #vao = Text.initalize_geometry()
    #texture = glutils.load_texture('fontB.jpg')
    #o = Text('3ETI', np.array([-1, -1], np.float32), np.array([1, 0.2], np.float32), vao, 2, programGUI_id, texture)
    #viewer.add_object(o)


    vao = Image.initialize_geometry()
    texture = glutils.load_texture("gun.png")
    o_gun = Image("gun.png", np.array([-0.5, -1], np.float32), np.array([0.5, 0], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o_gun)

    o_texture = glutils.load_texture(gun[etatgun])
    viewer.update_object_texture(2, o_texture)  # Assuming the gun object is at index 0

    viewer.run()



if __name__ == '__main__':
    main()
    