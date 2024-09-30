import math # math module
import sys  # argv

# constants
w = 7.292115*pow(10,-5) #rad/s

# initialize script arguments
year = float('nan')
month = float('nan')
day = float('nan')
hour = float('nan')
minute = float('nan')
second = float('nan')
eci_x_km = float('nan')
eci_y_km = float('nan')
eci_z_km = float('nan')

# parse script arguments
if len(sys.argv)==10:
  year = float(sys.argv[1])
  month = float(sys.argv[2])
  day = float(sys.argv[3])
  hour = float(sys.argv[4])
  minute = float(sys.argv[5])
  second = float(sys.argv[6])
  eci_x_km = float(sys.argv[7])
  eci_y_km = float(sys.argv[8])
  eci_z_km = float(sys.argv[9])
else:
  print(\
   'Usage: '\
   'python3 eci_to_ecef.py year month day hour minute second eci_x_km eci_y_km eci_z_km'\
  )
  exit()

# Caculate Julian date for the given datetime
jd = (day-32075+int(1461*(year+4800+int((month-14)/12))/4)+int(367*(month-2-int((month-14)/12)*12)/12)-int(3*int((year+4900+int((month-14)/12))/100)/4))

# JD at midnight
jd_midnight = jd - 0.5

# Fractional day part based on the time (hour, minute, second)
d_frac = (second + 60 * (minute + 60 * hour)) / 86400.0
    
# Final fractional Julian Date
jd_frac = jd_midnight + d_frac

# Calculate GMST angle
T_UT1 = (jd_frac-2451545)/36525
theta_GMST = 67310.54841+(876600*60*60+8640184.812866)*T_UT1+0.093104*pow(T_UT1,2)+(-6.2*pow(10,-6)*pow(T_UT1,3))
GMST_rad = (theta_GMST%86400)*w
GMST_deg = GMST_rad*180/math.pi

# Time-Dependent Rotation to figure ecef, manually do dot product 
ecef_x_km = math.cos(-GMST_rad)*eci_x_km - math.sin(-GMST_rad)*eci_y_km
ecef_y_km = math.sin(-GMST_rad)*eci_x_km + math.cos(-GMST_rad)*eci_y_km
ecef_z_km = eci_z_km

# print ecef_x_km, ecef_y_km, and ecef_z_km
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)