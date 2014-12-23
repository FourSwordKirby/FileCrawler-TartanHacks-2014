package  
{
	import org.flixel.*;

	public class Stairs extends FlxSprite 
	{
		//generate stair sprite to use
		[Embed(source = "../assets/gfx/DownStairs.png")] private static var DownSprite:Class;
		[Embed(source = "../assets/gfx/UpStairs.png")] private static var UpSprite:Class;
		
		//variables to indicate direction of stairs
		public var descend:Boolean //indicates whether the stair is going down a level or up a level
		public var above:Floor; //indicates the top level of that stair
		public var below:Floor; //indicates the bottomw level of that stair
		
		public function Stairs(X:int,Y:int,descend:Boolean,above:Floor, below:Floor) 
		{
			super(X, Y);
			
			this.above = above;
			this.below = below;
			if (descend == true)
			{
				this.descend = true;
				loadGraphic(DownSprite, false, true, 50, 50);
			}
			else
			{
				this.descend = false;
				loadGraphic(UpSprite, false, true, 50, 50);
			}
		}
	}
}