    #!/usr/bin/env python3
import OpenGL.GL as GL
import glfw
import pyrr
import numpy as np
from cpe3d import Object3D
from pyrr import Matrix44, Vector3
import os,sys, time
import glutils
import pygame

pygame.mixer.init(frequency = 44100, size = -16, channels = 3, buffer = 1012)
pygame.mixer.Channel(0).set_volume(0.5)


class ViewerGL:
    def __init__(self, gun ,etatgun,ammo,reloadglock,bolt,reloadbolt,crowbar):
        # initialisation de la librairie GLFW
        glfw.init()
        # paramétrage du context OpenGL
        glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
        glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, GL.GL_TRUE)
        glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
        # création et paramétrage de la fenêtre
        glfw.window_hint(glfw.RESIZABLE, False)
        self.window = glfw.create_window(400, 400, 'DA GAME', None, None)
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
        # Mouse handling variables
        self.prev_mouse_pos = None
        self.mouse_sensitivity = 0.001
        self.gun = gun
        self.crowbar = crowbar
        self.crowbar_indice = 0
        self.reloadglock = reloadglock
        self.bolt = bolt
        self.reloadbolt = reloadbolt
        self.reloading = False
        self.etatgun = etatgun
        self.texture_change_delay_fire = 0.02
        self.texture_change_delay_reload = 0.05
        self.current_change_delay = self.texture_change_delay_fire
        self.last_texture_change_time = glfw.get_time()  # Set the initial time to the current time
        self.gun_index = 0  # Index of the current gun texture
        self.is_texture_loop_active = False  # Flag indicating if the texture change loop is active
        self.left_mouse_button_pressed = False  # Flag indicating if the left mouse button is pressed
        self.mouse_buttons = []
        self.ammo = ammo
        self.boltammo = 1
        self.current_texture_list = self.crowbar[self.crowbar_indice]  # Initialize with the gun texture list
        self.weapon = "crowbar"
        self.usedammo = 10



    def run(self):
        global etatgun
        # hide the cursor
        glfw.set_input_mode(self.window, glfw.CURSOR, glfw.CURSOR_HIDDEN)
        self.choixammo()
        # boucle d'affichage
        while not glfw.window_should_close(self.window):
            # nettoyage de la fenêtre : fond et profondeur
            GL.glClear(GL.GL_COLOR_BUFFER_BIT | GL.GL_DEPTH_BUFFER_BIT)

            self.update_key()
            self.update_mouse_button()
            etatgun = 0
            self.fire()


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
                if isinstance(obj, Object3D):
                    self.update_camera(obj.program)
                obj.draw()
            if glfw.get_key(self.window, glfw.KEY_ESCAPE) == glfw.PRESS:
                glfw.set_window_should_close(self.window, True)
            # changement de buffer d'affichage pour éviter un effet de scintillement
            glfw.swap_buffers(self.window)
            # gestion des évènements
            glfw.poll_events()

        

    
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
        translation_speed = 0.1
        rotation_speed = 0.1

        # Update camera transformation based on pressed keys
        for key in self.key_pressed:
            if key == glfw.KEY_I:
                self.cam.transformation.rotation_euler[0] -= rotation_speed  # Negate rotation
            elif key == glfw.KEY_K:
                self.cam.transformation.rotation_euler[0] += rotation_speed  # Negate rotation
            elif key == glfw.KEY_J:
                self.cam.transformation.rotation_euler[2] -= rotation_speed  # Negate rotation
            elif key == glfw.KEY_L:
                self.cam.transformation.rotation_euler[2] += rotation_speed  # Negate rotation
            
            if key == glfw.KEY_2:
                self.weapon = "glock"
                self.current_texture_list = self.gun
                texture = glutils.load_texture("sprites/Pistol/HW2Fa0.png")
                self.update_object_texture(3, texture)
            elif key == glfw.KEY_3:
                self.weapon = "crowbar"
                self.current_texture_list = self.crowbar[self.crowbar_indice]
                texture = glutils.load_texture("sprites/Crowbar/crowbar1.png")
                self.update_object_texture(3, texture)


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
                self.cam.transformation.translation -= forward * translation_speed  # Negate translation
            elif key == glfw.KEY_S or key == glfw.KEY_DOWN:
                self.cam.transformation.translation += forward * translation_speed  # Negate translation
            elif key == glfw.KEY_A or key == glfw.KEY_LEFT:
                self.cam.transformation.translation += right * translation_speed  # Negate translation
            elif key == glfw.KEY_D or key == glfw.KEY_RIGHT:
                self.cam.transformation.translation -= right * translation_speed  # Negate translation
            elif key == glfw.KEY_Q:
                self.cam.transformation.translation += pyrr.Vector3([0, translation_speed, 0])
            elif key == glfw.KEY_E:
                self.cam.transformation.translation -= pyrr.Vector3([0, translation_speed, 0])

        # Update camera's rotation center based on its translation
        self.cam.transformation.rotation_center = self.cam.transformation.translation.copy()


    def mouse_button_callback(self, win, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            if self.reloading == False and not self.is_texture_loop_active:              
                if self.weapon == "glock":
                    if self.usedammo >0 :
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/pistol_fire1.wav'))
                    else:
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/DRY.ogg'))
                elif self.weapon == "bolt":
                    if self.usedammo >0:
                        pygame.mixer.Channel(0).play(pygame.mixer.Sound('sounds/bolt_fire.ogg'))
                    else:
                        self.reload()
                elif self.weapon == "crowbar":
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
            self.usedammo = self.ammo
        elif self.weapon == "bolt":
            self.usedammo = self.boltammo

    def fire(self):
        if self.reloading == False:
            if self.usedammo > 0:
                for button in self.mouse_buttons:
                    if button == glfw.MOUSE_BUTTON_LEFT and not self.is_texture_loop_active:
                        self.current_change_delay = self.texture_change_delay_fire
                        if self.weapon == "glock":
                            self.current_texture_list = self.gun
                        elif self.weapon == "bolt":
                            self.current_texture_list = self.bolt
                        elif self.weapon == "crowbar":
                            print("la crowbar frappe")
                            self.current_texture_list = self.crowbar[self.crowbar_indice]
                            self.crowbar_indice +=1
                            self.usedammo +=1
                            if self.crowbar_indice >2:
                                self.crowbar_indice = 0
                        self.usedammo -= 1  # Remove 1 from the ammo variable
                        self.change_gun_texture(self.current_texture_list)
                        self.last_texture_change_time = glfw.get_time()
                        self.is_texture_loop_active = True
            if self.usedammo == 0:
                self.reload()

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
            self.usedammo += 10


        elif self.weapon == "bolt":
            sound_clipout = pygame.mixer.Sound('sounds/bolt_reload.ogg')
            chan1 = pygame.mixer.find_channel()
            chan1.queue(sound_clipout)
            self.current_texture_list = self.reloadbolt
            self.usedammo += 1
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
            self.update_object_texture(3, texture)  # Assuming the gun object is at index 3
            print("changement de texture")
            self.gun_index += 1

        if self.gun_index >= len(texture_list):
            self.gun_index = 0  # Reset the index to loop back to the beginning
            self.reloading = False
            self.is_texture_loop_active = False  # Stop the texture change loop
            


        