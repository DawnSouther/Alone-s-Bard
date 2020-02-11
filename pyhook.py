# -*- coding: utf-8 -*- # 
import pythoncom 
import PyHook3  
def onMouseEvent(event): 
    # 监听鼠标事件   
  print("MessageName:" + event.MessageName)  
  print("Message:" + str(event.Message)) 
  print("Time:" + str(event.Time))  
  print("Window:" + str(event.Window))  
  print("WindowName:" + event.WindowName)  
  print("Position:" + str(event.Position))  
  print("Wheel:" + str(event.Wheel))  
  print("Injected:" + str(event.Injected))     
  print("---")
  # 返回 True 以便将事件传给其它处理程序   
  # 注意，这儿如果返回 False ，则鼠标事件将被全部拦截   
  # 也就是说你的鼠标看起来会僵在那儿，似乎失去响应了   
  return True
  
def onKeyboardEvent(event):
  # 监听键盘事件   
  print("MessageName:" + event.MessageName)  
  print("Message:" + str(event.Message)) 
  print("Time:" + str(event.Time))  
  print("Window:" + str(event.Window))  
  print("WindowName:" + event.WindowName)  
  print("Ascii:" + chr(event.Ascii))   
  print("Key:" + event.Key)  
  print("KeyID:" + str(event.KeyID))  
  print("ScanCode:" + str(event.ScanCode))  
  print("Extended:" + str(event.Extended))  
  print("Injected:" + str(event.Injected))  
  print("Alt: " + str(event.Alt))  
  print("Transition" + str(event.Transition))  
  print("event:" + str(event))  
  print("---")   
  # 同鼠标事件监听函数的返回值   
  return True
 
def main():   
  # 创建一个“钩子”管理对象   
  hm = PyHook3.HookManager()   
  # 监听所有键盘事件   
  hm.KeyDown = onKeyboardEvent   
  # 设置键盘“钩子”   
  hm.HookKeyboard()   
  # 监听所有鼠标事件   
  hm.MouseAll = onMouseEvent   
  # 设置鼠标“钩子”   
  hm.HookMouse()   
  # 进入循环，如不手动关闭，程序将一直处于监听状态   
  pythoncom.PumpMessages()
 
if __name__ == "__main__":   
  main()