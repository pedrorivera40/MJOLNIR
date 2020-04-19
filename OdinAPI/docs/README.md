# Getting started with doxygen for python documentation

In order to generate class and method documentation for classes within OdinAPI you need to install Doxygen. It is a documenbtation generator much like Javadoc or JSDoc. In order to install it on your system run the following command:
```bash
sudo apt-get install doxygen-gui
```
With that you are ready to use doxygen by runningh the command: `doxywizard`

Note: You might need to install qt5 for doxywizard to run properly
```bash
sudo apt-get install build-essential

sudo apt-get install qtcreator

sudo apt-get install qt5-default
```
## Doxypypy
Now doxygen is not fully optimized to understand python docstring syntax. So you need to install a filter that propperly formats your python files, enter doxypypy. To install doxypypy from within your virtualenv run the following command:
```bash
pip3 install doxypypy
```
More information on Doxypypy [here.](!https://github.com/Feneric/doxypypy)

## Getting doxypypy to work with doxygen
In order to get doxygen to work with doxypypy you must edit the `FILTER_PATTERNS ` option. To do so run the doxygen wizard, on the terminal run the following command:
```
doxywizard
```
The Doxygen GUI should open in the **Wizzard** tab. From here fill the information of the project. 

In **Step 1:** write the project's directory `<path/to>/MJOLNIR/OdinAPI`

In **Step 2:** Fill out the Projects information. In the field to specify the the directory to scan for source code, use OdinAPI by specifying is path like above. And select the option to scan recursively. In the field to specify the destination directory for the generated directories fill in `<path/to>/MJOLNIR/OdinAPI/docs`

After that, go to the **Expert** tab. Here in the **Topics** pannel navigate to the *Input* section, in here look for the `FILTER_PATTERNS ` field and write in `*.py=py_filter` and add it to the filters.

Now in the projects root directory create a new file with the name `py_filter`. Open it in an editor and write the following:
```bash
#!/bin/bash
doxypypy -a -c  $1
```
This is a bash script is the filter that formats python files passed in to an output understandable by doxygen. Save the file and close. Now you need to make it executable by running 
```bash
chmod +x py_filter
```
Copy this file to your bin, so it is available system wide.
```bash
sudo cp py_filter /usr/bin/
```

Now, go back to the Doxygen gui and click on the **Run** tab, here click on the run button, once its done running it should have generated the documentation for the Project. And you can click on the Show HTML output to view the generated files.

You can now close the doxygen gui and select to save the configuration to generate a `Doxygen` file which will contain the doxygen configuration and can be opened in Doxygen GUI to do further edits.