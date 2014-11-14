Recognito: 3D Gesture Recognition Using Leap Motion  
CS3235 Project  
AY2014/15 Group 12  

Abstract  
Living in Information Age, people use their digital devices with the rapidly increasing demands for both convenience and security. In this project, Recognito, a 3-dimensional gesture recognition application using Leap Motion is implemented. Users are identified by their gestures in the application. This application enhances user experience while accuracy and security of it are solid and never sacrificed.  

Commands  
./Recognito.py [Modes] [Picture Path]  
-h: Print help manual  
-s: Set benchmarking gesture  
-a: Authenticate your gesture against benchmarking gesture  
-b: Use binary mode  
-g: Use gesture mode  
-p: Use picture mode  
[Picture Path]: Path of the picture used in picture mode  

Examples  
Print help manual  
./Recognito.py -h  
Set benchmarking gesture using binary mode  
./Recognito.py -s -b  
Authenticate using binary mode  
./Recognito.py -a -b  
Set benchmarking gesture using gesture mode  
./Recognito.py -s -g  
Authenticate using gesture mode  
./Recognito.py -a -g  
Set benchmarking gesture using picture mode, with the picture doge.jpg  
./Recognito.py -s -p doge.jpg  
Authenticate using binary mode, with the picture doge.jpg  
./Recognito.py -a -p doge.jpg  
