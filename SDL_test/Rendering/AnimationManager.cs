using System;
using System.Collections.Generic;
using SDL2;

namespace EngineFramework.Rendering
{
    public class AnimationManager
    {
        Dictionary<string, Animation> animations;
        Animation idleAnimation;
        Animation activeAnimation;
        IntPtr Renderer;
        int time;
        int frame;

        public AnimationManager(IntPtr renderer)
        {
            activeAnimation = new Animation(new IntPtr[] { }, new float[] { }, false);
            frame = 0;
            animations = new Dictionary<string, Animation>();
            time = 0;
            idleAnimation = new Animation(new IntPtr[] { }, new float[] { }, false);
            Renderer = renderer;
        }

        #nullable enable
        public Animation? GetAnimationObjectByName(string name)
        {
            if (animations.ContainsKey(name)) //returns the animation if the animation name exists else return a null 
            {
                return animations[name];
            }
            return null;
        }
        public bool AddAnimation(string name, IntPtr[] frames, int[] timings,SDL.SDL_Rect? srect = null, bool doesLoop = false)
        {
            if (animations.ContainsKey(name))
            {
                return false; // cannot add an animation with the same name as an already existing one
            }
            animations[name] = new Animation(frames, timings, doesLoop, srect);
            return true;
        }

        public bool AddAnimation(string name, string[] framePaths, int[] timings,SDL.SDL_Rect? srect = null, bool doesLoop = false)
        {
            if (animations.ContainsKey(name))
            {
                return false;
            }

            animations[name] = new Animation(framePaths, timings, doesLoop, Renderer, srect);
            return true;

        }
        /**
        public bool AddAnimation(string name, string filePath)
        {
            //NOTE CODE FOR MAKING ANIM FILES EXISTS IN REPO WHICH CONTAINS MY PYTHON IMPLEMENTATION OF THIS, AND WILL BE INCLUDED AT A LATER DATE WHEN MORE DEV TOOLS HAVE
            //BEEN IMPLEMENTED
            if (animations.ContainsKey(name))
            {
                return false;
            }
			//todo: CONVERT ACROSS TO SDL2 FROM MONOGAME
            //Todo: MAKE THIS VERY BODGED CODE NICER, HOWEVER GOOD INITIAL IMPLEMENTATION
            
            var animArgs = new Dictionary<string, dynamic>();
            var streamFileNameDict = new Dictionary<string, Stream>();
            using (var animFile = ZipFile.OpenRead(filePath))
            {
                ZipArchiveEntry[] imgStreams;
                //function written with help from https://stackoverflow.com/questions/22604941/how-can-i-unzip-a-file-to-a-net-memory-stream
                //and https://docs.microsoft.com/en-us/dotnet/api/system.io.compression.ziparchive?view=net-5.0
                imgStreams = new ZipArchiveEntry[animFile.Entries.Count - 1];
                int pointerImgStreams = 0;
                foreach (var entry in animFile.Entries) //each file in the anim folder
                {

                    if (entry.Name != "info.cfg") 
                    {
                        imgStreams[pointerImgStreams] = entry;
                        pointerImgStreams++;
                    }
                    else{
                        string[] fileContent;
                        using (var reader = new StreamReader(entry.Open()))
                        {

                            fileContent = reader.ReadToEnd().Replace("\r\n", "").Replace(" ","").Split(";");
                            reader.Dispose();
                        }

                        foreach (var arg in fileContent)
                        {
                            dynamic value;
                            var split = arg.Split("=");
                            var key = split[0];
                            switch (key)
                            {
                                case ("does_loop"):
                                    value = Convert.ToBoolean(split[1]);
                                    animArgs[key] = value;
                                    break;
                                case ("timings"):
                                    var timingsString = split[1].Split(",");
                                    value = new float[timingsString.Length];
                                    for(var i = 0; i < timingsString.Length;i++)
                                    {
                                        value[i] = float.Parse(timingsString[i]);
                                    }
                                    animArgs[key] = value;
                                    break;
                                case ("image_locs"):
                                    value = split[1].Split(",");
                                    animArgs[key] = value;
                                    break;
                            }
                        }

                    }

                }
                //convert the image Zip objects into a dictionary of stream objects and their name
                foreach (var img in imgStreams)
                {
                    streamFileNameDict[img.Name] = img.Open();
                }
                //use arguments from the info.cfg to create an animation object
                Texture2D[] frames = new Texture2D[animArgs["image_locs"].Length];
                for (var i = 0; i < animArgs["image_locs"].Length; i++)
                {

                    frames[i] = LoadTexture.GetTexture2DFromStream(streamFileNameDict[animArgs["image_locs"][i]], graphicsDevice);
                }
                
                animations[name] = new Animation(frames, animArgs["timings"], animArgs["does_loop"]);
            }
            GC.Collect(); //todo: decide if this is a good or bad thing to include
            GC.WaitForFullGCApproach();
            return false;
            }
            **/


        public bool AddAnimation(string name, Animation animation)
        {
            if (animations.ContainsKey(name))
            {
                return false;
            }
            animations[name] = animation;
            return true;
        }

        public bool RemoveAnimation(string name)
        {

            if (animations.ContainsKey(name) && idleAnimation != animations[name])
            {

                if (activeAnimation == animations[name])
                {
                    activeAnimation = idleAnimation;
                }
                //unlike monogame SDL requires resources are managed so i must manually close the textures
                animations[name].Close();
                animations.Remove(name);
                GC.Collect(); //Garbage collection collect's the removed animation Object and remove it from memory

                return true;
            }

            return false;

        }

        public bool SetIdleAnimation(string animationName)
        {
            if (!animations.ContainsKey(animationName))
            {
                return false;
            }

            idleAnimation = animations[animationName];
            return true;
        }

        public bool SetActiveAnimation(string animationName)
        {
            if (!animations.ContainsKey(animationName))
            {
                return false;
            }

            activeAnimation = animations[animationName];
            frame = 0; //resting the frame and time back to 0, starting the animation from the start
            time = 0;
            return true;
        }

        public IntPtr GetNextFrame(int deltaTime)
        {
            time += deltaTime;
            while (true)
            {
                //if the time is greater than the current frame work out the next frame
                if (time > activeAnimation.Timings[frame])
                {
                    //if not on the last frame of the animation
                    if (frame + 1 < activeAnimation.Frames.Length)
                    {
                        time -= activeAnimation.Timings[frame];
                        frame += 1;
                    }
                    else
                    {
                        time -= activeAnimation.Timings[frame];
                        frame = 0;

                        //if it doesn't loop go back to the idle animation
                        if (!(bool)activeAnimation.DoesLoop)
                        {
                            activeAnimation = idleAnimation;
                        }

                    }
                }
                else
                {
                    //here will eventually always be reached which is how the while loop is escaped
                    return activeAnimation.Frames[frame];
                }
            }
        }
        public ref SDL.SDL_Rect GetSourceRect()
        {
            return ref activeAnimation.sRect;
        }
        public void Close()
        {
            foreach(var anim in animations.Values)
            {
                anim.Close();
            }
            animations.Clear();
            idleAnimation = null;
            activeAnimation = null;
            Renderer = IntPtr.Zero;
        }
    }
}