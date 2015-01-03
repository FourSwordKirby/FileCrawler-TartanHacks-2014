package  
{
	import org.flixel.*;

	public class Stairs extends FlxSprite 
	{
		//generate stair sprite to use
		[Embed(source = "../assets/gfx/DownStairs.png")] private static var DownSprite:Class;
		[Embed(source = "../assets/gfx/UpStairs.png")] private static var UpSprite:Class;
		
		//variables to indicate direction of stairs
		public var paired_stair:Stairs;
		public var floor:Floor;
		
		public function Stairs(X:int,Y:int,descend:Boolean,floor:Floor) 
		{
			super(X, Y);
			
			this.floor = floor;
			if (descend == true)
			{
				loadGraphic(DownSprite, false, true, 50, 50);
			}
			else
			{
				loadGraphic(UpSprite, false, true, 50, 50);
			}
		}
	}
}