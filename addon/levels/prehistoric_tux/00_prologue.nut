function initialize()
{
  start_cutscene();

  TUX.set_action("big-stand-right");
  pier.set_solid(false);

  Tux.deactivate();
  Tux.set_visible(false);
  Tux.set_pos(96, 480);

  Camera.set_pos(50, 200);
  Camera.set_scale_anchor(1.2, 4);

  Effect.sixteen_to_nine(0);
  Effect.fade_in(2);
  Camera.scroll_to(200, 500, 10);

  wait(2);
  TUX.set_velocity(100, -400);
  TUX.set_action("big-jump-right");
  wait(0.5);
  pier.set_solid(true);
  TUX.set_action("big-fall-right");
  wait(0.2);
  TUX.set_velocity(0, 0);
  TUX.set_action("big-stand-right");
  wait(0.5);

  trigger_state("textbox");

  wait(19);
  TUX.set_velocity(150, 0);
  TUX.set_action("big-walk-right");
  Camera.scroll_to(3000, Camera.get_y(), 10);
  wait(8);

  trigger_state("end_level");
  end_cutscene();
}

function textbox()
{
  Text.set_text(_("One morning, Tux found a warm egg beside a shattered nest."));
  Text.fade_in(0.5);
  wait(4);
  Text.fade_out(0.5);
  wait(1);

  Text.set_text(_("Huge footprints crossed the ground. Three sharp claws pointed toward the mountains."));
  Text.fade_in(0.5);
  wait(5);
  Text.fade_out(0.5);
  wait(1);

  Text.set_text(_("A shadow passed overhead. Whatever had taken the egg was not alone."));
  Text.fade_in(0.5);
  wait(4);
  Text.fade_out(0.5);
  wait(1);

  Text.set_text(_("Tux followed the trail into a forgotten land where dinosaurs still ruled."));
  Text.fade_in(0.5);
  wait(5);
  Text.fade_out(0.5);
}

function end_level()
{
  Effect.fade_out(2);
  wait(3);
  stop_music(1);
  wait(1);
  Level.finish(true);
}

state_idx <- 0;
states <- { init=0, start=1, textbox=2, end_level=3 };

function trigger_state(state)
{
  local idx = states[state];
  if(!idx || idx <= state_idx)
    return;

  state_idx = idx;

  switch(state) {
    case "start":
      initialize();
      break;
    case "textbox":
      textbox();
      break;
    case "end_level":
      end_level();
      break;
  }
}
