package 
{
	import flash.text.engine.ElementFormat;
	import mx.core.ButtonAsset;
	import mx.core.FlexApplicationBootstrap;
	import mx.core.FlexSprite;
	import org.flixel.*;
	import flash.display.Graphics;
	import flash.utils.getQualifiedSuperclassName; //used to figure out the super class of some classes
	
	public class  BattleState extends FlxState
	{
		[Embed(source = "../assets/music/Uber_Battle.mp3")] private var BattleBGM:Class;
		private var backstate:OverworldState; //this holds our previous state before the battle
		public var player:Player;
		public var name:String;
		public var health:int;
		public var type:String;
		public var i:int;
		
		public function BattleState(name:String, health:int, type:String, prevstate:OverworldState) 
		{
			//player.health = health;
			//enemy = theenemy;
			this.name = name;
			this.health = health;
			this.type = type;
			backstate = prevstate;
		}
		
		override public function create():void
		{
			FlxG.stream("../assets/music/Battle.mp3",0.5, true); //Potentially used later to adjust volume settings. 
			FlxG.play(BattleBGM);
			
			var player:Player = new Player(100, 200);
			var enemy:Enemy = new Enemy(400, 200, type, name, health);
			add(player);
			add(enemy);
			/*trace("hello");
			
			
			*/
			super.create();
		}
		
		override public function update():void
		{
			if (FlxG.keys.justPressed("A"))
			{
				i++;
			}
			if (i > 20)
			{
				FlxG.switchState(backstate);
				FlxG.resetState();
			}
			super.update();
		}
	}

}