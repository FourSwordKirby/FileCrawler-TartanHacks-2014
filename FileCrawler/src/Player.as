package  
{
	import org.flixel.*;

	public class Player extends FlxSprite 
	{
		//generate player sprite to use
		[Embed(source = "../assets/gfx/Bitman.png")] private static var CharacterSprite:Class;
		
		//variables to control player movement
		
		public var inBattle:Boolean; //used to define whether the player is in the overworld or in battle
		
		public function Player(X:int,Y:int) 
		{
			super(X,Y);
			loadGraphic(CharacterSprite, true, true,50,50);
			
			//Phsysics[!?]
			maxVelocity.x = 300;
			maxVelocity.y = 600;
			
			/*
			 * animations needed
			 * moving
			 * victory
			 * surprise
			 * holding objects
			 */ 
			addAnimation("move_right", [0, 1], 5,true);			//self explanatory
			addAnimation("move_up", [2, 3], 5,true);			//self explanatory
			addAnimation("move_left", [4,5], 5,true);			//self explanatory
			addAnimation("move_down", [6,7],5,true);			//self explanatory
		}
		
		override public function update():void
		{	
			var moving:Boolean = false;
			if (FlxG.keys.RIGHT)
			{
				this.x += 4;
				moving = true;
				play("move_right");
			}
			if (FlxG.keys.LEFT)
			{
				//facing = LEFT;
				this.x -= 4;
				moving = true;
				play("move_left");
			}
			if (FlxG.keys.UP)
			{
				//facing = ;
				this.y -= 4;
				moving = true;
				play("move_up");
			}
			if (FlxG.keys.DOWN)
			{
				//facing = ;
				this.y += 4;
				moving = true;
				play("move_down");
			}
			if (!moving)
				play("idle");
			/*if (this.x % 50 != 0)
			{
				this.x += 10;
			}
			else if (this.y % 50 != 0)
			{
				this.y += 10;
			}*/
		}
		//********IMPLEMENT THESE******************
		public function restorePhysics():void 
		{

		}
		public function die(mapheight:int):void
		{

		}
		public function victory():void 
		{
			
		}
		public function doAttack():void 
		{
			
		}
	}

}