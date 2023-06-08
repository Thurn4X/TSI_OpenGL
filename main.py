from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D,Text,Image
import numpy as np
import OpenGL.GL as GL
import pyrr


def main():
    gruntidle = ["sprites/Grunt1/HK1Oa1.png","sprites/Grunt1/HK1Ob1.png","sprites/Grunt1/HK1Oc1.png","sprites/Grunt1/gruntfire.png"]
    gruntmove=["sprites/Grunt1/HK1Ra1.png","sprites/Grunt1/HK1Rb1.png","sprites/Grunt1/HK1Rc1.png","sprites/Grunt1/HK1Rd1.png","sprites/Grunt1/HK1Re1.png","sprites/Grunt1/HK1Rf1.png",]
    crowbar =[["sprites/Crowbar/crowbar1.png","sprites/Crowbar/crowbar2.png","sprites/Crowbar/crowbar3.png","sprites/Crowbar/crowbar4.png","sprites/Crowbar/crowbar5.png","sprites/Crowbar/crowbar6.png","sprites/Crowbar/crowbar7.png","sprites/Crowbar/crowbar1.png"],["sprites/Crowbar/crowbar7.png","sprites/Crowbar/crowbar8.png","sprites/Crowbar/crowbar9.png","sprites/Crowbar/crowbar10.png","sprites/Crowbar/crowbar11.png","sprites/Crowbar/crowbar12.png","sprites/Crowbar/crowbar13.png","sprites/Crowbar/crowbar14.png","sprites/Crowbar/crowbar15.png","sprites/Crowbar/crowbar7.png"],["sprites/Crowbar/crowbar15.png","sprites/Crowbar/crowbar16.png","sprites/Crowbar/crowbar17.png","sprites/Crowbar/crowbar18.png","sprites/Crowbar/crowbar19.png","sprites/Crowbar/crowbar20.png","sprites/Crowbar/crowbar21.png","sprites/Crowbar/crowbar22.png","sprites/Crowbar/crowbar23.png","sprites/Crowbar/crowbar24.png","sprites/Crowbar/crowbar25.png","sprites/Crowbar/crowbar26.png","sprites/Crowbar/crowbar27.png","sprites/Crowbar/crowbar15.png"]]
    bolt = ["sprites/bolt/bolt2.png","sprites/bolt/bolt1.png"]
    reloadbolt = ["sprites/bolt/bolt_reload0.png","sprites/bolt/bolt_reload1.png","sprites/bolt/bolt_reload2.png","sprites/bolt/bolt_reload3.png","sprites/bolt/bolt_reload4.png","sprites/bolt/bolt_reload5.png","sprites/bolt/bolt_reload6.png","sprites/bolt/bolt_reload7.png","sprites/bolt/bolt_reload8.png","sprites/bolt/bolt_reload9.png","sprites/bolt/bolt_reload10.png"]
    gun = ["sprites/Pistol/HW2Fa0.png","sprites/Pistol/HW2Fb0.png","sprites/Pistol/HW2Fc0.png","sprites/Pistol/HW2Fd0.png","sprites/Pistol/HW2Fe0.png","sprites/Pistol/HW2Ff0.png","sprites/Pistol/HW2Fg0.png","sprites/Pistol/HW2Fh0.png","sprites/Pistol/HW2Fi0.png","sprites/Pistol/HW2Fj0.png","sprites/Pistol/HW2Fk0.png","sprites/Pistol/HW2Fl0.png","sprites/Pistol/HW2Fa0.png"]
    reloadglock = ["sprites/Pistol/HW2Ra0.png","sprites/Pistol/HW2Rb0.png","sprites/Pistol/HW2Rc0.png","sprites/Pistol/HW2Rd0.png","sprites/Pistol/HW2Re0.png","sprites/Pistol/HW2Rf0.png","sprites/Pistol/HW2Rg0.png","sprites/Pistol/HW2Rh0.png","sprites/Pistol/HW2Ri0.png","sprites/Pistol/HW2Rj0.png","sprites/Pistol/HW2Rk0.png","sprites/Pistol/HW2Rl0.png","sprites/Pistol/HW2Rm0.png","sprites/Pistol/HW2Rn0.png","sprites/Pistol/HW2Ro0.png","sprites/Pistol/HW2Rp0.png","sprites/Pistol/HW2Rq0.png","sprites/Pistol/HW2Rr0.png","sprites/Pistol/HW2Rs0.png","sprites/Pistol/HW2Rt0.png","sprites/Pistol/HW2Ru0.png","sprites/Pistol/HW2Rv0.png",]
    etatgun =1
    ammo = 10
    viewer = ViewerGL(gun,etatgun,ammo,reloadglock,bolt,reloadbolt,crowbar,gruntmove,gruntidle)
    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
    programIMG_id= glutils.create_program_from_file('image.vert', 'image.frag')




    map_matrix = [
        [1,1,2,2,2,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2],
        [1,2,1,1,1,2,2,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,2,2,2,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,2,1,1,1,1,1,2,1,1,1,2,2,2,2,2,2,2,2,1,2,1,1,2,1,1,1,1,1,2],
        [1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,1,2,1,1,1,1,1,2],
        [1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,1,2,2],
        [1,1,1,1,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1,1,1,1,1,1,1,2,1],
        [1,1,2,2,2,1,2,1,1,1,1,1,2,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,2,1],
        [1,1,2,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1,2,1],
        [2,2,2,1,2,1,1,1,1,1,1,2,2,1,1,1,1,1,1,2,1,1,1,1,1,2,2,1,2,2],
        [1,1,1,1,2,2,2,2,2,2,1,2,2,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2],
        [2,2,2,1,2,1,1,1,1,2,1,2,2,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1],
        [1,1,2,1,2,1,1,1,1,2,1,2,2,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,2],
        [1,1,2,1,2,2,2,1,1,2,1,2,2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,2,1],
        [1,1,2,1,1,1,2,1,1,2,1,2,2,2,2,2,2,1,2,2,2,1,2,1,1,2,2,1,2,2],
        [1,1,2,2,2,1,2,2,1,2,1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,2],
        [1,1,1,2,1,1,1,2,2,2,1,2,2,2,2,2,2,1,2,2,2,2,2,1,1,1,1,1,1,2],
        [1,1,1,2,1,1,1,1,1,2,1,2,2,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2],
        [1,1,1,2,1,1,1,2,2,2,1,2,2,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2],
        [1,1,1,2,2,2,2,2,1,2,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2],
        [1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2],


    ]

    cube = Mesh.load_obj('cube.obj')
    cube_width = np.amax(cube.vertices, axis=0)[0] - np.amin(cube.vertices, axis=0)[0]
    cube_height = np.amax(cube.vertices, axis=0)[1] - np.amin(cube.vertices, axis=0)[1]
    cube_depth = np.amax(cube.vertices, axis=0)[2] - np.amin(cube.vertices, axis=0)[2]
    cube.normalize()
    cube_scale = min(1.0, 4.0 / cube_width)  # Adjust the desired scale of the cubes
    cube.apply_matrix(pyrr.matrix44.create_from_scale([1, 2, 1, 1]))






    texture_paths = {
    0: 'grass.jpg',
    2: 'evenbiggerwall.png',
    }

    # Load the textures
    textures = {}
    for value, path in texture_paths.items():
        textures[value] = glutils.load_texture(path)
 
    # Iterate over the map_matrix and add cubes accordingly
    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] == 0:
                texture = textures[0]  # Use the grass texture for 0s
                tr = Transformation3D()
                tr.translation.x = col * (cube_width * cube_scale)
                tr.translation.y = -np.amin(cube.vertices, axis=0)[1] * cube_scale
                tr.translation.z = -row * (cube_depth * cube_scale)
                tr.rotation_center.z = 0.2
                o = Object3D(cube.load_to_gpu(), cube.get_nb_triangles(), program3d_id, texture, tr)
                viewer.add_object(o)
            elif map_matrix[row][col] in textures:
                texture = textures[map_matrix[row][col]]
                tr = Transformation3D()
                tr.translation.x = col * (cube_width * cube_scale)
                tr.translation.y = -np.amin(cube.vertices, axis=0)[1] * cube_scale
                tr.translation.z = -row * (cube_depth * cube_scale)
                tr.rotation_center.z = 0.2
                o = Object3D(cube.load_to_gpu(), cube.get_nb_triangles(), program3d_id, texture, tr)
                viewer.add_object(o)


    m = Mesh()
    offset = 10  # Adjust the translation offset along the z-axis
    p0, p1, p2, p3 = [-1, 0, -50], [60, 0, -50], [60, 0, 0], [-1, 0, 0]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [30, 0], [30, 30], [0, 30]  # Modify the UV coordinates
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('tilefinale.png')  # Replace 'grass.jpg' with 'tilefinale.png'
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)




    #m = Mesh.load_obj('doom_voxel_marines.obj')
    #m.normalize()
    #m.apply_matrix(pyrr.matrix44.create_from_scale([3, 3, 3, 1]))
    #tr = Transformation3D()
    #tr.translation.y = -np.amin(m.vertices, axis=0)[1]
    #tr.translation.z = -5
    #tr.rotation_center.z = 0.2
    #texture = glutils.load_texture('doom_voxel_marines.png')
    #o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
    #viewer.add_object(o)

    #m = Mesh()
    #p0, p1, p2, p3 = [-1, 0, -1], [1, 0, -1], [1, 0, 1], [-1, 0, 1]
    #n, c = [0, 1, 0], [1, 1, 1]
    #t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    #m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    #m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    #texture = glutils.load_texture('XCONC11.png')
    #o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    #viewer.add_object(o)

    #vao = Text.initalize_geometry()
    #texture = glutils.load_texture('fontB.jpg')
    #o = Text('3ETI', np.array([-1, -1], np.float32), np.array([1, 0.2], np.float32), vao, 2, programGUI_id, texture)
    #viewer.add_object(o)

    m = Mesh()
    #variables carré méchant 2D
    p0, p1, p2, p3 =  [1.5, 0, 1.5],[0, 0, 0], [0, 2.5, 0], [1.5, 2.5, 1.5]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    #définition carré
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)

    #ajout texture
    texture = glutils.load_texture("sprites/Grunt1/HK1Ba0.png")
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
    o_gun = Image("sprites/Crowbar/crowbar1.png", np.array([-0.7, -1], np.float32), np.array([0.7, 0.8], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o_gun)

    o_texture = glutils.load_texture(crowbar[0][0])
    viewer.update_object_texture(1, o_texture)  # Assuming the gun object is at index 3


    texture = glutils.load_texture("crosshair.png")
    o_crosshair = Image("crosshair.png", np.array([-0.02, -0.05], np.float32), np.array([0.02, 0.05], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o_crosshair)

    o_texture = glutils.load_texture("crosshair.png")
    viewer.update_object_texture(2, o_texture)  # Assuming the crosshair object is at index 2




    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    o = Text('HP :', np.array([-1, -0.95], np.float32), np.array([-0.75,-0.8], np.float32), vao, 2, programGUI_id, texture)
    o_lifevalue = Text('100', np.array([-0.75, -0.95], np.float32), np.array([-0.65,-0.8], np.float32), vao, 2, programGUI_id, texture)
    o_ammo = Text('MUN :', np.array([0.45, -0.95], np.float32), np.array([0.65,-0.8], np.float32), vao, 2, programGUI_id, texture)
    o_ammovalue = Text('0', np.array([0.7, -0.95], np.float32), np.array([0.8,-0.8], np.float32), vao, 2, programGUI_id, texture)
    viewer.add_object(o)
    viewer.add_object(o_lifevalue)
    viewer.add_object(o_ammo)
    viewer.add_object(o_ammovalue)

   





    viewer.run()



    
if __name__ == '__main__':
    main()