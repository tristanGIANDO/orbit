**Copyright (c) 2023 tristanGIANDO**

*Permission is hereby granted, free of charge, to any person obtaining a copy*
*of this software and associated documentation files (the "Software"), to deal*
*in the Software without restriction, including without limitation the rights*
*to use, copy, modify, merge, publish, distribute, sublicense, and/or sell*
*copies of the Software, and to permit persons to whom the Software is*
*furnished to do so, subject to the following conditions:*

*The above copyright notice and this permission notice shall be included in all*
*copies or substantial portions of the Software.*

*THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR*
*IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,*
*FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE*
*AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER*
*LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,*
*OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE*
*SOFTWARE.*

<h2 align="center" style="margin:1em;">
    <img src="solar_system_cartography\icons\title_dark.png"
         alt="orbit"></a>
</h2>

<h3 align="center">
    Orbit data calculator and 3D representation
</h3>

### A brief introduction
I developed this tool for learning purposes and with the aim of getting closer to the field of **astronomy**, trying to link **science and 3D**.

The results obtained are correct but not as accurate as possible because I don't yet have the necessary knowledge. What's more, I haven't used any external libraries that automate everything. Everything is done using the **math** library.

The reason the package is open-source is so that I can exchange ideas and learn from others, and I'd be delighted to do that!

##
This tool is written in **Python 3**, **Qt** and uses **SQLite**.
Associated plug-in (no require) : **Autodesk Maya 2022+**

# INSTALL
Simply run the file `launcher.exe` ( or `launcher.py` if you want to open it from an IDE ).

### USAGE
Once you have opened the interface, you need to determine a location where the project can be saved.
Click on the `set_project` button and select a folder.
A database is automatically created and this is where your data will be stored.

To add an object, simply enter the required data in the `Create` tab and click on the button of the same name.

If you are in standalone mode, the object you create will be added to the database, but to view it in 3D, you need to be in Autodesk Maya.

If this is not the case, don't panic, every time you open a project, Maya will read all the contents of the database and create anything that doesn't exist.
So there's never any need to save your scenes - everything is done automatically, just set up a project!

# API DOCUMENTATION

```mermaid
flowchart TD
    AP{ORBIT};
    A(class Api) -- inits --> B(class Database);
    A -- inits --> C(class ObjectInOrbit);
    A -- inits --> D(class Star);
    C -- is added into --> B
    D -- is added into --> B
    B -- sends information --> A
    E{ui} -- calls --> A
```

## INSTRUCTIONS FOR USE
```py
from solar_system_cartography.api import Api

new_object = [
            # name,
            # type,
            # parent,
            # mass,
            # orbital period,
            # object inclination,
            # semi major axis,
            # orbit inclination,
            # eccentricity,
            # ascending node,
            # argument of periapsis,
            # random perihelion / perigee date
        ]

project_path = r"path\to\a\directory"

api = Api(project_path)
api.add_element(new_object)
```
