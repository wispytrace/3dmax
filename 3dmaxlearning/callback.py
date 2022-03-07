import pymxs
rt = pymxs.runtime

# remove any previous callbacks:
rt.callbacks.removeScripts(id=rt.name('MyCallbacks'))

# function to print the notification param, which in the case of NodeCreated, is the node
def myCallback():
    print ('Callback fired!')
    notification = rt.callbacks.notificationParam()
    print (notification)

rt.callbacks.addScript(rt.Name('nodeCreated'), myCallback, id=rt.Name('MyCallbacks'))
# Will print something like this:
# Callback fired!
# $Sphere:Sphere005 @ [0.000000,0.000000,0.000000]

print(rt.callbacks.show(id=rt.Name('MyCallbacks'), asArray=True))

# Prints something like:
# #(#(#nodeCreated, #myCallbacks, false, false, "<function myCallback at 0x0000021020609828>()"))