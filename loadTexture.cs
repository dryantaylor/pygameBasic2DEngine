using System.IO;
using Microsoft.Xna.Framework.Graphics;

namespace FirstDraft
{
    public class LoadTexture
    {
        public static Texture2D GetTexture2DFromFile(string path, GraphicsDevice graphicsDevice)
        {
            //opens a filestream and creates a Texture2D from said filestrem before retuning it
            //code taken from https://community.monogame.net/t/loading-png-jpg-etc-directly/7403/3
            FileStream fileStream = new FileStream(path, FileMode.Open);
            return GetTexture2DFromStream(fileStream, graphicsDevice);
        }

        public static Texture2D GetTexture2DFromStream(FileStream stream, GraphicsDevice graphicsDevice)
        {
            Texture2D texture = Texture2D.FromStream(graphicsDevice, stream);
            stream.Dispose();
            return texture;
        }

        public static Texture2D GetTexture2DFromStream(Stream stream, GraphicsDevice graphicsDevice)
        {
            Texture2D texture = Texture2D.FromStream(graphicsDevice, stream);
            stream.Dispose();
            return texture;
        }
        
    }
}