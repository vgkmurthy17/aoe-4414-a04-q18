# eci_to_ecef.py
#
# Usage: python3 year month day hour minute second eci_x_km eci_y_km eci_z_km
# Converts eci to ecef
# 
# Parameters:
#  year
#  month
#  day
#  hour
#  minute
#  second
#  eci_x_km
#  eci_y_km
#  eci_z_km
# Output:
#  Prints the ecef x, y, and z coordinates
#
# Written by Vineet Keshavamurthy
# Other contributors: None
#
# This work is licensed under CC BY-SA 4.0


# Earth rotational speed in rad/sec
import math
import sys

w_rot_speed = 7.292115e-5

# Declare input variables
year = float('nan')
month = float('nan')
day = float('nan')
hour = float('nan')
minute = float('nan')
second = float('nan')
eci_x_km = float('nan')
eci_y_km = float('nan')
eci_z_km = float('nan')

# Argument number check
if len(sys.argv) == 10:
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
    print("Number of arguments passed is not valid, recheck your command line statement")
    sys.exit()

# Julian day calculation
offset_1 = (14-month)//12
year_component = year+4800-offset_1
month_component = month-2+offset_1*12
day_contribution = day-32075
julian_term_1 = 1461* year_component // 4
julian_term_2 = 367*month_component // 12
century_corr = (year_component+4900) // 100
julian_term_3 = 3*century_corr//4
julian_day = day_contribution+julian_term_1+julian_term_2-julian_term_3

# Calculate the fractional day
seconds_in_day = 86400.0
total_seconds = second +(minute*60) + (hour*3600)
fractional_day = total_seconds/seconds_in_day
julian_full_day = julian_day+fractional_day - 0.5

# Time in Julian centuries
century_time = (julian_full_day-2451545.0)/36525.0

# Calculation for GMST
gmst_term = 67310.54841
gmst_century_term = (876600*3600+8640184.812866)*century_time
gmst_square_term = 0.093104*century_time**2
gmst_cube_term = -6.2e-6*century_time**3

# Final GMST in seconds
gmst_seconds = gmst_term+gmst_century_term+gmst_square_term+gmst_cube_term

# Convert GMST into radians
gmst_radians = (gmst_seconds % seconds_in_day) * w_rot_speed

# Calculate ECEF coordinates by using rotation formula
ecef_x_km = -math.sin(-gmst_radians)*eci_y_km + eci_x_km * math.cos(-gmst_radians)
ecef_y_km = -(math.cos(-gmst_radians)*eci_y_km + math.sin(-gmst_radians)*eci_x_km)
ecef_z_km = eci_z_km

# Print ECEF coordinates
print(ecef_x_km)
print(ecef_y_km)
print(ecef_z_km)