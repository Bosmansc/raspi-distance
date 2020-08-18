# from tplight import LB130
# from tpplug import HS100
#
# if __name__ == '__main__':
#     try:
#         while True:
#             print("Measuring distance...")
#             dist = distance()
#             print("Measured Distance = %.1f cm" % dist)
#
#             dist_threshold = 5
#
#             if dist < dist_threshold:
#                 print("too close: light off")
#                 light.off()
#
#             if dist > dist_threshold:
#                 print("far enough: light on")
#                 light.on()
#
#             time.sleep(1)
#
#     # Reset by pressing CTRL + C
# except KeyboardInterrupt:
# print("Measurement stopped by User")
# GPIO.cleanup()