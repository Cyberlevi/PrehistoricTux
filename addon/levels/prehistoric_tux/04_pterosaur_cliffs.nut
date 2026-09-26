// Pterosaur Cliffs — gust timing.
// Wind objects are authored with (blowing #f) in the level file, so the import
// itself stays side-effect free and only trigger calls start/stop gusts.

function gust_a()
{
  GUST_A.start();
  wait(3.0);
  GUST_A.stop();
}

function gust_b()
{
  GUST_B.start();
  wait(3.4);
  GUST_B.stop();
}

function gust_c()
{
  GUST_C.start();
  wait(3.8);
  GUST_C.stop();
}

function gust_d()
{
  GUST_D.start();
  wait(4.1);
  GUST_D.stop();
}
