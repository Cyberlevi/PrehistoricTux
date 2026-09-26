// Palaszarusz Crater — scripted boss prototype.
// Three increasingly fast charges create a real dodge encounter without an engine fork.
// A later custom C++ boss can preserve these timings while adding health/AI.

PALASZARUSZ_BOSS.set_visible(false);
PALASZARUSZ_BOSS.set_solid(false);
PALASZARUSZ_BOSS.enable_gravity(false);
STOLEN_EGG_FINAL.set_visible(false);

function boss_reset(x, y)
{
  PALASZARUSZ_BOSS.set_velocity(0, 0);
  PALASZARUSZ_BOSS.set_solid(false);
  PALASZARUSZ_BOSS.set_visible(false);
  PALASZARUSZ_BOSS.set_pos(x, y);
}

function boss_charge(speed, y)
{
  boss_reset(9568, y);
  PALASZARUSZ_BOSS.set_action("roar");
  PALASZARUSZ_BOSS.set_visible(true);
  play_sound("sounds/yeti_roar.wav");
  wait(0.75);

  PALASZARUSZ_BOSS.set_action("charge");
  PALASZARUSZ_BOSS.set_solid(true);
  PALASZARUSZ_BOSS.set_velocity(-speed, 0);
  wait(2.20);

  PALASZARUSZ_BOSS.set_solid(false);
  PALASZARUSZ_BOSS.set_velocity(0, 0);
  PALASZARUSZ_BOSS.set_visible(false);
  wait(0.70);
}

function palaszarusz_battle()
{
  // Phase 1: ground-level charge.
  boss_charge(650, 620);

  // Phase 2: faster and slightly higher, forcing different platform use.
  boss_charge(760, 560);

  // Phase 3: fastest pass.
  boss_charge(880, 610);

  // The Palaszarusz retreats. The egg remains.
  boss_reset(9568, 620);
  STOLEN_EGG_FINAL.set_visible(true);

  Tux.use_scripting_controller(true);
  Tux.do_scripting_controller("left", false);
  Tux.do_scripting_controller("right", false);

  Camera.set_mode("manual");
  Effect.sixteen_to_nine(1);
  Camera.scroll_to(8864, 600, 2.0);
  wait(2.2);

  Effect.fade_out(1.0);
  wait(1.0);
  Level.finish(true);
}
