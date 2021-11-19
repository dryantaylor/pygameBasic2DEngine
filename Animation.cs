using namespace EngineFramework.Rendering
{
	public class Animation
	{
		public float[] Timings;
        public IntPtr[] Frames;
        public bool DoesLoop;
		
		public Animation(string[] frames, float[] timings,bool doesLoop ,IntPtr renderer)
        {
            Frames = new Texture2D[frames.Count()];
            for (int i = 0; i < frames.Count(); i++)
            {
                Frames[i] = SDL_image.IMG_LoadTexture(frames[i]);
            }
            Timings = timings;
            DoesLoop = doesLoop;
        }

        public Animation(IntPtr[] frames, float[] timings, bool doesLoop)
        {
            Timings = timings;
            Frames = frames;
            DoesLoop = doesLoop;
        }
		
		public void Close()
		{
			foreach (var frame in Frames)
			{
			SDL.SDL_DestroyTexture(frame);
			}
			
		}
	}
}