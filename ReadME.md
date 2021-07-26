### Install & Test Run

1. Download & install [Python 3.9.x](https://www.python.org/downloads/).

2. Create and activate Python virtual environment [(official documentation)](https://docs.python.org/3/library/venv.html). \
Create: ```python -m venv myenv``` \
Activate in *Ubuntu*: ```source myenv/bin/activate``` \
Activate in *Windows*: ```source myenv/Scripts/activate```

3. Download the files from this repository into the server host. \
```git clone https://github.com/CYBEX-P/cybexp-archive.git```

4. Install external dependencies
```
cd cybexp-archive
pip install -r requiremnts.txt
```

5. Download and install TAHOE
```
cd ..
git clone https://github.com/CYBEX-P/tahoe
cd tahoe
python setup.py install
```

6. Unittest
```
cd ../cybexp-archive
python -m unittest
```

7. Test Run
```
python archive.py
```
