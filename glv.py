from math import *

a = 6378137;   # the Earth's semi-major axis
f  = 1/298.257;# flattening
wie = 7.2921151467e-5; 
b = (1- f)* a;  # semi-minor axis
e = sqrt(2* f- f**2);  
e2 =  e**2; # 1st eccentricity
ep = sqrt( a**2- b**2)/ b; 
ep2 =  ep**2; # 2nd eccentricity
wie = wie;  # the Earth's angular rate
g0 = 9.7803267714;  # gravitational force
mg = 1.0e-3* g0; # milli g
ug = 1.0e-6* g0; # micro g
mGal = 1.0e-3*0.01; # milli Gal = 1cm/s**2 ~= 1.0E-6*g0
ugpg2 =  ug/ g0**2;# ug/g**2
ppm = 1.0e-6;   # parts per million
deg = pi/180;   # arcdeg
min =  deg/60;   # arcmin
sec =  min/60;   # arcsec
hur = 3600; # time hour (1hur=3600second)
dps = pi/180/1; # arcdeg / second
dph =  deg/ hur;  # arcdeg / hour
dpss =  deg/sqrt(1); # arcdeg / sqrt(second)
dpsh =  deg/sqrt( hur);  # arcdeg / sqrt(hour)
dphpsh =  dph/sqrt( hur); # (arcdeg/hour) / sqrt(hour)
Hz = 1/1;   # Hertz
dphpsHz =  dph/ Hz;   # (arcdeg/hour) / sqrt(Hz)
ugpsHz =  ug/sqrt( Hz);  # ug / sqrt(Hz)
ugpsh =  ug/sqrt( hur); # ug / sqrt(hour)
mpsh = 1/sqrt( hur); # m / sqrt(hour)
mpspsh = 1/1/sqrt( hur); # (m/s) / sqrt(hour), 1*mpspsh~=1700*ugpsHz
ppmpsh =  ppm/sqrt( hur); # ppm / sqrt(hour)

