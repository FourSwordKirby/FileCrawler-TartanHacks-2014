package  
{
	import org.flixel.*;

	public class Enemy extends FlxSprite 
	{
		//generate stair sprite to use
		[Embed(source = "../assets/gfx/DOCSprite.png")] private static var DOCSprite:Class;
		[Embed(source = "../assets/gfx/PDFSprite.png")] private static var PDFSprite:Class;
		
		//variables to indicate direction of stairs
		public var myName:FlxText
		
		public function Enemy(X:int, Y:int, type:String, name:String, size:int) 
		{
			super(X, Y);
			if (type == "DOC")
				loadGraphic(DOCSprite, false, true, 50, 50);
			else if (type == "PDF")
				loadGraphic(PDFSprite, false, true, 50, 50);
			health = size;
			myName = new FlxText(x -10, y - 20, 50, name);
		}
	}
}