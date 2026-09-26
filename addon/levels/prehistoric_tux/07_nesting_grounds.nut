// Nesting Grounds story reveal.

PALASZARUSZ_GROUNDS.set_visible(false);
STOLEN_EGG_GROUNDS.set_visible(false);
SPINO_GROUNDS.set_action("idle-left");

function grounds_reveal()
{
  Tux.use_scripting_controller(true);
  Tux.do_scripting_controller("left", false);
  Tux.do_scripting_controller("right", false);

  Camera.set_mode("manual");
  Effect.sixteen_to_nine(1);
  Camera.scroll_to(10000, 430, 2.6);

  wait(0.7);
  PALASZARUSZ_GROUNDS.set_visible(true);
  STOLEN_EGG_GROUNDS.set_visible(true);
  PALASZARUSZ_GROUNDS.set_action("roar");
  play_sound("sounds/yeti_roar.wav");

  wait(2.0);
  PALASZARUSZ_GROUNDS.set_action("charge");
  wait(0.8);
  PALASZARUSZ_GROUNDS.set_visible(false);
  STOLEN_EGG_GROUNDS.set_visible(false);

  Effect.fade_out(0.8);
  wait(0.8);
  Level.finish(true);
}
