import OpenGL.GL as GL
import pyrr
import numpy as np 

class Transformation3D: 
    def __init__(self, euler = pyrr.euler.create(), center = pyrr.Vector3(), translation = pyrr.Vector3()):
        self.rotation_euler = euler.copy()
        self.rotation_center = center.copy()
        self.translation = translation.copy()

class Object:
    def __init__(self, vao, nb_triangle, program, texture):
        self.vao = vao
        self.nb_triangle = nb_triangle
        self.program = program
        self.texture = texture
        self.visible = True

    def draw(self):
        if self.visible : 
            GL.glUseProgram(self.program)
            GL.glBindVertexArray(self.vao)
            GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
            GL.glDrawElements(GL.GL_TRIANGLES, 3*self.nb_triangle, GL.GL_UNSIGNED_INT, None)




class Hitbox:
    def __init__(self, width, height, x, y):
        self.width = width
        self.height = height
        self.x = x
        self.y = y

    def collides_with(self, other_hitbox):
        pass






class Object3D(Object):
    def __init__(self, vao, nb_triangle, program, texture, transformation):
        super().__init__(vao, nb_triangle, program, texture)
        self.transformation = transformation

    def draw(self):
        GL.glUseProgram(self.program)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(self.program, "translation_model")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : translation_model")
        # Modifie la variable pour le programme courant
        translation = self.transformation.translation
        GL.glUniform4f(loc, translation.x, translation.y, translation.z, 0)

        # Récupère l'identifiant de la variable pour le programme courant
        loc = GL.glGetUniformLocation(self.program, "rotation_center_model")
        # Vérifie que la variable existe
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_center_model")
        # Modifie la variable pour le programme courant
        rotation_center = self.transformation.rotation_center
        GL.glUniform4f(loc, rotation_center.x, rotation_center.y, rotation_center.z, 0)

        rot = pyrr.matrix44.create_from_eulers(self.transformation.rotation_euler)
        loc = GL.glGetUniformLocation(self.program, "rotation_model")
        if (loc == -1) :
            print("Pas de variable uniforme : rotation_model")
        GL.glUniformMatrix4fv(loc, 1, GL.GL_FALSE, rot)

        super().draw()




class Camera():
    def __init__(self, transformation=Transformation3D(translation=pyrr.Vector3([0, 1, 0], dtype='float32')),
                projection=pyrr.matrix44.create_perspective_projection(60, 1, 0.01, 100)):
        self.transformation = transformation
        self.projection = projection
        self.forward_direction = pyrr.Vector3([0, 0, -1])
        self.right_direction = pyrr.Vector3([1, 0, 0])
        self.update_directions()  # Update the initial directions

    def update_directions(self):
        rotation = pyrr.matrix33.create_from_eulers(self.transformation.rotation_euler)
        self.forward_direction = rotation @ pyrr.Vector3([0, 0, -1])
        self.forward_direction.y = 0.0
        self.forward_direction = pyrr.vector.normalise(self.forward_direction)  # Normalize the vector
        self.right_direction = rotation @ pyrr.Vector3([1, 0, 0])
        self.right_direction.y = 0.0
        self.right_direction = pyrr.vector.normalise(self.right_direction)  # Normalize the vector

    def rotate(self, axis, angle):
        self.transformation.rotate(axis, angle)
        self.update_directions()

    def translate(self, vector):
        self.transformation.translate(vector)
        self.update_directions()

    def projection_matrix(self):
        return self.projection
    
    def view_matrix(self):
        translation_matrix = pyrr.matrix44.create_from_translation(-self.transformation.translation)
        rotation_matrix = pyrr.matrix44.create_from_matrix33(pyrr.matrix33.create_from_eulers(self.transformation.rotation_euler))
        return rotation_matrix @ translation_matrix


class Text(Object):
    def __init__(self, value, bottomLeft, topRight, vao, nb_triangle, program, texture):
        self.value = value
        self.bottomLeft = bottomLeft
        self.topRight = topRight
        super().__init__(vao, nb_triangle, program, texture)

    def draw(self):
        GL.glUseProgram(self.program)
        GL.glDisable(GL.GL_DEPTH_TEST)
        size = self.topRight-self.bottomLeft
        size[0] /= len(self.value)
        loc = GL.glGetUniformLocation(self.program, "size")
        if (loc == -1) :
            print("Pas de variable uniforme : size")
        GL.glUniform2f(loc, size[0], size[1])
        GL.glBindVertexArray(self.vao)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        for idx, c in enumerate(self.value):
            loc = GL.glGetUniformLocation(self.program, "start")
            if (loc == -1) :
                print("Pas de variable uniforme : start")
            GL.glUniform2f(loc, self.bottomLeft[0]+idx*size[0], self.bottomLeft[1])

            loc = GL.glGetUniformLocation(self.program, "c")
            if (loc == -1) :
                print("Pas de variable uniforme : c")
            GL.glUniform1i(loc, np.array(ord(c), np.int32))

            GL.glDrawElements(GL.GL_TRIANGLES, 3*2, GL.GL_UNSIGNED_INT, None)
        GL.glEnable(GL.GL_DEPTH_TEST)

    @staticmethod
    def initalize_geometry():
        p0, p1, p2, p3 = [0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]
        geometrie = np.array([p0+p1+p2+p3], np.float32)
        index = np.array([[0, 1, 2]+[0, 2, 3]], np.uint32)
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, geometrie, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        vboi = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ELEMENT_ARRAY_BUFFER,vboi)
        GL.glBufferData(GL.GL_ELEMENT_ARRAY_BUFFER,index,GL.GL_STATIC_DRAW)
        return vao
    
class Image(Object):
    def __init__(self, filename, bottomLeft, topRight, vao, nb_triangle, program, texture):
        self.filename = filename
        self.bottomLeft = bottomLeft
        self.topRight = topRight
        super().__init__(vao, nb_triangle, program, texture)

    def draw(self):
        GL.glUseProgram(self.program)
        GL.glDisable(GL.GL_DEPTH_TEST)
        loc = GL.glGetUniformLocation(self.program, "start")
        if loc == -1:
            print("Pas de variable uniforme : start")
        GL.glUniform2f(loc, *self.bottomLeft)

        loc = GL.glGetUniformLocation(self.program, "size")
        if loc == -1:
            print("Pas de variable uniforme : size")
        size = self.topRight-self.bottomLeft
        GL.glUniform2f(loc, *size)

        GL.glBindVertexArray(self.vao)
        GL.glBindTexture(GL.GL_TEXTURE_2D, self.texture)
        GL.glDrawArrays(GL.GL_TRIANGLES, 0, self.nb_triangle * 3)
        GL.glEnable(GL.GL_DEPTH_TEST)

    @staticmethod
    def initialize_geometry():
        p0, p1, p2, p3 = [0, 0, 0], [0, 1, 0], [1, 1, 0], [1, 0, 0]
        geometry = np.array([p0 + p1 + p2, p0 + p2 + p3], np.float32)
        vao = GL.glGenVertexArrays(1)
        GL.glBindVertexArray(vao)
        vbo = GL.glGenBuffers(1)
        GL.glBindBuffer(GL.GL_ARRAY_BUFFER, vbo)
        GL.glBufferData(GL.GL_ARRAY_BUFFER, geometry, GL.GL_STATIC_DRAW)
        GL.glEnableVertexAttribArray(0)
        GL.glVertexAttribPointer(0, 3, GL.GL_FLOAT, GL.GL_FALSE, 0, None)
        GL.glBindVertexArray(0)
        return vao


