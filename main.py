from modules.animation import animationManager, transformationManager
import pygame

from createAnimFile import create_file


def example_animation_from_file():
    display = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
    # creating the animation file
    #FILE = "assets/character/idle/"
    #create_file("test.anim",(1/6, 1/6, 1/6, 1/6), (FILE+"00.png", FILE+"01.png", FILE+"02.png", FILE+"03.png"))
    anim_manager = animationManager.AnimationManager()
    anim_manager.add_animation_from_file("test","test.anim",display,10.0)
    anim_manager.set_active_animation("test")
    anim_manager.set_idle_animation("test")

    clock = pygame.time.Clock()
    running = True
    while running:
        delta_time = clock.tick()
        if delta_time > 0:
            delta_time /= 1000
        else:
            delta_time = 0.0005

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.fill((128, 128, 128))
        display.blit(anim_manager.get_frame(delta_time), (100, 100))
        pygame.display.flip()
        print(1/delta_time)


def example_transform():
    display = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
    transformation_manager = transformationManager.TransformationManager()
    transformation_manager.add_transformation("rotate",(1.0,1.0,1.0,1.0,1.0),((pygame.transform.rotate, [None, 0], 0),(transformationManager.CustomTransitions.tint_image,[None,(128,0,0,50)],0)),
                                              ((pygame.transform.rotate, [None, 90], 0), (transformationManager.CustomTransitions.tint_image,[None,(128,0,0,50)],0)),
                                              ((pygame.transform.rotate, [None, 180], 0), (transformationManager.CustomTransitions.tint_image,[None,(128,0,0,50)],0)),
                                              ((pygame.transform.rotate, [None, 270], 0), (transformationManager.CustomTransitions.tint_image,[None,(128,0,0,50)],0)))
    transformation_manager.set_active_transformation("rotate")
    animation_manager = animationManager.AnimationManager()
    animation_manager.add_animation_from_file("idle","./test.anim", display, 10.0)
    animation_manager.set_idle_animation("idle")
    animation_manager.set_active_animation("idle")

    clock = pygame.time.Clock()
    running = True
    image = pygame.transform.scale(pygame.image.load("./assets/character/idle/00.png"), (500, 370)).convert_alpha()
    while running:
        delta_time = clock.tick()
        if delta_time > 0:
            delta_time /= 1000
        else:
            delta_time = 0.0005

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        display.fill((128, 128, 128))
        if transformation_manager.active_transformation is not None:
            display.blit(transformation_manager.apply_transformation_to_frame(delta_time, animation_manager.get_frame(delta_time)), (100, 100))
        else:
            display.blit(animation_manager.get_frame(delta_time), (100, 100))

        pygame.display.flip()
        print(1 / delta_time)

if __name__ == "__main__":
    #example_animation_from_file()
    example_transform()

