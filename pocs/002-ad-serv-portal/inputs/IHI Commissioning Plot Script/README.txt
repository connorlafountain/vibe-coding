README

	The "IHI_cxplotscript" script is used to plot IHI commissioning test results on individual graphs and with appropriate axes and labeling.
	By using the "matplotlib" Python library, plots can be saved, zoomed into, and generally analyzed.
	This README will provide information on the file and how to use it.  

PYTHON

	Python can be downloaded and installed from the official website (https://www.python.org/).
	
	However, the easiest way to install Python on Windows is to go to the Microsoft Store app in Windows and
	install one of the Python 3.X versions (I recommend the latest non-beta version).
	
	Additionally, the script requires a few additional Python libraries to be installed to work properly (otherwise, it will give error messages).
	After Python is installed, use PowerShell or Command Prompt to install libraries using the following commands:
		pip install pandas
		pip install matplotlib
		pip install openpyxl
	
HOW TO USE

	1. Ensure Python and needed libraries are installed
	2. Ensure the script is using the correct filenames (i.e., file_name, and if needed file_name2, are equal to the files you want to plot)
	3. Open either Windows PowerShell or Command Prompt in the location with the test results file(s)
		(Tip: In the Windows file browser, hold "Shift" and right-click and an "Open PowerShell window here" option will be available)
	4. Run the script using the following syntax:
		>> python [filepath]\IHI_cxplotscript.py   (generic example)
		>> python C:\Users\pgiessner\Documents\Scripts\IHI_cxplotscript.py   (specific user example)
	5. The script will take 10-15 seconds to run and then plots will pop-up
	6. Analyze and/or save the plots; toolbar is in bottom-left of each plot
	7. To exit the script, select the terminal (PowerShell or Command Prompt) window and hit "Ctrl+C" (may take a few times)