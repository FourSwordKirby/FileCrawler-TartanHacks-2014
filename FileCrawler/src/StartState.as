package  
{
	import com.greensock.events.LoaderEvent;
	import com.greensock.loading.DataLoader;
	import mx.core.FlexSprite;
	import org.flixel.*;
	import flash.text.*;
	import flash.events.Event;
	import com.greensock.*;
	/**
	 * ...
	 * @author rojerplz
	 */
	
	public class StartState extends FlxState
	{
		FlxG.debug;
		//******Eventually put title screen things***********
		//Title screen will look like LOZ title screen or whatever
		
		//******Background Music*****************************
		//Battle on the Big Bridge
		[Embed(source = "../assets/music/Battle.mp3")] private var BattleBGM:Class;
		[Embed(source = "../assets/gfx/logo.png")] private var DATLogo:Class
		//*******Buttons and things on the screen************
		private var StartButton:FlxButton = new FlxButton(300, 300, "Activate Crawl.exe", startGame);
		private var inputField:TextField = new TextField();
		private var loaded:Boolean = false;
		private var loader:DataLoader;
		
		private function finished(e:LoaderEvent):void
		{
			loaded = true;
		}

		override public function create():void
		{
			loader = new DataLoader('temp.txt', { onComplete:finished } );
			loader.load()
			//All of this stuff is to create an input field that will hold out giant ass string
			inputField.type = "input";
			inputField.border = true;
			inputField.width = 600;
			inputField.height = 200;
			inputField.x = 100;
			inputField.y = 100;
			inputField.multiline = true;
			inputField.background = true;
			inputField.backgroundColor = 0xFFFFFF;
			inputField.visible = false;
			//This adds out input field to the game. 
			FlxG.stage.addChild(inputField);

			var logo:FlxSprite = new FlxSprite(250, 100, DATLogo);
			add(logo);
			
			add(StartButton);
			FlxG.stream("../assets/music/Battle.mp3",0.5, true); //Potentially used later to adjust volume settings. 
			FlxG.play(BattleBGM);
			FlxG.mouse.show();
		}
		override public function update():void
		{
			super.update();
		}

		//This function will take us from the start menu state and put us into the game itself.
		public function startGame():void {
			if (!loaded) return;
			var levelstring:String = loader.content;
			levelstring = levelstring.split("\r").join("");
			inputField.text = levelstring;
			
			//These variables are here to pass the text to the game. This is our workaround for not being able to use dynamically generated .txt files
			var overworld:OverworldState = new OverworldState;
			
			//Putting our input into the state to make the level. 
			//var pattern:RegExp = //r/gi;
			overworld.spec = levelstring.split("\r").join("\n");
			FlxG.switchState(overworld);
			
			//removes the input. 
			FlxG.stage.removeChild(inputField);
		}
		
	}

}