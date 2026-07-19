<h1 align="center">capeify</h1>
<p align="center">A tool to convert Windows cursor packs to Mousecape capes</p>
<p align="center">
<a href="https://github.com/mmemoo/capeify"><img width="300" alt="capeify logo" src="logo.png"></a></br>
</p>

# Downloading

</br>

**Capeify**

To download Capeify itself, simply:
```
pip install capeify
```

# How to use it
To convert a Windows cursor pack , run :
```
capeify convert --path PATH/TO/THE/CURSORPACK --inf-file INF_FILE_NAME --out OUT_FILE_PATH
```

# How it works
The program first parses the INF file and reads the [Strings],[AddReg] etc. entries and gets the cursor names and their corresponding cur/ani files,
after that those cur/ani files are parsed and their hotspot position,frame duration,frame count etc. are saved and they're converted to pngs, also the cursor names are translated into MacOS cursor identifiers.

After that a ready cape file template is filled with those data and its ready to use.

# Contributing
You can contribute to this project code-wise by cloning this repo and fixing issues, adding new features, fixing bugs and completing the TODO lists elements (in order) down below and creating pull requests.

You can also contribute to this project idea and feedback wise by create issues telling me if there are any problems like if a Win cursor name is translated into the wrong MacOS identifier or if a identifier is missing,if a cursors hotspot is wrong etc.

Also you can recommend features to contribute and further develop this project.

# TODO
- [x] Fix the issue with .ani files caused by the mousecape frame count limit
- [x] Fix the issue caused by cur files in ani files having varying height
- [x] Fix the issue with ani files caused by the wrong calculation of the frame count
- [ ] Create a easier to use app
- [ ] Fix the false frame duration issue with .ani files
- [ ] Fix issues caused by non-centered .cur and (possibly) .ani files
- [ ] Add min cursor size and cursor size capping
- [ ] Create tests.
- [ ] Add cape to windows cursor pack conversion
