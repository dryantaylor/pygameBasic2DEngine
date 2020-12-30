import modules.animations.animationManager as animationManager
import pygame

def write_anim_to_file(animation: animationManager.Animation,img_mode : int ,fileName,file_locations = None):
    file = open(fileName,"w")
    text = ""
    text+=str((int(animation.does_loop)))+ "\n" +str(img_mode)+"\n"
    text+=str(len(animation.images)) + "\n"
    if img_mode == 0:
        for location in file_locations:
            text+=location+"\n"

    elif img_mode == 1: #doesn't work here
        sizes = []
        for image in animation.images:

            text += str(pygame.image.tostring(image,"RGBA"))[2:][:-1] + "\n"
            sizes.append(f"{image.get_width()},{image.get_height()}")
        for size in sizes:
            text+=size+"\n"
    for timing in animation.timings:
        text += str(timing) + "\n"
    text = text[:-1]

    file.write(text)

animation_manager = animationManager.AnimationManager()

timing = 1/8

""" ADD ANIMATIONS"""
images = [pygame.image.load("./assets/character/idle/00.png"),
          pygame.image.load("./assets/character/idle/01.png"),
          pygame.image.load("./assets/character/idle/02.png"),
          pygame.image.load("./assets/character/idle/03.png")]

for i, image in enumerate(images):
    images[i] = pygame.transform.scale(image, (500, 370))
animation_manager.add_animation("idle", images, (timing, timing, timing, timing), does_loop= True)
write_anim_to_file(animation_manager.animations["idle"],0,"test.anim",("./assets/character/idle/00.png","./assets/character/idle/01.png","./assets/character/idle/02.png","./assets/character/idle/03.png"))
animation_manager.add_animation_from_file("idle_2","./test.anim")

animation_manager.set_active_animation("idle_2")
x = 0
display = pygame.display.set_mode((1280,720),pygame.DOUBLEBUF)
clock = pygame.time.Clock()
while True:
    deltaTime = clock.tick()  # deltaTime is in MilliSeconds
    if deltaTime > 0:
        deltaTime /= 1000  # ms to seconds
    else:
        deltaTime = 0.0005  # half an ms
    for event in pygame.event.get():
        pass
    display.fill((200,200,200))
    display.blit(pygame.transform.scale(animation_manager.get_frame(deltaTime),(500,370)),(1,1))
    pygame.display.flip()