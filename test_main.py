import pygame
import modules.animations.animationManager as animationManager
import modules.GUI.UIManager as UIManager
pygame.init()

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

    """ ADD ANIMATION FROM FILE"""
    animation_manager.add_animation_from_file("idle_2", "./test.anim")

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
    display = pygame.display.set_mode((1280,900),pygame.DOUBLEBUF)
    UI_manager = UIManager.GUIManager(display,(1280,900))
    UI_manager.add_element(UIManager.Button,"testButton",(100,100), pygame.Rect(100,100,190,40),(say_hi,()),
                                                pygame.image.load("./assets/UI_elements/button00.png"),
                                                pygame.image.load("./assets/UI_elements/button01.png"))

    UI_manager.add_element(UIManager.Slider,"testSlider",(50,200),pygame.image.load("./assets/UI_elements/blue_tick.png"),pygame.image.load("assets/UI_elements/blue_sliderRight.png"),
                                                UIManager.Directions.LEFTtoRIGHT)

    font = pygame.font.SysFont("comic sans",50)
    UI_manager.add_element(UIManager.DropDown,"testDropdown",(50,300),pygame.image.load("./assets/UI_elements/button00.png"),pygame.image.load("./assets/UI_elements/button01.png"),
                           pygame.Surface((10,10)),0,(font.render("hello",True,(0,0,0)),"hello"),(font.render("aa",True,(0,0,0)),"aa"),(font.render("bb",True,(0,0,0)),"bb"))
    while True:
        deltaTime = clock.tick()  # deltaTime is in MilliSeconds
        if deltaTime > 0:
            deltaTime /= 1000  # ms to seconds
        else:
            deltaTime = 0.0005  # half an ms
        UI_manager.update_animations(deltaTime)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            UI_manager.update_at_event(event)


        display.fill((120,120,120))
        UI_manager.draw()
        pygame.display.flip()

def example_SettingsMenu():
    def change_settings(UI_manager: UIManager.GUIManager,res_button_name,flags_element_names : list):
        res = UI_manager.get_state_of_element(res_button_name)
        flags = pygame.DOUBLEBUF
        for name in flags_element_names:
            flags |= UI_manager.get_state_of_element(name)
        UI_manager.scale(res)
        return pygame.display.set_mode(res,flags)
    def test(*args):
        print("hello")

    clock = pygame.time.Clock()
    display = pygame.display.set_mode((1280, 720), pygame.DOUBLEBUF)
    UI_manager = UIManager.GUIManager(display, (1280, 720))

    UI_manager.add_element(UIManager.Button, "apply_button", (1000, 600), pygame.Rect(1000, 600, 190, 40), (change_settings, (UI_manager,"resoloution",["screen_mode"])),
                           pygame.image.load("./assets/UI_elements/button00.png"),
                           pygame.image.load("./assets/UI_elements/button01.png"))

    font = pygame.font.SysFont("comic sans",50)
    UI_manager.add_element(UIManager.DropDown,"resoloution",(50,300),pygame.image.load("./assets/UI_elements/button00.png"),pygame.image.load("./assets/UI_elements/button01.png"),
                           pygame.Surface((10,10)),0,(font.render("848x480",True,(0,0,0)),(848,480)),(font.render("1280x720",True,(0,0,0)),(1280,720)),(font.render("1920x1080",True,(0,0,0)),(1920,1080)))
    UI_manager.add_element(UIManager.DropDown,"screen_mode",(50,500),pygame.image.load("./assets/UI_elements/button00.png"),pygame.image.load("./assets/UI_elements/button01.png"),
                           pygame.Surface((10,10)),0,(font.render("windowed",True,(0,0,0)),pygame.SHOWN),(font.render("borderless",True,(0,0,0)),pygame.NOFRAME),(font.render("fullscreen",True,(0,0,0)),pygame.FULLSCREEN))
    while True:
        deltaTime = clock.tick()  # deltaTime is in MilliSeconds
        if deltaTime > 0:
            deltaTime /= 1000  # ms to seconds
        else:
            deltaTime = 0.0005  # half an ms
        UI_manager.update_animations(deltaTime)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return

            UI_manager.update_at_event(event)


        display.fill((120,120,120))
        UI_manager.draw()
        pygame.display.flip()

if __name__ == "__main__":
    #example_animations()
    example_UI()
    #example_SettingsMenu()