from viewerGL import ViewerGL
import glutils
from mesh import Mesh
from cpe3d import Object3D, Camera, Transformation3D,Text,Image,Hitbox
import numpy as np
import OpenGL.GL as GL
import pyrr


def main():
    zombieattack = ["sprites/zombie/HLEAa1.png","sprites/zombie/HLEAb1.png","sprites/zombie/HLEAc1.png","sprites/zombie/HLEAd1.png","sprites/zombie/HLEAe1.png","sprites/zombie/HLEAf1.png","sprites/zombie/HLEAg1.png","sprites/zombie/HLEAh1.png","sprites/zombie/HLEAi1.png","sprites/zombie/HLEAj1.png",]
    zombiemove = ["sprites/zombie/HLEWa1.png","sprites/zombie/HLEWb1.png","sprites/zombie/HLEWc1.png","sprites/zombie/HLEWd1.png","sprites/zombie/HLEWe1.png","sprites/zombie/HLEWf1.png","sprites/zombie/HLEWg1.png"]
    slavedeath = ["sprites/slave/HLFDa0.png","sprites/slave/HLFDb0.png","sprites/slave/HLFDc0.png","sprites/slave/HLFDd0.png","sprites/slave/HLFDe0.png","sprites/slave/HLFDf0.png","sprites/slave/HLFDg0.png","sprites/slave/HLFDh0.png","sprites/slave/HLFDj0.png","sprites/slave/HLFDk0.png","sprites/slave/HLFDl0.png","sprites/slave/HLFDm0.png","sprites/slave/HLFDn0.png"]
    slavedistance = ["sprites/slave/HLFNa1.png","sprites/slave/HLFNb1.png","sprites/slave/HLFNc1.png","sprites/slave/HLFNd1.png","sprites/slave/HLFNe1.png","sprites/slave/HLFNf1.png",]
    slavecorpsacorps = ["sprites/slave/HLFIa1.png","sprites/slave/HLFMa1.png","sprites/slave/HLFMb1.png","sprites/slave/HLFMc1.png","sprites/slave/HLFMd1.png","sprites/slave/HLFMe1.png","sprites/slave/HLFMf1.png","sprites/slave/HLFMg1.png","sprites/slave/HLFMh1.png"]
    slavemove = ["sprites/slave/HLFWa1.png","sprites/slave/HLFWb1.png","sprites/slave/HLFWc1.png","sprites/slave/HLFWd1.png","sprites/slave/HLFWe1.png","sprites/slave/HLFWf1.png",]
    slaveball= ["sprites/slave/slave_bullet/X025A0.png","sprites/slave/slave_bullet/X025B0.png","sprites/slave/slave_bullet/X025C0.png","sprites/slave/slave_bullet/X025D0.png","sprites/slave/slave_bullet/X025E0.png","sprites/slave/slave_bullet/X025F0.png","sprites/slave/slave_bullet/X025G0.png","sprites/slave/slave_bullet/X025H0.png","sprites/slave/slave_bullet/X025I0.png","sprites/slave/slave_bullet/X025J0.png","sprites/slave/slave_bullet/X025K0.png"]
    gruntmove=["sprites/Grunt1/HK1Ra1.png","sprites/Grunt1/HK1Rb1.png","sprites/Grunt1/HK1Rc1.png","sprites/Grunt1/HK1Rd1.png","sprites/Grunt1/HK1Re1.png","sprites/Grunt1/HK1Rf1.png",]
    crowbar =[["sprites/Crowbar/crowbar1.png","sprites/Crowbar/crowbar2.png","sprites/Crowbar/crowbar3.png","sprites/Crowbar/crowbar4.png","sprites/Crowbar/crowbar5.png","sprites/Crowbar/crowbar6.png","sprites/Crowbar/crowbar7.png","sprites/Crowbar/crowbar1.png"],["sprites/Crowbar/crowbar7.png","sprites/Crowbar/crowbar8.png","sprites/Crowbar/crowbar9.png","sprites/Crowbar/crowbar10.png","sprites/Crowbar/crowbar11.png","sprites/Crowbar/crowbar12.png","sprites/Crowbar/crowbar13.png","sprites/Crowbar/crowbar14.png","sprites/Crowbar/crowbar15.png","sprites/Crowbar/crowbar7.png"],["sprites/Crowbar/crowbar15.png","sprites/Crowbar/crowbar16.png","sprites/Crowbar/crowbar17.png","sprites/Crowbar/crowbar18.png","sprites/Crowbar/crowbar19.png","sprites/Crowbar/crowbar20.png","sprites/Crowbar/crowbar21.png","sprites/Crowbar/crowbar22.png","sprites/Crowbar/crowbar23.png","sprites/Crowbar/crowbar24.png","sprites/Crowbar/crowbar25.png","sprites/Crowbar/crowbar26.png","sprites/Crowbar/crowbar27.png","sprites/Crowbar/crowbar15.png"]]
    bolt = ["sprites/M16/HW3Fa0.png","sprites/M16/HW3Fb0.png","sprites/M16/HW3Fc0.png","sprites/M16/HW3Fd0.png","sprites/M16/HW3Fe0.png","sprites/M16/HW3Ff0.png",]
    reloadbolt = ["sprites/M16/HW3Ra0.png","sprites/M16/HW3Rb0.png","sprites/M16/HW3Rc0.png","sprites/M16/HW3Rd0.png","sprites/M16/HW3Re0.png","sprites/M16/HW3Rf0.png","sprites/M16/HW3Rg0.png","sprites/M16/HW3Rh0.png","sprites/M16/HW3Ri0.png","sprites/M16/HW3Rj0.png","sprites/M16/HW3Rk0.png","sprites/M16/HW3Rl0.png","sprites/M16/HW3Rm0.png","sprites/M16/HW3Rn0.png","sprites/M16/HW3Ro0.png","sprites/M16/HW3Rp0.png","sprites/M16/HW3Rq0.png","sprites/M16/HW3Sa0.png","sprites/M16/HW3Sb0.png","sprites/M16/HW3Sc0.png","sprites/M16/HW3Sd0.png","sprites/M16/HW3Se0.png","sprites/M16/HW3Sf0.png","sprites/M16/HW3Sg0.png","sprites/M16/HW3Sh0.png","sprites/M16/HW3Si0.png",]
    gun = ["sprites/Pistol/HW2Fa0.png","sprites/Pistol/HW2Fb0.png","sprites/Pistol/HW2Fc0.png","sprites/Pistol/HW2Fd0.png","sprites/Pistol/HW2Fe0.png","sprites/Pistol/HW2Ff0.png","sprites/Pistol/HW2Fg0.png","sprites/Pistol/HW2Fh0.png","sprites/Pistol/HW2Fi0.png","sprites/Pistol/HW2Fj0.png","sprites/Pistol/HW2Fk0.png","sprites/Pistol/HW2Fl0.png","sprites/Pistol/HW2Fa0.png"]
    reloadglock = ["sprites/Pistol/HW2Ra0.png","sprites/Pistol/HW2Rb0.png","sprites/Pistol/HW2Rc0.png","sprites/Pistol/HW2Rd0.png","sprites/Pistol/HW2Re0.png","sprites/Pistol/HW2Rf0.png","sprites/Pistol/HW2Rg0.png","sprites/Pistol/HW2Rh0.png","sprites/Pistol/HW2Ri0.png","sprites/Pistol/HW2Rj0.png","sprites/Pistol/HW2Rk0.png","sprites/Pistol/HW2Rl0.png","sprites/Pistol/HW2Rm0.png","sprites/Pistol/HW2Rn0.png","sprites/Pistol/HW2Ro0.png","sprites/Pistol/HW2Rp0.png","sprites/Pistol/HW2Rq0.png","sprites/Pistol/HW2Rr0.png","sprites/Pistol/HW2Rs0.png","sprites/Pistol/HW2Rt0.png","sprites/Pistol/HW2Ru0.png","sprites/Pistol/HW2Rv0.png",]
    etatgun =1
    ammo = 10

    map_matrix = [
        [1,1,1,2,2,2,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2],
        [1,1,2,1,1,1,2,2,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,1,2,2,2,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,1,2,1,1,1,2,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,1,2,1,1,1,1,1,2,1,1,1,2,2,2,2,2,2,2,2,1,2,1,1,2,1,1,1,1,1,2],
        [1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,2,1,1,1,1,1,2],
        [1,1,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2,2,1,2,2,2,1,2,1,1,1,1,1,2],
        [1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,2,2,2,2],
        [1,1,1,1,1,2,1,2,2,2,2,2,2,2,2,2,2,2,2,1,2,1,1,1,1,1,1,1,1,2,2,1,1,1,1,1,1,1,1,2],
        [1,1,1,2,2,2,1,2,1,1,1,1,1,2,1,1,1,1,1,1,2,2,2,2,2,2,2,2,1,2,2,1,1,1,1,1,1,1,1,2],
        [1,1,1,2,1,1,1,2,2,2,2,2,2,2,1,1,1,1,1,1,2,1,1,1,1,1,1,2,1,2,2,1,1,1,1,1,1,1,1,2],
        [1,2,2,2,1,2,1,1,1,1,1,1,2,2,1,1,1,1,1,1,2,1,1,1,1,1,2,2,1,2,2,1,1,1,1,1,1,1,1,2],
        [2,1,1,1,1,2,2,2,2,2,2,1,2,2,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,2,1,1,1,1,1,1,1,1,2],
        [1,2,2,2,1,2,1,1,1,1,2,1,2,2,1,1,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1,1,1,2],
        [1,1,1,2,1,2,1,1,1,1,2,1,2,2,1,1,1,1,1,1,2,2,2,2,2,2,2,1,1,1,2,1,1,1,1,1,1,1,1,2],
        [1,1,1,2,1,2,2,2,1,1,2,1,2,2,1,1,1,1,1,1,2,2,1,1,1,1,2,2,1,2,1,1,1,1,1,1,1,1,1,2],
        [1,1,1,2,1,1,1,2,1,1,2,1,2,2,2,2,2,2,1,2,2,2,1,2,1,1,2,2,1,2,2,1,1,1,1,1,1,1,1,2],
        [1,1,1,2,2,2,1,2,2,1,2,1,2,1,1,1,1,2,1,1,1,1,1,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,2],
        [1,1,1,1,2,1,1,1,2,2,2,1,2,2,2,2,2,2,1,2,2,2,2,2,1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,2],
        [1,1,1,1,2,1,1,1,1,1,2,1,2,2,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2],
        [1,1,1,1,2,1,1,1,2,2,2,1,2,2,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2],
        [1,1,1,1,2,2,2,2,2,1,2,1,1,1,1,1,1,1,1,1,2,1,1,2,1,1,1,1,1,1,2],
        [1,1,1,1,1,1,1,1,1,1,2,2,2,2,2,2,2,2,2,2,2,1,1,2,2,2,2,2,2,2,2],


    ]



    viewer = ViewerGL(gun,etatgun,ammo,reloadglock,bolt,reloadbolt,crowbar,slavemove,slavedistance,map_matrix,slavecorpsacorps,zombieattack,zombiemove,slavedeath)
    viewer.set_camera(Camera())
    viewer.cam.transformation.translation.y = 2
    viewer.cam.transformation.translation.x = 2
    viewer.cam.transformation.translation.z = 28
    viewer.cam.transformation.rotation_center = viewer.cam.transformation.translation.copy()

    program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
    programGUI_id = glutils.create_program_from_file('gui.vert', 'gui.frag')
    programIMG_id= glutils.create_program_from_file('image.vert', 'image.frag')






    cube = Mesh.load_obj('cube.obj')
    cube_width = np.amax(cube.vertices, axis=0)[0] - np.amin(cube.vertices, axis=0)[0]
    cube_depth = np.amax(cube.vertices, axis=0)[2] - np.amin(cube.vertices, axis=0)[2]
    cube.normalize()
    cube.apply_matrix(pyrr.matrix44.create_from_scale([1, 2, 1, 1]))





    texture_paths = {
    0: 'grass.jpg',
    2: 'murblanc.png',
    }

    textures = {}
    for value, path in texture_paths.items():
        textures[value] = glutils.load_texture(path)
 

    for row in range(len(map_matrix)):
        for col in range(len(map_matrix[row])):
            if map_matrix[row][col] == 2:
                texture = textures[2]
                tr = Transformation3D()
                tr.translation.x = col * cube_width
                tr.translation.y = -np.amin(cube.vertices, axis=0)[1] 
                tr.translation.z = row * cube_depth
                tr.rotation_center.z = 0.2
                o = Object3D(cube.load_to_gpu(), cube.get_nb_triangles(), program3d_id, texture, tr)
                viewer.add_object(o)






    m = Mesh()
    p0, p1, p2, p3 = [-1, 0, 50], [60, 0, 50], [60, 0, 0], [-1, 0, 0]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [30, 0], [30, 30], [0, 30] 
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('tilefinale.png')
    o = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    viewer.add_object(o)#318

    p0, p1, p2, p3 = [-1, 4, 50], [60, 4, 50], [60, 4, 0], [-1, 4, 0]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [30, 0], [30, 30], [0, 30] 
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)
    texture = glutils.load_texture('Xplaf.png') 
    plafondobj = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, Transformation3D())
    plafondobj.transformation.translation.x = 100
    viewer.add_object(plafondobj)


    # Variables carré méchant 2D
    p0, p1, p2, p3 = [1.5, 0, 1.5], [0, 0, 0], [0, 2.5, 0], [1.5, 2.5, 1.5]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    # Définition carré
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)

    # Define the center position of the square
    square_center = np.array([0.75, 0, 0.75]) 


    square_center = square_center.reshape((1, 1, 3))
    m.vertices[..., :3] -= square_center

    # Ajout texture
    texturevorti = glutils.load_texture("sprites/Grunt1/HK1Ba0.png")
    texturezombie = glutils.load_texture("sprites/zombie/HLEAa1.png")
    vorti = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texturevorti, Transformation3D())
    zombard1 = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texturezombie, Transformation3D())
    zombard2 = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texturezombie, Transformation3D())

    vorti.transformation.translation.x = 62
    vorti.transformation.translation.z = 30
    viewer.add_object(vorti)#319
    #viewer.add_object(zombard1)
    #viewer.add_object(zombard2)

    p0, p1, p2, p3 = [0.5, 0, 0.5], [0, 0, 0], [0, 1, 0], [0.5, 1, 0.5]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    # Définition carré
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)

    # Define the center position of the square
    square_center = np.array([0.25, 0, 0.25])

    square_center = square_center.reshape((1, 1, 3))
    m.vertices[..., :3] -= square_center

    # Ajout texture
    texturepistol = glutils.load_texture("sprites/DEPIA0.png")
    spritegun = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texturepistol, Transformation3D())
    spritegun.transformation.translation.x = 7
    spritegun.transformation.translation.z = 5
    texturem16 = glutils.load_texture("sprites/M16.png")
    texturebullet = glutils.load_texture("sprites/slave/slave_bullet/X025A0.png")


    viewer.add_object(spritegun)#320

    spritem16 = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texturem16, Transformation3D())
    spritem16.transformation.translation.x = 55
    spritem16.transformation.translation.z = 5

    spritebullet = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texturebullet, Transformation3D())
    spritebullet.transformation.translation.x = 100

    viewer.add_object(spritem16)#321
    viewer.add_object(spritebullet)#322



    p0, p1, p2, p3 = [0, 0, -1], [0, 4, -1], [0, 4, 1], [0, 0, 1]
    n, c = [0, 1, 0], [1, 1, 1]
    t0, t1, t2, t3 = [0, 0], [1, 0], [1, 1], [0, 1]
    # Définition carré
    m.vertices = np.array([[p0 + n + c + t0], [p1 + n + c + t1], [p2 + n + c + t2], [p3 + n + c + t3]], np.float32)
    m.faces = np.array([[0, 1, 2], [0, 2, 3]], np.uint32)

    # Ajout texture


    textureportail = glutils.load_texture("portail.png")
    portailobj = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, textureportail, Transformation3D())
    portailobj.transformation.translation.x = -157
    viewer.add_object(portailobj)#323

    vao = Image.initialize_geometry()
    texture = glutils.load_texture("sprites/Crowbar/crowbar1.png")
    o_gun = Image("sprites/Crowbar/crowbar1.png", np.array([-0.7, -1], np.float32), np.array([0.7, 0.8], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o_gun)#-7

    o_texture = glutils.load_texture(crowbar[0][0])
    viewer.update_object_texture(328, o_texture)  # Assuming the gun object is at index 3


    texture = glutils.load_texture("crosshair.png")
    o_crosshair = Image("crosshair.png", np.array([-0.02, -0.05], np.float32), np.array([0.02, 0.05], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o_crosshair)

    o_texture = glutils.load_texture("crosshair.png")
    viewer.update_object_texture(329, o_texture)  # Assuming the crosshair object is at index 2


    texture = glutils.load_texture("i_health.png")
    o = Image("i_health.png", np.array([-0.95, -1], np.float32), np.array([-0.85, -0.7], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o)

    texture = glutils.load_texture("i_bul3.png")
    o = Image("i_bul3.png", np.array([0.55, -0.95], np.float32), np.array([0.65, -0.7], np.float32), vao, 2, programIMG_id, texture)
    viewer.add_object(o)

    vao = Text.initalize_geometry()
    texture = glutils.load_texture('fontB.jpg')
    #o = Text('HP :', np.array([-1, -0.95], np.float32), np.array([-0.75,-0.8], np.float32), vao, 2, programGUI_id, texture)
    o_lifevalue = Text('100', np.array([-0.75, -1], np.float32), np.array([-0.60,-0.75], np.float32), vao, 2, programGUI_id, texture)
    #o_ammo = Text('MUN :', np.array([0.45, -0.95], np.float32), np.array([0.65,-0.8], np.float32), vao, 2, programGUI_id, texture)
    o_ammovalue = Text('0', np.array([0.7, -0.95], np.float32), np.array([0.8,-0.8], np.float32), vao, 2, programGUI_id, texture)
    #viewer.add_object(o)
    viewer.add_object(o_lifevalue)
    #viewer.add_object(o_ammo)
    viewer.add_object(o_ammovalue)
    viewer.run()

if __name__ == '__main__':
    main()



