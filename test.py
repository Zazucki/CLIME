import os

linuxText = []
windowsText = []

linDir = "levels/linux"
for filename in os.listdir(linDir):
	file = os.path.join(linDir, filename)
	with open(file, 'r') as myfile:
		data = myfile.read()
		linuxText.append(data)

winDir = "levels/windows"
for filename in os.listdir(winDir):
	file = os.path.join(winDir, filename)
	with open(file, 'r') as myfile:
		data = myfile.read()
		windowsText.append(data)

print(linuxText)
print(windowsText)
