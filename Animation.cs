
using System;
using System.Collections.Generic;
using System.IO;
using System.IO.Compression;
using System.Linq;
using Microsoft.Xna.Framework.Graphics;

namespace FirstDraft
{
    public class AnimationManager
    {
        Dictionary<string, Animation> animations;
        Animation idleAnimation;
        Animation activeAnimation;
        readonly GraphicsDevice graphicsDevice;
        float time;
        int frame;

        public AnimationManager(GraphicsDevice graphicsDevice)
        {
            activeAnimation = new Animation(new Texture2D[]{}, new float[]{},false);
            frame = 0;
            animations = new Dictionary<string, Animation>();
            time = 0.0f;
            idleAnimation = new Animation(new Texture2D[] { }, new float[] { }, false);
            this.graphicsDevice = graphicsDevice;
        }

        public Animation? GetAnimationObjectByName(string name)
        {
            if (animations.Keys.Contains(name)) //returns the animation if the animation name exists else return a null 
            {
                return animations[name];
            }
            return null;
        }
        public bool AddAnimation(string name, Texture2D[] frames, float[] timings, bool doesLoop = false)
        {
            if (animations.ContainsKey(name))
            {
                return false; // cannot add an animation with the same name as an already existing one
            }
            animations[name] = new Animation(frames, timings, doesLoop);
            return true;
        }

        public bool AddAnimation(string name, string[] framePaths, float[] timings, bool doesLoop = false)
        {
            if (animations.ContainsKey(name))
            {
                return false;
            }

            animations[name] = new Animation(framePaths, timings, doesLoop, graphicsDevice);
            return true;
        }

        public bool AddAnimation(string name, string filePath)
        {
            //NOTE CODE FOR MAKING ANIM FILES EXISTS IN REPO WHICH CONTAINS MY PYTHON IMPLEMENTATION OF THIS, AND WILL BE INCLUDED AT A LATER DATE WHEN MORE DEV TOOLS HAVE
            //BEEN IMPLEMENTED
            if (animations.ContainsKey(name))
            {
                return false;
            }
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
                //https://stackoverflow.com/questions/17509891/c-sharp-how-to-completely-remove-object-from-memory
                //I was unsure whether the animation object being removed would need it's own function to release it's variables but here
                //seemed to indicate it doesn't https://stackoverflow.com/questions/2146434/destroying-a-struct-object-in-c
                //testing with and without a CleanUp function also supports this
                if (activeAnimation == animations[name])
                {
                    activeAnimation = idleAnimation;
                }

                animations.Remove(name);
                GC.Collect(); //Garbage collection collect's the removed animation Object and remove it from memory
                GC.WaitForFullGCApproach();
                
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
            time = 0.0f;
            return true;
        }

        public Texture2D GetNextFrame(float deltaTimeSeconds)
        {
            time += deltaTimeSeconds;
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
        
    }

    public class Animation
    {
        public float[] Timings;
        public Texture2D[] Frames;
        public bool? DoesLoop;

        public Animation(string[] frames, float[] timings,bool doesLoop ,GraphicsDevice graphicsDevice)
        {
            Frames = new Texture2D[frames.Count()];
            for (int i = 0; i < frames.Count(); i++)
            {
                Frames[i] = LoadTexture.GetTexture2DFromFile(frames[i], graphicsDevice);
            }
            Timings = timings;
            DoesLoop = doesLoop;
        }

        public Animation(Texture2D[] frames, float[] timings, bool doesLoop)
        {
            Timings = timings;
            Frames = frames;
            DoesLoop = doesLoop;
        }

        public void CleanUp()
        {
            Frames = null;
            Timings = null;
            DoesLoop = null;
        }

    }
}