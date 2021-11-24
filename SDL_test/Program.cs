using System;
using SDL2;


namespace SDL_test
{
    class Program
    {
        static void Main(string[] args)
        {
            Console.WriteLine("Hello World!");
            var Window = SDL.SDL_CreateWindow("Animation Test",SDL.SDL_WINDOWPOS_CENTERED, SDL.SDL_WINDOWPOS_CENTERED, 1280,720,SDL.SDL_WindowFlags.SDL_WINDOW_SHOWN);
            var Renderer = SDL.SDL_CreateRenderer(Window, -1, SDL.SDL_RendererFlags.SDL_RENDERER_ACCELERATED);
            bool running = true;
            var animManager = new EngineFramework.Rendering.AnimationManager(Renderer);
            animManager.AddAnimation("Idle", new string[] {"idle/00.png", "idle/01.png","idle/02.png","idle/03.png"}, new int[] {125, 125, 125, 125},null, true);
            animManager.AddAnimation("Attack1", new string[] { "attack/00.png", "attack/01.png", "attack/02.png", "attack/03.png", "attack/04.png" }, new int[] {100,100,100,100,100});
            animManager.SetIdleAnimation("Idle");
            animManager.SetActiveAnimation("Idle");
            uint last_time = SDL.SDL_GetTicks();
            uint deltaTime = 0;
            bool mouse_pressed = false;
            while (running)
            {
                uint curr_time = SDL.SDL_GetTicks();
                deltaTime = curr_time - last_time;
                while (SDL.SDL_PollEvent(out var e) != 0)
                {
                    switch (e.type)
                    {
                        case (SDL.SDL_EventType.SDL_QUIT):
                            running = false;
                            break;
                        case (SDL.SDL_EventType.SDL_MOUSEBUTTONDOWN):
                            if (!mouse_pressed)
                            {
                                mouse_pressed = true;
                                animManager.SetActiveAnimation("Attack1");
                            }
                            break;
                        case (SDL.SDL_EventType.SDL_MOUSEBUTTONUP):
                            if (mouse_pressed)
                            {
                                mouse_pressed = false;
                            }
                            break;
                    }
                }
                var dRect = new SDL.SDL_Rect() { x = 0, y = 0, w = 500, h = 370 };
                SDL.SDL_RenderClear(Renderer);
                SDL.SDL_RenderCopy(Renderer,animManager.GetNextFrame((int) deltaTime), ref animManager.GetSourceRect(), ref dRect);
                SDL.SDL_RenderPresent(Renderer);

                last_time = curr_time;
            }
            animManager.Close();
            SDL.SDL_DestroyRenderer(Renderer);
            SDL.SDL_DestroyWindow(Window);
        }
    }
}
