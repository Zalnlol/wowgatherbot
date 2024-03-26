# wowgatherbot
# Credit to pygamebot: https://www.youtube.com/@pgamebot
# This script is use for auto gathering herb / ore and interupt in World of Warcraft
# Using python openCV library
# The gathering task is done using minimap as navigation system - see screenshot for example.
# Set minimap to auto rotate
# Set up UI like screenshot using the import UI note following:
1 39 0 0 1 7 7 UIParent 0.0 45.0 -1 ##$$%/&&'%)$+$,$ 0 1 1 6 0 MainMenuBar 0.0 5.0 -1 ##$$%/&&'%(#,$ 0 2 1 6 0 MultiBarBottomLeft 0.0 5.0 -1 ##$$%/&&'%(#,$ 0 3 1 5 5 UIParent -5.0 -77.0 -1 #$$$%/&('%($,$ 0 4 1 2 0 MultiBarRight -5.0 0.0 -1 #$$$%/&('%($,$ 0 5 1 1 4 UIParent 0.0 0.0 -1 ##$$%/&('%(&,# 0 6 1 1 7 MultiBar5 0.0 0.0 -1 ##$$%/&('%(#,$ 0 7 1 1 7 MultiBar6 0.0 0.0 -1 ##$$%/&('%(#,$ 0 10 1 6 0 MainMenuBar 0.0 5.0 -1 ##$$&('% 0 11 1 6 0 MainMenuBar 0.0 5.0 -1 ##$$&('%,# 0 12 1 6 0 MainMenuBar 0.0 5.0 -1 ##$$&('% 1 -1 1 4 4 UIParent 0.0 0.0 -1 ##$#%# 2 -1 0 0 2 BuffFrame 4.0 0.0 -1 ##$$%) 3 0 1 0 0 UIParent 4.0 -4.0 -1 $#3# 3 1 0 3 3 UIParent 344.7 331.4 -1 %$3# 3 2 1 0 0 TargetFrame 250.0 -240.0 -1 %#&#3# 3 3 0 0 0 UIParent 184.7 -266.0 -1 '$(#)#-C.'/#1$3# 3 4 0 0 0 UIParent 84.7 -266.0 -1 ,#-#.#/#0%1#2( 3 5 1 5 5 UIParent 0.0 0.0 -1 &#*$3# 3 6 0 2 2 UIParent -244.7 -306.0 -1 -#.#/#4& 3 7 1 4 4 UIParent 0.0 0.0 -1 3# 4 -1 0 0 6 PlayerFrame 20.0 13.0 -1 # 5 -1 0 4 4 UIParent 360.0 -253.0 -1 # 6 0 0 1 1 UIParent 220.0 -6.0 -1 ##$#%#&.(()( 6 1 1 2 8 BuffFrame -13.0 -15.0 -1 ##$#%#'+(()( 7 -1 1 6 0 MainMenuBar 0.0 5.0 -1 # 8 -1 0 6 6 UIParent 35.0 50.0 -1 #'$A%$&7 9 -1 1 6 0 MainMenuBar 0.0 5.0 -1 # 10 -1 1 0 0 UIParent 16.0 -116.0 -1 # 11 -1 1 8 8 UIParent -9.0 85.0 -1 # 12 -1 1 2 2 UIParent -110.0 -275.0 -1 #K$# 13 -1 1 8 8 MicroButtonAndBagsBar 0.0 0.0 -1 ##$#%)&- 14 -1 1 2 2 MicroButtonAndBagsBar 0.0 0.0 -1 ##$#%( 15 0 1 7 7 StatusTrackingBarManager 0.0 0.0 -1 # 15 1 1 7 1 MainStatusTrackingBarContainer 0.0 0.0 -1 # 16 -1 1 5 5 UIParent 0.0 0.0 -1 #( 17 -1 1 1 1 UIParent 0.0 -100.0 -1 ## 18 -1 1 5 5 UIParent 0.0 0.0 -1 #- 19 -1 1 7 7 UIParent 0.0 0.0 -1 ##