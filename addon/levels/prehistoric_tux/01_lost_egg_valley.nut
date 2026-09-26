// PrehistoricTux — Level 01 scripted beats.
// Gameplay-critical logic stays in the level file; this script handles presentation.

PALASZARUSZ.set_visible(false);

function palaszarusz_reveal()
{
  Tux.use_scripting_controller(true);
  Tux.do_scripting_controller("left", false);
  Tux.do_scripting_controller("right", false);

  Camera.set_mode("manual");
  Effect.sixteen_to_nine(1);
  Camera.scroll_to(12840, 480, 3.2);

  wait(0.9);
  PALASZARUSZ.set_visible(true);
  PALASZARUSZ.set_action("roar");
  play_sound("sounds/yeti_roar.wav");

  wait(2.2);
  Effect.fade_out(1.2);
  wait(1.2);
  Level.finish(true);
}
