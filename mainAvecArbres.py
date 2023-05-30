from viewerGLAvecArbres import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D,Text,Image
import numpy as np
import OpenGL.GL as GL
import pyrr

#SIUUUU
def main():
    crowbar =[["sprites/Crowbar/crowbar1.png","sprites/Crowbar/crowbar2.png","sprites/Crowbar/crowbar3.png","sprites/Crowbar/crowbar4.png","sprites/Crowbar/crowbar5.png","sprites/Crowbar/crowbar6.png","sprites/Crowbar/crowbar7.png","sprites/Crowbar/crowbar1.png"],["sprites/Crowbar/crowbar7.png","sprites/Crowbar/crowbar8.png","sprites/Crowbar/crowbar9.png","sprites/Crowbar/crowbar10.png","sprites/Crowbar/crowbar11.png","sprites/Crowbar/crowbar12.png","sprites/Crowbar/crowbar13.png","sprites/Crowbar/crowbar14.png","sprites/Crowbar/crowbar15.png","sprites/Crowbar/crowbar7.png"],["sprites/Crowbar/crowbar15.png","sprites/Crowbar/crowbar16.png","sprites/Crowbar/crowbar17.png","sprites/Crowbar/crowbar18.png","sprites/Crowbar/crowbar19.png","sprites/Crowbar/crowbar20.png","sprites/Crowbar/crowbar21.png","sprites/Crowbar/crowbar22.png","sprites/Crowbar/crowbar23.png","sprites/Crowbar/crowbar24.png","sprites/Crowbar/crowbar25.png","sprites/Crowbar/crowbar26.png","sprites/Crowbar/crowbar27.png","sprites/Crowbar/crowbar15.png"]]
    bolt = ["sprites/bolt/bolt2.png","sprites/bolt/bolt1.png"]
    reloadbolt = ["sprites/bolt/bolt_reload0.png","sprites/bolt/bolt_reload1.png","sprites/bolt/bolt_reload2.png","sprites/bolt/bolt_reload3.png","sprites/bolt/bolt_reload4.png","sprites/bolt/bolt_reload5.png","sprites/bolt/bolt_reload6.png","sprites/bolt/bolt_reload7.png","sprites/bolt/bolt_reload8.png","sprites/bolt/bolt_reload9.png","sprites/bolt/bolt_reload10.png"]
    gun = ["sprites/Pistol/HW2Fa0.png","sprites/Pistol/HW2Fb0.png","sprites/Pistol/HW2Fc0.png","sprites/Pistol/HW2Fd0.png","sprites/Pistol/HW2Fe0.png","sprites/Pistol/HW2Ff0.png","sprites/Pistol/HW2Fg0.png","sprites/Pistol/HW2Fh0.png","sprites/Pistol/HW2Fi0.png","sprites/Pistol/HW2Fj0.png","sprites/Pistol/HW2Fk0.png","sprites/Pistol/HW2Fl0.png","sprites/Pistol/HW2Fa0.png"]
    reloadglock = ["sprites/Pistol/HW2Ra0.png","sprites/Pistol/HW2Rb0.png","sprites/Pistol/HW2Rc0.png","sprites/Pistol/HW2Rd0.png","sprites/Pistol/HW2Re0.png","sprites/Pistol/HW2Rr0.png","sprites/Pistol/HW2Rg0.png","sprites/Pistol/HW2Rh0.png","sprites/Pistol/HW2Ri0.png","sprites/Pistol/HW2Rj0.png","sprites/Pistol/HW2Rk0.png","sprites/Pistol/HW2Rl0.png","sprites/Pistol/HW2Rm0.png","sprites/Pistol/HW2Rn0.png","sprites/Pistol/HW2Ro0.png","sprites/Pistol/HW2Rp0.png","sprites/Pistol/HW2Rq0.png","sprites/Pistol/HW2Rr0.png","sprites/Pistol/HW2Rs0.png","sprites/Pistol/HW2Rt0.png","sprites/Pistol/HW2Ru0.png","sprites/Pistol/HW2Rv0.png",]
    etatgun =1
    ammo = 10
    viewer = ViewerGL(gun , etatgun,ammo,reloadglock,bolt,reloadbolt,crowbar)
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

    m = Mesh.load_obj('tree.obj')
    m.normalize()
    m.apply_matrix(pyrr.matrix44.create_from_scale([5, 5, 5, 1]))
    for k in range (0,3):
        
        if k == 0:
            tr = Transformation3D()
            tr.translation.y = -np.amin(m.vertices, axis=0)[1]
            tr.translation.z = -10
            tr.translation.x = 10
            tr.rotation_center.z = 0.2
            
        if k == 1:
            tr = Transformation3D()
            tr.translation.y = -np.amin(m.vertices, axis=0)[1]
            tr.translation.z = -25
            tr.translation.x = 5
            tr.rotation_center.z = 0.2
            
        if k == 2:
            tr = Transformation3D()
            tr.translation.y = -np.amin(m.vertices, axis=0)[1]
            tr.translation.z = -15
            tr.translation.x = -16
            tr.rotation_center.z = 0.2
        
        texture = glutils.load_texture('tree.png')
        o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        viewer.add_object(o)

    #m = Mesh.load_obj('tree.obj')
    #m.normalize()
    #m.apply_matrix(pyrr.matrix44.create_from_scale([5, 5, 5, 1]))
    #tr = Transformation3D()
    #tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    #tr.translation.z = -30
    #tr.translation.x = 5
    #tr.rotation_center.z = 0.2
    #texture = glutils.load_texture('tree.png')
    #o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    #viewer.add_object(o)

    #m = Mesh.load_obj('tree.obj')
    #m.normalize()
    #m.apply_matrix(pyrr.matrix44.create_from_scale([5, 5, 5, 1]))
    #tr = Transformation3D()
    #tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    #tr.translation.z = -20
    #tr.translation.x = -2
    #tr.rotation_center.z = 0.2
    #texture = glutils.load_texture('tree.png')
    #o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    #viewer.add_object(o)

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

    m = Mesh()
    p0, p1, p2, p3 =  [2, 0, 2],[0, 0, 0], [0, 3, 0], [2, 3, 2]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture("sprites/Grunt1/HK1Ia1.png")
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)

    
    #m = Mesh.load_obj('DUST2.obj')
    #m.normalize()
    #m.apply_matrix(pyrr.matrix44.create_from_scale([40, 40, 40, 1]))
    #tr = Transformation3D()
    #tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    #tr.translation.z = -5
    #tr.rotation_center.z = 0.2
    #texture = glutils.load_texture('doom_voxel_marines.png')
    #o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    #viewer.add_object(o)


    vao = Image.initialize_geometry()
    texture = glutils.load_texture("sprites/Crowbar/crowbar1.png")
    o_gun = Image("sprites/Crowbar/crowbar1.png", np.array([-0.5, -1], np.float32), np.array([0.5, 0], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o_gun)

    o_texture = glutils.load_texture(crowbar[0][0])
    viewer.update_object_texture(6, o_texture)  # Assuming the gun object is at index 2


    viewer.run()



if __name__ == '__main__':
    main()
    