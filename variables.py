""" Variables """

# Current game level
lvl = 1
# Default time for each lvl
default_timer = 15
# Storing current time
timer = default_timer
# True when ball hits bottom of the screen
bottom = False
# Running game_loop()
run = True
# Used when preventing ball to go straight up at the beginning
epsilon = 0.75
# Slow motion
slomo = False
# Default slow motion cooldown
slow_timer_default = 20
# Current slow motion cooldown
slow_timer = slow_timer_default
# Amount of slow motion actions available
slomo_amount = 0
# Default value of slow_timer2
slow_timer2_default = 75
# Current value of available "length" of slow motion
slow_timer2 = slow_timer2_default
# Value used to limit time of game communicates
death_counter = 0
# False to pause the timer
clock_run = True
