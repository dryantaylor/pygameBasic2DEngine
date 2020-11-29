import pygame
import modules.animations.animationManager as animationManager
import modules.GUI.UIManager as UIManager

def example_animations():
    display = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)

    animation_manager = animationManager.AnimationManager()
    timing = 1/8

    """ ADD ANIMATIONS"""
    images = [pygame.image.load("./assets/character/idle/00.png").convert_alpha(display),
              pygame.image.load("./assets/character/idle/01.png").convert_alpha(display),
              pygame.image.load("./assets/character/idle/02.png").convert_alpha(display),
              pygame.image.load("./assets/character/idle/03.png").convert_alpha(display)]
    for i, image in enumerate(images):
        images[i] = pygame.transform.scale(image, (500, 370))
    animation_manager.add_animation("idle", images, (timing, timing, timing, timing), does_loop= True)

    images = [pygame.image.load("./assets/character/attack_01/00.png").convert_alpha(display),
              pygame.image.load("./assets/character/attack_01/01.png").convert_alpha(display),
              pygame.image.load("./assets/character/attack_01/02.png").convert_alpha(display),
              pygame.image.load("./assets/character/attack_01/03.png").convert_alpha(display),
              pygame.image.load("./assets/character/attack_01/04.png").convert_alpha(display)]
    for i, image in enumerate(images):
        images[i] = pygame.transform.scale(image, (500, 370))
    animation_manager.add_animation("attack_1", images, (1/6, timing, timing, timing, timing), does_loop=False)

    """NECESSARY --- SET IDLE AND ACTIVE ANIMATION"""
    animation_manager.set_idle_animation("idle")  #IDLE - should be looping
    animation_manager.set_active_animation("idle")
    clock = pygame.time.Clock()

    while True:
        deltaTime = clock.tick()  # deltaTime is in MilliSeconds
        if deltaTime > 0:
            deltaTime /= 1000  # ms to seconds
        else:
            deltaTime = 0.0005  # half an ms

        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONDOWN:
                  if event.button == pygame.BUTTON_LEFT:
                        animation_manager.set_active_animation("attack_1")

        display.fill((120, 120, 120))
        display.blit(animation_manager.get_frame(deltaTime), (100, 100))
        pygame.display.flip()

def example_UI():
    def say_hi():
        print("hi")

    clock = pygame.time.Clock()
    display = pygame.display.set_mode((1280,720),pygame.DOUBLEBUF)
    UI_manager = UIManager.GUIManager(display,(1280,720))
    UI_manager.elements.append(UIManager.Button(UI_manager,"testOne",(100,100), pygame.Rect(100,100,190,40),(say_hi,()),
                                                pygame.image.load("./assets/UI_elements/button00.png"),
                                                pygame.image.load("./assets/UI_elements/button01.png")))

    while True:
        deltaTime = clock.tick()  # deltaTime is in MilliSeconds
        if deltaTime > 0:
            deltaTime /= 1000  # ms to seconds
        else:
            deltaTime = 0.0005  # half an ms
        UI_manager.update_aimations(deltaTime)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pass

            UI_manager.update_at_event(event)
        display.fill((120,120,120))
        UI_manager.draw()
        pygame.display.flip()

if __name__ == "__main__":
    #example_animations()
    example_UI()