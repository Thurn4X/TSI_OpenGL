    #!/usr/bin/env python3
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D,Transformation3D,Image,Text
from pyrr import Matrix44, Vector3
import glutils
import pygame
from math import *
import random
import time
from mesh import Mesh
pygame.mixer.init(frequency = 44100, size = -16, channels = 3, buffer = 1012)
pygame.mixer.Channel(0).set_volume(0.5)


class ViewerGL:
    def __init__(self, gun ,etatgun,ammo,reloadglock,m16,reloadm16,crowbar,gruntmove,gruntidle,map_matrix,slavecorpsacorps,zombieattack,zombiemove,slavedeath):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(1280, 700, 'DA GAME', None, None)
        # paramétrage de la fonction de gestion des évènements
        glfw.set_key_callback(self.window, self.key_callback)
        glfw.set_cursor_pos_callback(self.window, self.mouse_callback)
        glfw.set_mouse_button_callback(self.window, self.mouse_button_callback)
        # activation du context OpenGL pour la fenêtre
        glfw.make_context_current(self.window)
        glfw.swap_interval(1)
        # activation de la gestion de la profondeur
        GL.glEnable(GL.GL_DEPTH_TEST)



        # choix de la couleur de fond
        GL.glClearColor(0.5, 0.6, 0.9, 1.0)
        self.touch = set()
        self.objs = []
        self.key_pressed = {}
        # pour la souris
        self.prev_mouse_pos = None
        self.mouse_sensitivity = 0.001
        #tous le reste (gros bazar)
        self.life = 100
        self.nbbullet = 0
        self.gun = gun
        self.gruntmove = gruntmove
        self.gruntidle = gruntidle
        self.slavecorpsacorps = slavecorpsacorps
        self.creationbullet = False
        self.crowbar = crowbar
        self.crowbar_indice = 0
        self.reloadglock = reloadglock
        self.m16 = m16
        self.reloadm16 = reloadm16
        self.reloading = False
        self.etatgun = etatgun
        self.texture_change_delay_fire = 0.01
        self.texture_change_delay_reload = 0.05
        self.enemy_texture_delay = 0.2
        self.enemyattack = False
        self.last_frame_index = -1
        self.current_change_delay = self.texture_change_delay_fire
        self.last_texture_change_time = glfw.get_time()  # Set the initial time to the current time
        self.gun_index = 0  # Index of the current gun texture
        self.is_texture_loop_active = False  # Flag indicating if the texture change loop is active
        self.left_mouse_button_pressed = False  # Flag indicating if the left mouse button is pressed
        self.mouse_buttons = []
        self.ammo = ammo
        self.m16ammo = 30
        self.current_texture_list = self.crowbar[self.crowbar_indice]  # Initialize with the gun texture list
        self.weapon = "crowbar"
        self.usedammo = 10
        self.listeammo=[0,10,30]
        self.descente =1#variable saut
        self.ensaut = False
        self.translation_jump=0.1
        self.tinit=0#temps début du saut
        self.ennemiposition=[[[2, 0, 2],[0, 0, 0], [0, 3, 0], [2, 3, 2]]]#liste de l'ennemi avec sa position
        self.last_sound_play_time = 0
        self.sound_delay = 0.5
        self.last_attack_time = 0.0 #temps d'attaque de l'ennemi
        self.attaqueencours = False
        self.attaquedistance = False
        self.enemy_index = 0
        self.start_time = 0
        self.map_matrix = map_matrix
        self.sound_channel = None
        self.angle = 0
        self.inventory = ["crowbar"]
        self.zombieattack = zombieattack
        self.zombiemove = zombiemove
        self.creationbullet = False
        self.bullet_textures = ["sprites/slave/slave_bullet/X025A0.png","sprites/slave/slave_bullet/X025B0.png","sprites/slave/slave_bullet/X025C0.png","sprites/slave/slave_bullet/X025D0.png","sprites/slave/slave_bullet/X025E0.png","sprites/slave/slave_bullet/X025F0.png","sprites/slave/slave_bullet/X025G0.png","sprites/slave/slave_bullet/X025H0.png","sprites/slave/slave_bullet/X025I0.png","sprites/slave/slave_bullet/X025J0.png"]
        self.translation_speed = 0.4
        self.enemyhit = False
        self.enemylife = 10
        self.enemienvie = True
        self.frame_index = 0
        self.mortfinie = False
        self.slavedeath = slavedeath
        """
        program3d_id = glutils.create_program_from_file('shader.vert', 'shader.frag')
        m = Mesh.load_obj('cube.obj')
        m.normalize()
        m.apply_matrix(pyrr.matrix44.create_from_scale([2, 2, 2, 1]))
        tr = Transformation3D()
        tr.translation.y = -np.amin(m.vertices, axis=0)[1]
        tr.translation.z = -5
        tr.rotation_center.z = 0.2
        texture = glutils.load_texture('doom_voxel_marines.png')
        self.ballobject = Object3D(m.load_to_gpu(), m.get_nb_triangles(), program3d_id, texture, tr)
        """


    def run(self):
        #paramètres parabole pour le saut
        alpha=-6
        beta=1.5
        global etatgun
        # hide the cursor
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        self.choixammo()
        self.last_enemy_texture_change_time = glfw.get_time()

        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)
            self.update_key()
            self.update_mouse_button()
            etatgun = 0
            self.update_gui()
            self.fire()
            self.check_enemy_distance()
            self.bulletmovement()
            self.tirtouche()
            self.tournerleserviettes()
            self.sound_distance()
            self.change_vorti_hit()
            self.enemi_death_anim()
            self.check_position(self.cam.transformation.translation, self.map_matrix)
            if self.ensaut:
                    self.cam.transformation.translation.y = alpha*(glfw.get_time()-self.tinit-0.5)**2 + beta +2
                    if self.cam.transformation.translation.y <= 2:
                        self.ensaut= False

            if self.is_texture_loop_active:
                # Calculate the time elapsed since the last texture change
                current_time = glfw.get_time()
                elapsed_time = current_time - self.last_texture_change_time

                # Check if enough time has passed for the next texture change
                if elapsed_time >= self.current_change_delay:
                    self.change_gun_texture(self.current_texture_list)  # Pass the gun texture list
                    self.last_texture_change_time = current_time


            for obj in self.objs:
                GL.glUseProgram(obj.program)
                obj.draw()
            self.update_camera(self.objs[0].program)
                



            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()
    
        
    def check_position(self, viewer_position, map_matrix):
        cube = Mesh.load_obj('cube.obj')
        cube_width = np.amax(cube.vertices, axis=0)[0] - np.amin(cube.vertices, axis=0)[0]
        cube_height = np.amax(cube.vertices, axis=0)[1] - np.amin(cube.vertices, axis=0)[1]
        cube_depth = np.amax(cube.vertices, axis=0)[2] - np.amin(cube.vertices, axis=0)[2]

        viewer_offset_x = cube_width / 2.0
        viewer_offset_z = cube_depth / 2.0

        row = int((viewer_position.z + viewer_offset_z) / cube_depth)  # Calculate the row based on the viewer's position
        col = int((viewer_position.x + viewer_offset_x) / cube_width)  # Calculate the column based on the viewer's position

        #print("Viewer Position:", viewer_position)
        #print("Row:", row)
        #print("Column:", col)

        if row >= 0 and row < len(map_matrix) and col >= 0 and col < len(map_matrix[row]):
            if map_matrix[row][col] == 2:
                #print("I am on a 2")
                return False

        return True






    
    def add_object(self, obj):
        self.objs.append(obj)

    def set_camera(self, cam):
        self.cam = cam

    def update_camera(self, prog):
        GL.glUseProgram(prog)
        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "translation_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_view")
        # Modifie la variable pour le programme courant
        translation = -self.cam.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(prog, "rotation_center_view")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_view")
        # Modifie la variable pour le programme courant
        rotation_center = self.cam.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(-self.cam.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(prog, "rotation_view")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_view")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)
    
        loc = GL.glGetUniformLocation(prog, "projection")
        if (loc == -1) :
            print("Pas de variable uniforme : projection")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, self.cam.projection)


    def key_callback(self, win, key, scancode, action, mods):
        # Set the flag when a key is pressed
        if action == glfw.PRESS:
            self.key_pressed[key] = True
        # Clear the flag when a key is released
        elif action == glfw.RELEASE:
            if key in self.key_pressed:
                del self.key_pressed[key]


    def update_key(self):
        sons = ["sounds/pl_tile1.wav","sounds/pl_tile2.wav","sounds/pl_tile3.wav","sounds/pl_tile4.wav","sounds/pl_tile5.wav"]
        index = random.randint(0,4)
        step_sound = sons[index]

        translation_speed = 0.4
        rotation_speed = 0.1

        # Update camera transformation based on pressed keys
        for key in self.key_pressed:
            if self.sound_channel is None or not self.sound_channel.get_busy() and not self.ensaut:
                self.sound_channel = pygame.mixer.find_channel()
                self.sound_channel.fadeout(1000) 
                self.sound_channel.play(pygame.mixer.Sound(step_sound))

            if key == glfw.KEY_I:
                self.creationbullet= True
                self.createenemybullet()
                print("creation bullet")
                #self.cam.transformation.rotation_euler[0] -= rotation_speed  # Negate rotation
            elif key == glfw.KEY_K:
                self.cam.transformation.rotation_euler[0] += rotation_speed  # Negate rotation
            elif key == glfw.KEY_J:
                self.cam.transformation.rotation_euler[2] -= rotation_speed  # Negate rotation
            elif key == glfw.KEY_L:
                self.cam.transformation.rotation_euler[2] += rotation_speed  # Negate rotation
            
            if key == glfw.KEY_2:
                if "glock" in self.inventory:
                    self.weapon = "glock"
                    self.current_texture_list = self.gun
                    texture = glutils.load_texture("sprites/Pistol/HW2Fa0.png")
                    self.update_object_texture(-6, texture)
                    self.choixammo()
            elif key == glfw.KEY_3:
                self.weapon = "crowbar"
                self.current_texture_list = self.crowbar[self.crowbar_indice]
                texture = glutils.load_texture("sprites/Crowbar/crowbar1.png")
                self.update_object_texture(-6, texture)
                self.choixammo()
            
            elif key == glfw.KEY_1:
                if "m16" in self.inventory:
                    self.weapon = "m16"
                    self.choixammo()
                    self.current_texture_list = self.crowbar[self.crowbar_indice]
                    texture = glutils.load_texture("sprites/M16/HW3Fa0.png")
                    self.update_object_texture(-6, texture)


        # Get the forward direction by transforming the default forward vector with the rotation matrix
        forward = pyrr.Vector3([0, 0, 1])  # Negate forward vector
        rotation = pyrr.matrix33.create_from_eulers(-self.cam.transformation.rotation_euler)  # Negate rotation
        forward = rotation @ forward
        forward.y = 0.0  # Set the y component to 0
        forward = pyrr.vector.normalise(forward)

        # Calculate the right direction by taking the cross product of the forward vector and the up vector
        up = pyrr.Vector3([0, 1, 0])
        right = pyrr.vector3.cross(forward, up)
        right = pyrr.vector.normalise(right)

        # Update camera transformation based on pressed keys
        for key in self.key_pressed:
            if key == glfw.KEY_W or key == glfw.KEY_UP:
                if self.check_position(self.cam.transformation.translation - forward * translation_speed, self.map_matrix):
                    self.cam.transformation.translation -= forward * translation_speed
            elif key == glfw.KEY_S or key == glfw.KEY_DOWN:
                if self.check_position(self.cam.transformation.translation + forward * translation_speed, self.map_matrix):
                    self.cam.transformation.translation += forward * translation_speed
            elif key == glfw.KEY_A or key == glfw.KEY_LEFT:
                if self.check_position(self.cam.transformation.translation + right * translation_speed, self.map_matrix):
                    self.cam.transformation.translation += right * translation_speed
            elif key == glfw.KEY_D or key == glfw.KEY_RIGHT:
                if self.check_position(self.cam.transformation.translation - right * translation_speed, self.map_matrix):
                    self.cam.transformation.translation -= right * translation_speed

            elif key == glfw.KEY_Q:
                self.cam.transformation.translation += pyrr.Vector3([0, translation_speed, 0])
            elif key == glfw.KEY_E:
                self.cam.transformation.translation -= pyrr.Vector3([0, translation_speed, 0])
            elif key == glfw.KEY_SPACE:
                if self.ensaut == False:
                    self.tinit=glfw.get_time()#temps début du saut
                    self.ensaut = True

                    

        # Update camera's rotation center based on its translation
        self.cam.transformation.rotation_center = self.cam.transformation.translation.copy()


    def mouse_button_callback(self, win, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            if self.reloading == False and not self.is_texture_loop_active:              
                if self.weapon == "glock":
                    if self.usedammo > 0:
                        pygame.mixer.Channel(0).fadeout(0)  # Stop the previous sound (fade out over 100 milliseconds)
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/pistol_fire1.wav'))
                    else:
                        pygame.mixer.Channel(0).fadeout(0)
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/DRY.ogg'))

                elif self.weapon == "m16":
                    if self.usedammo >0:
                        pygame.mixer.Channel(0).fadeout(0)  # Stop the previous sound (fade out over 100 milliseconds)
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/bolt_fire.ogg'))
                    else:
                        self.reload()
                elif self.weapon == "crowbar":
                    pygame.mixer.Channel(0).fadeout(0)  # Stop the previous sound (fade out over 100 milliseconds)
                    pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/cbar_miss1.wav'))



        if action == glfw.PRESS:
            self.mouse_buttons.append(button)
        elif action == glfw.RELEASE and button in self.mouse_buttons:
            self.mouse_buttons.remove(button)


    def update_mouse_button(self):
        if self.left_mouse_button_pressed and not self.is_texture_loop_active:
            self.change_gun_texture(self.current_texture_list)  # Change the texture immediately
            self.last_texture_change_time = glfw.get_time()  # Update the last texture change time
            self.is_texture_loop_active = True  # Set the flag to start the texture change loop

    def mouse_callback(self, win, xpos, ypos):
        window_width, window_height = glfw.get_window_size(self.window)
        center_x = window_width // 2
        center_y = window_height // 2

        if self.prev_mouse_pos is None:
            self.prev_mouse_pos = (center_x, center_y)

        dx = xpos - self.prev_mouse_pos[0]
        dy = ypos - self.prev_mouse_pos[1]

        self.prev_mouse_pos = (center_x, center_y)

        dx *= self.mouse_sensitivity
        dy *= self.mouse_sensitivity

        # Update the rotation only if it's within the limits
        if self.cam.transformation.rotation_euler[0] + dy <= np.pi / 2 and self.cam.transformation.rotation_euler[0] + dy >= -np.pi / 2:
            self.cam.transformation.rotation_euler[0] += dy  # Inverted rotation

        self.cam.transformation.rotation_euler[2] += dx  # Inverted rotation

        # Restrict cursor movement to stay inside the window
        glfw.set_cursor_pos(self.window, center_x, center_y)

    def update_object_texture(self, obj_index, texture):
        if obj_index < len(self.objs):
            obj = self.objs[obj_index]
            obj.texture = texture

    def choixammo(self):
        if self.weapon == "glock":
            self.usedammo = self.listeammo[1]
        elif self.weapon == "m16":
            self.usedammo = self.listeammo[2]
        elif self.weapon == "crowbar":
            self.usedammo = self.listeammo[0]

    def fire(self):
        #print(self.listeammo)
        if self.reloading == False:
            if self.usedammo > 0 or self.weapon == "crowbar":
                for button in self.mouse_buttons:
                    if button == glfw.MOUSE_BUTTON_LEFT and not self.is_texture_loop_active:
                        self.current_change_delay = self.texture_change_delay_fire
                        if self.weapon == "glock":
                            self.listeammo[1] -= 1
                            self.usedammo = self.listeammo[1]
                            self.current_texture_list = self.gun
                        elif self.weapon == "m16":
                            self.listeammo[2] -= 1
                            self.usedammo = self.listeammo[2]
                            self.current_texture_list = self.m16
                        elif self.weapon == "crowbar":
                            #print("la crowbar frappe")
                            self.current_texture_list = self.crowbar[self.crowbar_indice]
                            self.crowbar_indice +=1
                            if self.crowbar_indice >2:
                                self.crowbar_indice = 0
                        if self.tirtouche():
                            #print("TU AS TIRE SUR L'ENNEMI")
                            self.enemyhit = True
                            self.last_hit_time = time.time()
                            self.change_vorti_hit()
                        self.change_gun_texture(self.current_texture_list)   
                        self.last_texture_change_time = glfw.get_time()
                        self.is_texture_loop_active = True
                        
            if self.usedammo == 0:
                if self.weapon == "glock":
                    self.listeammo[1] = self.ammo
                    self.usedammo = self.listeammo[1]
                    self.reload()
                elif self.weapon == "m16":
                    self.listeammo[2] = self.m16ammo
                    self.usedammo = self.listeammo[2]
                    self.reload()

    def enemi_death_anim(self):
        if not self.enemienvie:
            if not self.mortfinie:

                print("ennemi est mort")
                self.frame_index  +=1
                texture_path = self.slavedeath[self.frame_index]
                texture = glutils.load_texture(texture_path)
                self.update_object_texture(-11,texture)
                if self.frame_index == len(self.slavedeath)-1:
                    positionportail = self.objs[-11].transformation.translation
                    self.objs.pop(-11)
                    self.mortfinie = True
                    self.objs[-7].transformation.translation= positionportail

        



    def change_vorti_hit(self):
        if self.enemienvie:
            if self.enemyhit:
                
                print(self.enemylife)
                if self.enemylife <= 0:

                    self.enemienvie = False
                    self.enemi_death_anim()
                self.update_object_texture(-11, glutils.load_texture("sprites/slave/HLFPa1.png"))
                if self.enemyhit:
                    self.update_object_texture(-11, glutils.load_texture("sprites/slave/HLFPa1.png"))
                    current_time = time.time()
                    elapsed_time = current_time - self.last_hit_time
                    #print("lepased time: ", elapsed_time)

                    if elapsed_time >= 0.5:
                        self.enemyhit = False
                        self.last_hit_time = current_time

    def reload(self):
        
        self.reloading = True
        self.current_change_delay = self.texture_change_delay_reload
        if self.weapon == "glock":           
            sound_clipout = pygame.mixer.Sound('sounds/CLIPOUT.ogg')
            sound_clipin = pygame.mixer.Sound('sounds/CLIPIN.ogg')
            chan1 = pygame.mixer.find_channel()
            chan1.queue(sound_clipout)
            chan1.queue(sound_clipin)
            self.current_texture_list = self.reloadglock
  


        elif self.weapon == "m16":
            sound_clipout = pygame.mixer.Sound('sounds/CLIPOUT.ogg')
            sound_clipin = pygame.mixer.Sound('sounds/CLIPIN.ogg')
            chan1 = pygame.mixer.find_channel()
            chan1.queue(sound_clipout)
            chan1.queue(sound_clipin)
            self.current_texture_list = self.reloadm16

        elif self.weapon == "crowbar":
            pass
        
        self.change_gun_texture(self.current_texture_list)
        self.last_texture_change_time = glfw.get_time()
        self.is_texture_loop_active = True

    def change_gun_texture(self, texture_list=None):
        if texture_list is None:
            texture_list = self.current_texture_list

        if self.gun_index < len(texture_list):
            texture_path = texture_list[self.gun_index]
            texture = glutils.load_texture(texture_path)
            self.update_object_texture(-6, texture)  # Assuming the gun object is at index 3
            ##print("changement de texture")
            self.gun_index += 1

        if self.gun_index >= len(texture_list):
            self.gun_index = 0  # Reset the index to loop back to the beginning
            self.reloading = False
            self.is_texture_loop_active = False  # Stop the texture change loop
        
###
    #def ennemis(self):
        #angle=np.arctan(self.cam.transformation.translation.z/self.cam.transformation.translation.x) #angle de la rotation
        #différent cas de rotation selon le signe des axes
        #if self.cam.transformation.translation.x>0 and self.cam.transformation.translation.z>0: 
         #   rotation=[[cos(angle),0,sin(angle)],[0,1,0],[-sin(angle),0,cos(angle)]]
          #  for i in range (0,3):
           #     self.ennemiposition[0][i]=np.dot(self.ennemiposition[0][i],rotation)
        #if self.cam.transformation.translation.x<0 and self.cam.transformation.translation.z>0:
         #   rotation=[[cos(angle+(1/2)*pi),0,sin(angle+(1/2)*pi)],[0,1,0],[-sin(angle+(1/2)*pi),0,cos(angle+(1/2)*pi)]]
          #  for i in range (0,3):
           #     self.ennemiposition[0][i]=np.dot(self.ennemiposition[0][i],rotation)
        #if self.cam.transformation.translation.x>0 and self.cam.transformation.translation.z<0:
         #   rotation=[[cos(angle+(3/2)*pi),0,sin(angle+(3/2)*pi)],[0,1,0],[-sin(angle+(3/2)*pi),0,cos(angle+(3/2)*pi)]]
          #  for i in range (0,3):
           #     self.ennemiposition[0][i]=np.dot(self.ennemiposition[0][i],rotation)
        #if self.cam.transformation.translation.x<0 and self.cam.transformation.translation.z<0:
         #   rotation=[[cos(angle+pi),0,sin(angle+pi)],[0,1,0],[-sin(angle+pi),0,cos(angle+pi)]]
          #  for i in range (0,3):
           #     self.ennemiposition[0][i]=np.dot(self.ennemiposition[0][i],rotation)

    ###
    def ennemis(self):
        if self.enemienvie:
            # Get the enemy's position
            enemy_position = self.objs[-11].transformation.translation  # Assuming the enemy object is at index 0 in the objs list

            # Get the camera's position
            camera_position = self.cam.transformation.translation

            # Calculate the angle between the enemy and the camera
            angle = np.arctan2(camera_position[0] - enemy_position[0], camera_position[2] - enemy_position[2])

            # Update the enemy object's rotation around the y-axis
            self.objs[-11].transformation.rotation_euler[pyrr.euler.index().yaw] = -angle

            # Define the speed at which the enemy moves towards the camera
            speed = 0.1

            # Calculate the direction from the enemy to the camera
            direction = camera_position - enemy_position

            # Normalize the direction vector
            direction = direction / np.linalg.norm(direction)

            # Calculate the enemy's new position by moving towards the camera
            new_position = enemy_position + direction * speed
            if new_position.x > 70 or new_position.x < 61 or new_position.z> 40 or new_position.z <20:
                #print("l'ennemi a atteint ses limites")
                new_position = self.objs[-11].transformation.translation
            # Adjust the new position to stay grounded on the y-axis (assuming ground level is at y=0)
            new_position[1] = 0

            # Check if the new position is valid (not on a "2" in the map matrix)
            if self.check_position(new_position, self.map_matrix):
                # Update the enemy's translation with the new position
                self.objs[-11].transformation.translation = new_position
            else:
                # Handle the case where the new position is invalid (on a "2" in the map matrix)
                # For example, you could stop the enemy or make it choose a different direction.
                # You can add your custom logic here.
                pass


    def enemy_animation(self):
        if self.enemienvie:

            if not self.enemyhit:
                current_time = glfw.get_time()
                distance_traveled = self.objs[-11].transformation.translation.length

                frame_index = 0  # Initialize frame_index with a default value

                if not self.enemyattack:
                    print("not enemyattack")
                    frame_index = int(distance_traveled / self.enemy_texture_delay) % len(self.gruntmove)
                    texture_path = self.gruntmove[frame_index]
                else:
                    print("enemyattack")
                    frame_index_idle = int(current_time / self.enemy_texture_delay) % len(self.slavecorpsacorps)
                    texture_path = self.slavecorpsacorps[frame_index_idle]

                if frame_index != self.last_frame_index or self.enemyattack:
                    texture = glutils.load_texture(texture_path)
                    self.update_object_texture(-11, texture)  # Assuming the enemy object is at index 0
                    self.last_frame_index = frame_index

                self.last_enemy_texture_change_time = current_time

    

    def change_enemy_texture(self, texture_list=None):
        if self.enemienvie:
            if not self.enemyhit:
                if texture_list is None:
                    texture_list = self.gruntidle

                frame_index = self.enemy_index // len(texture_list)  # Calculate the current frame index

                if frame_index < len(texture_list):
                    texture_path = texture_list[frame_index]
                    texture = glutils.load_texture(texture_path)
                    self.update_object_texture(-11, texture)  # Assuming the enemy object is at index -12

                self.enemy_index += 1

                if frame_index == len(texture_list) - 1:
                    self.enemy_index = 0  # Reset the index to loop back to the beginning
                    self.creationbullet = True
                    self.createenemybullet()
                    self.sound_channel.play(pygame.mixer.Sound("sounds/zap1.wav"))
                    self.attaquedistance = False  # Stop further animation when the last frame is reached


    def check_enemy_distance(self):
        if self.enemienvie:
            enemy_position = self.objs[-11].transformation.translation
            camera_position = self.cam.transformation.translation
            distance = np.linalg.norm(enemy_position - camera_position)
            #print(self.attaquedistance)
            if  distance > 15:
                self.enemy_animation()
                self.ennemis()
                #print("TROP LOIN")
                self.enemyattack = False
            elif 5 <= distance <= 15:
                enemy_position = self.objs[-11].transformation.translation
                camera_position = self.cam.transformation.translation
                angle = np.arctan2(camera_position[0] - enemy_position[0], camera_position[2] - enemy_position[2])
                self.objs[-11].transformation.rotation_euler[pyrr.euler.index().yaw] = -angle

                if not self.attaquedistance:
                    self.attaquedistance = True
                    self.start_time = glfw.get_time()  # Update the start_time here
                    self.enemy_index = 0  # Reset the enemy_index when attack distance begins

                if self.attaquedistance:
                    current_time = glfw.get_time()
                    elapsed_time = current_time - self.start_time
                    self.change_enemy_texture()
                    
            else:
                
                self.enemyattack = True
                print("je set l'attauqe sur true")


                self.enemy_animation()
                
                enemy_position = self.objs[-11].transformation.translation

                # Get the camera's position
                camera_position = self.cam.transformation.translation

                # Calculate the angle between the enemy and the camera
                angle = np.arctan2(camera_position[0] - enemy_position[0], camera_position[2] - enemy_position[2])

                # Update the enemy object's rotation around the y-axis
                self.objs[-11].transformation.rotation_euler[pyrr.euler.index().yaw] = -angle
                #print("je fais tourner lenemi")
                frame_index_idle = int(glfw.get_time() / self.enemy_texture_delay) % len(self.slavecorpsacorps)
                #texture_path = self.slavecorpsacorps[frame_index_idle]
                #texture = glutils.load_texture(texture_path)
                #self.update_object_texture(-11, texture)


            





    def tirtouche(self):
        if self.enemienvie:

            # Assuming you have a camera object with a transformation matrix
            rotation = pyrr.matrix33.create_from_eulers(-self.cam.transformation.rotation_euler)  # Negate rotation

            # Get the forward direction vector in the world space
            forward_direction = rotation @ pyrr.Vector3([0, 0, -1])

            # Normalize the forward direction vector
            forward_direction = forward_direction / np.linalg.norm(forward_direction)

            enemy_position = self.objs[-11].transformation.translation
            camera_position = self.cam.transformation.translation
            distance = np.linalg.norm(enemy_position - camera_position)

            # Calculate the vector from the camera to the enemy, ignoring the Y component
            enemy_direction = enemy_position - camera_position
            enemy_direction[1] = 0  # Set Y component to zero

            # Normalize the enemy direction vector
            enemy_direction = enemy_direction / np.linalg.norm(enemy_direction)

            # Calculate the angle between the enemy direction and the forward direction
            angle = np.arccos(np.dot(enemy_direction, forward_direction))

            # Convert the angle from radians to degrees
            angle_degrees = np.degrees(angle)


            threshold = 60 / distance # Adjust the factors as needed

            if angle_degrees <= threshold:
                #print("I'M ON THE TARGET")
                if self.weapon != "crowbar":
                    self.enemylife -= 10
                    return True
                else:
                    if distance <= 3:
                        self.enemylife -= 1
                        return True
                    else:
                        return False


            else:
                #print("I'm not")
                return False




    def tournerleserviettes(self):


        if self.angle  >= 360:
            self.angle = 0
        self.angle +=0.5
        self.objs[-10].transformation.rotation_euler[pyrr.euler.index().yaw] = self.angle
        self.objs[-9].transformation.rotation_euler[pyrr.euler.index().yaw] = self.angle


        glock_position = self.objs[-10].transformation.translation
        m16_position = self.objs[-9].transformation.translation
        camera_position = self.cam.transformation.translation
        if not "m16" in self.inventory:
            distance_m16 = np.linalg.norm(m16_position - camera_position)
            if distance_m16 <= 2.5:
                sound = pygame.mixer.Sound("sounds/DSITEMUP.wav")
                sound.play()
                print("i pick up the gun")
            
                self.objs[-9].transformation.translation.x = 100
                self.inventory.append("m16")
                self.weapon = "m16"
                texture = glutils.load_texture(self.m16[0])
                self.update_object_texture(-6, texture)
                self.choixammo()
                self.choixammo()

        if not "glock" in self.inventory:
            distance_glock = np.linalg.norm(glock_position - camera_position)
            if distance_glock <= 2.5:
                sound = pygame.mixer.Sound("sounds/DSITEMUP.wav")
                sound.play()
                print("i pick up the gun")
                sound = pygame.mixer.Sound("sounds/DSITEMUP.wav")
                sound.play()
                self.objs[-10].transformation.translation.x = 100
                self.inventory.append("glock")
                self.weapon = "glock"
                texture = glutils.load_texture(self.gun[0])
                self.update_object_texture(-6, texture)
                self.choixammo()



    def sound_distance(self):

        m16_position = self.objs[-7].transformation.translation
        camera_position = self.cam.transformation.translation
        distance = np.linalg.norm(m16_position - camera_position)
        if distance <2.1:
            exit()
            

        sons = ["sounds/spark1.wav","sounds/spark2.wav","sounds/spark3.wav","sounds/spark4.wav","sounds/spark5.wav","sounds/spark6.wav"]
        index = random.randint(0,5)
        portal_sound = sons[index]


        soundportal = pygame.mixer.Sound(portal_sound)
        max_volume = 1.0
        min_distance = 1.0  # Distance at which the volume is maximum
        max_distance = 30.0  # Distance at which the volume is minimum
        # Calculate the volume based on distance
        volume = max_volume - (distance - min_distance) / (max_distance - min_distance)
        volume = max(0, min(volume, 1))  # Ensure the volume is between 0 and 1
        soundportal.set_volume(volume)
        
        if self.sound_channel is None or not self.sound_channel.get_busy() and not self.ensaut:
            self.sound_channel = pygame.mixer.find_channel()
            self.sound_channel.fadeout(1000) 
            soundportal.play()
        # Set the volume for the sound

    def createenemybullet(self):
        if self.enemienvie:
            if self.creationbullet:
                self.nbbullet += 1
                bullet_position = self.objs[-11].transformation.translation
                self.objs[-8].transformation.translation = bullet_position
                texture = glutils.load_texture("grass.jpg")
                self.update_object_texture(-8, texture)
                self.creationbullet = False
                self.initial_direction = self.cam.transformation.translation - bullet_position  # Store the initial direction
                self.initial_direction = self.initial_direction / np.linalg.norm(self.initial_direction)  # Normalize the initial direction
            else:
                self.bulletmovement()

    def bulletmovement(self):
        if self.nbbullet > 0:
            bullet_position = self.objs[-8].transformation.translation
            speed = 0.5
            new_position = bullet_position + self.initial_direction * speed  # Use the initial direction for bullet movement

            # Adjust the new position to stay grounded on the y-axis (assuming ground level is at y=0)
            new_position[1] = 0

            # Calculate the texture index based on the bullet's movement
            texture_index = int(new_position[0] / 0.1) % len(self.bullet_textures)
            texture = glutils.load_texture(self.bullet_textures[texture_index])
            self.update_object_texture(-8, texture)

            self.objs[-8].transformation.translation = new_position

            # Get the camera's position
            camera_position = self.cam.transformation.translation
            distance = np.linalg.norm(bullet_position - camera_position)

            # Calculate the angle between the enemy and the camera
            angle = np.arctan2(camera_position[0] - new_position[0], camera_position[2] - new_position[2])

            # Update the enemy object's rotation around the y-axis
            self.objs[-8].transformation.rotation_euler[pyrr.euler.index().yaw] = -angle

            if distance <2.2:
                self.life -= 10
            #print(self.cam.transformation.translation)
            #self.checkbullettime()

    #def checkbullettime(self):
    def update_gui(self):
        #print(self.usedammo)
        self.objs[-2].value = str(self.life)
        self.objs[-1].value = str(self.usedammo)
        pass