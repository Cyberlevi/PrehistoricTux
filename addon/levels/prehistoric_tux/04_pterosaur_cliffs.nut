// Pterosaur Cliffs — gust timing.
// Short bursts make the wind readable and prevent permanent forced movement.

GUST_A.stop();
GUST_B.stop();
GUST_C.stop();
GUST_D.stop();

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
