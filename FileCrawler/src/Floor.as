package  
{
	import org.flixel.FlxG;
	import org.flixel.FlxGroup;
	import org.flixel.FlxObject;
	import org.flixel.FlxTilemap;
	
	public class Floor extends FlxTilemap 
	{
		public var name:String;
		public var parentname:String;
		public var stairGroup:FlxGroup;	//This holds all the stairs associated with this floor.
		public var map:FlxTilemap;
		public var files:int; 	//This tells us how many files we have
		public var subdirectories:int; //This tells us how many folders we have (this translates to stairs)
		public var enemies:Array = Array(2);
		
		public function Floor() 
		{
			stairGroup = new FlxGroup
			files = 0;
			subdirectories = 0;
		}
		
		public function determineStair(player:FlxObject):Stairs
		{
			for each (var stair:Stairs in stairGroup.members)
			{
				if (Math.abs(stair.x - player.x) < 50 || Math.abs(stair.y - player.y) < 50)
					return stair;
			}
			return stair;
		}
	}

}