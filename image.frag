#version 330 core

out vec4 color;

in vec2 vtex;

uniform sampler2D texture;

void main (void)
{
  vec2 tex_coord = vtex;
  color = texture2D(texture, tex_coord);
  if(length(color.a) < 0.2)
    discard;
}
