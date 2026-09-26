// PrehistoricTux — Level 01 scripted beats.
// Gameplay-critical geometry remains in the level file.
// Scripted creatures are used for readable set-piece attacks without requiring an engine fork yet.

PALASZARUSZ.set_visible(false);
CAVEMAN_GUIDE.set_action("idle-left");
SPINOSAURUS_CAMEO.set_action("idle-left");

SNAKE_AMBUSH_1.set_visible(false);
SNAKE_AMBUSH_1.set_solid(false);
SNAKE_AMBUSH_1.enable_gravity(false);

SNAKE_AMBUSH_2.set_visible(false);
SNAKE_AMBUSH_2.set_solid(false);
SNAKE_AMBUSH_2.enable_gravity(false);

PTERO_DIVE_1.set_visible(false);
PTERO_DIVE_1.set_solid(false);
PTERO_DIVE_1.enable_gravity(false);

PTERO_DIVE_2.set_visible(false);
PTERO_DIVE_2.set_solid(false);
PTERO_DIVE_2.enable_gravity(false);

function snake_ambush_1()
{
  SNAKE_AMBUSH_1.set_action("left");
  SNAKE_AMBUSH_1.set_visible(true);
  play_sound("sounds/brick.wav");
  wait(0.25); // telegraph before the strike
  SNAKE_AMBUSH_1.set_solid(true);
  SNAKE_AMBUSH_1.set_velocity(-300, 0);
  wait(1.25);
  SNAKE_AMBUSH_1.set_velocity(0, 0);
  wait(0.75);
  SNAKE_AMBUSH_1.set_solid(false);
  SNAKE_AMBUSH_1.set_visible(false);
}

function snake_ambush_2()
{
  SNAKE_AMBUSH_2.set_action("left");
  SNAKE_AMBUSH_2.set_visible(true);
  play_sound("sounds/brick.wav");
  wait(0.30);
  SNAKE_AMBUSH_2.set_solid(true);
  SNAKE_AMBUSH_2.set_velocity(-340, 0);
  wait(1.30);
  SNAKE_AMBUSH_2.set_velocity(0, 0);
  wait(0.65);
  SNAKE_AMBUSH_2.set_solid(false);
  SNAKE_AMBUSH_2.set_visible(false);
}

function ptero_dive_1()
{
  PTERO_DIVE_1.set_action("left");
  PTERO_DIVE_1.set_visible(true);
  play_sound("sounds/willocatch.wav");
  wait(0.30); // wingbeat warning
  PTERO_DIVE_1.set_solid(true);
  PTERO_DIVE_1.set_velocity(-390, 190);
  wait(1.8);
  PTERO_DIVE_1.set_solid(false);
  PTERO_DIVE_1.set_visible(false);
}

function ptero_dive_2()
{
  PTERO_DIVE_2.set_action("left");
  PTERO_DIVE_2.set_visible(true);
  play_sound("sounds/willocatch.wav");
  wait(0.25);
  PTERO_DIVE_2.set_solid(true);
  PTERO_DIVE_2.set_velocity(-430, 220);
  wait(1.9);
  PTERO_DIVE_2.set_solid(false);
  PTERO_DIVE_2.set_visible(false);
}

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
