using System.Net.Http;
using HtmlAgilityPack;

namespace Scraper
{
    class Program
    {
        public static async Task Main(string[] args)
        {
            var web = new HtmlWeb();

            // This allows for 'searching' on apples end of things and selects thier first choice
            string albumName = "17";
            string url = "https://music.apple.com/us/search?term=" + formatalbumnameforurl(albumName);
            HtmlDocument document = web.Load(url);

            // Selects the first album in the list, fis the xpath later
            HtmlNodeCollection firstalbuminsearch = document.DocumentNode.SelectNodes(
                "//a[@class='product-lockup__link svelte-cgujde'])[0]");

            string ablumpagelink = firstalbuminsearch[0].Attributes["href"].Value;

            Console.WriteLine(ablumpagelink);


            HtmlDocument albumpage = web.Load(ablumpagelink);

            HtmlNode picture = albumpage.DocumentNode.QuerySelectorAll("picture")[0];
            var src = picture.QuerySelectorAll("source")[1];
            Console.WriteLine( src.OuterHtml.Split(',').Last().Split(' ')[0]);

            // Album name, Artist, Year released
            HtmlNode info = albumpage.QuerySelector(".headings.svelte-1la0y7y");
            Console.WriteLine(info.InnerText);

            // Xpath is like regex for html
            // this gets every div that has the track-title for its data-testid
            var songslist = albumpage.DocumentNode.SelectNodes("//div[@data-testid='track-title']");
            Console.WriteLine(songslist.Count);



        }

        private static string formatalbumnameforurl(string name)
        {
            string s = string.Empty;
            foreach (char c in name)
            {
                if (c != ' ')
                    s += c;
                else
                    s += "%20";
            }
            return s;
        }
    }

    public class Album
    {
        public string? name;
        public string? artist;
        public string? art;
        public List<string>? songs;

        public int? releaseYear;

        public override string ToString()
        {
            return $"{name}, {artist}, {releaseYear},{art}, \n {songs}";
        }
    }

    public interface IGetAlbumLink
    {
        public abstract string AlbumLink(string albumSearchQuery);
    }
    public interface IGetCoverSourceLink
    {
        // Gets the best quality image link of the cover art
        public abstract string CoverLink(HtmlDocument doc);
    }
    public interface IGetArtistName
    {
        public abstract string Artist(HtmlDocument doc);
    }
    public interface IGetAlbumName
    {
        public abstract string Album(HtmlDocument doc);
    }
    public interface IGetSongs
    {
        public abstract List<string> Songs(HtmlDocument doc);
    }

    public class MusicSearch : IGetAlbumLink, IGetCoverSourceLink
    {
        protected HtmlWeb web = new HtmlWeb();

        public Album Generate(string search)
        {
            Album a = new Album();
            string link = AlbumLink(search);
            HtmlDocument albumpage = web.Load(link);

            a.art = CoverLink(albumpage);

            return a;
        }

        public virtual string AlbumLink(string search) => String.Empty;
        
        public virtual string CoverLink(HtmlDocument doc) => String.Empty;
    }

    public class AppleMusic : MusicSearch
    {

        public override string CoverLink(HtmlDocument doc)
        {
            HtmlNode picture = doc.DocumentNode.QuerySelectorAll("picture")[0];
            var src = picture.QuerySelectorAll("source")[1];
            return src.OuterHtml.Split(',').Last().Split(' ')[0];
        }

        public override string AlbumLink(string albumSearchQuery)
        {
            string url = "https://music.apple.com/us/search?term=" + formatalbumnameforurl(albumSearchQuery);
            HtmlDocument document = web.Load(url);

            // Selects the first album in the list 
            HtmlNodeCollection firstalbuminsearch = document.DocumentNode.SelectNodes(
                "//*[@id=\"scrollable-page\"]/main/div/div[2]/div[3]/div/div[2]/section/div[1]/ul/li[1]/div/div/div[1]/div[3]/a");

            return firstalbuminsearch[0].Attributes["href"].Value;
        }

        private static string formatalbumnameforurl(string name)
        {
            string s = string.Empty;
            foreach (char c in name)
            {
                if (c != ' ')
                    s += c;
                else
                    s += "%20";
            }
            return s;
        }


    }
}