#$language = "VBScript"
#$interface = "1.0"

crt.Screen.Synchronous = True

' This automatically generated script may need to be
' edited in order to work correctly.

Sub Main
	Set fso = CreateObject("Scripting.FileSystemObject")
    Set file = fso.OpenTextFile("E:\AutoInspect\equipmentInfo.txt")
	crt.Window.Show 3
	Do Until file.AtEndOfStream 
		line = file.ReadLine
		commendAndLog line
	Loop
	crt.Quit()

End Sub

Sub commendAndLog(line)
	equipmentInfo = Split(line)
	ip = equipmentInfo(0)
	uname = equipmentInfo(1)
	pwd = equipmentInfo(2)
	equip_type = equipmentInfo(3)
	Call crt.Session.Log(False)
	crt.session.ConnectInTab "/SSH2 /L "&uname&" /PASSWORD "&pwd&" "&ip
	crt.Session.LogFileName = "E:\AutoInspect\Logs\%H.txt"
	Call crt.Session.Log(True)
	crt.Screen.Synchronous = True
	select case equip_type
		case "FW"
			call Juniper_SRX3600Commend
			crt.screen.WaitForString ">"
		case "SW"
			call H3C_12518
			crt.screen.WaitForString ">"
		case "F5"
			call F5_2400
			crt.screen.WaitForString "#"
		case Else
			msgbox "Data Error"
	end select
	'crt.screen.WaitForString ">"
	Call crt.Session.Log(False)
	crt.session.disconnect
End Sub

Sub Juniper_SRX3600Commend()
	crt.screen.WaitForString ">"
	crt.Screen.Send "show chassis alarms | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show system alarms | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show system uptime | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show chassis routing-engine | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show chassis cluster status | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show chassis fpc pic-status | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show chassis environment pem | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show security monitoring performance spu | no-more" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "show security monitoring | no-more" & chr(13)
End Sub

Sub H3C_12518()
	crt.screen.WaitForString ">"
	crt.Screen.Send "screen-length disable" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display cpu-usage" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display memory" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display version" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display device" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display environment" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display alarm" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display fan" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display ntp-service status" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send "display irf link" & chr(13)
	crt.screen.WaitForString ">"
	crt.Screen.Send chr(13)
End Sub

Sub F5_2400()
	crt.screen.WaitForString "#"
	crt.Screen.Send "tmsh" & chr(13)
	crt.screen.WaitForString "#"
	crt.Screen.Send "show sys performance connection" & chr(13)
	crt.screen.WaitForString "#"
	crt.Screen.Send "show sys performance system" & chr(13)
	crt.screen.WaitForString "#"
	crt.Screen.Send "show sys performance throughput" & chr(13)
	crt.screen.WaitForString "#"
	crt.Screen.Send chr(13)
End Sub