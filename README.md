# Vladimir Șontea (NetID: vs3006) Capstone Project

## Full Pipeline Implementation of a Label-Free GNSS Spoofing Framework

**About**
This section concerns the implementation of the pipeline originally conceived in [this](https://doi.org/10.1109/LCOMM.2026.3670467) paper.

**Preliminary Requirements**
1. *Python* installed with **latest** distribution of *pip*.
2. The '1221' folder found [here](https://data.mendeley.com/datasets/nxk9r22wd6/1). For ease of operations, suggested practice is extracting it to a new subfolder of this master folder (e.g., *./data/*).
3. A *config.ini* file following the structure of the example. **All fields are mandatory**.

**Execution Instructions**
1. Run *launch.py* **from repository root** using the existing *Python* distribution. The path to the virtual environment's Python installation will be written to the file *venvPython_path.txt*.
2. After *launch.py* finishes configuring the virtual environment, use <p align = 'center'>*```<venvPython_path> -m invoke runPipelineWithYUMCD```*</p> to run the entire pipeline, from input extraction to fusion/final decisions. You may use <p align = 'center'>*```<venvPython_path> -m invoke clear```*</p> to delete the *existing* virtual environment and all other runtime artifacts created by the executables.