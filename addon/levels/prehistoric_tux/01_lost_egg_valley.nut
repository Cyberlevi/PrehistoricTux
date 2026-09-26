// PrehistoricTux — Level 01 scripted beats.
// Keep gameplay-critical logic in the level file; this script is presentation only.

function palaszarusz_reveal()
{
  Tux.use_scripting_controller(true);
  Tux.do_scripting_controller("left", false);
  Tux.do_scripting_controller("right", false);

  Camera.set_mode("manual");
  Effect.sixteen_to_nine(1);
  Camera.scroll_to(12840, 480, 4);

  wait(1.6);

  // The final bespoke boss sprite will be revealed here. During the
  // bootstrap phase the camera reveal + story block establishes timing.
  Effect.fade_out(1.2);
  wait(1.2);
  Level.finish(true);
}
