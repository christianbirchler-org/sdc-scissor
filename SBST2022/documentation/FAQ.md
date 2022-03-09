# Frequently Asked Questions

### 1. BeamNG does not start and I get a `socket.timeout` exception.

If you experience this problem please check if the path to the folder containing the BeamNG executables and/or the path the user folder contain any space. If so, please move the offending folder to a location without spaces in the path.

Another possible cause is the use of environmental variables to configure BeamNG that might take over the parameters to configure the BeamNG executors. For this reason, we discourage using environmental variables and suggest to use the command line parameters `--beamng-home` and `--beamng-user` instead.

### 2. BeamNG starts but I get a `ConnectionRefusedError` exception.

You may experience this problem if you did not set properly the `--beamng-user` path to the folder you created and in which you copied the `tech.key` file.

### 3. Dave2 executor fails to starts because tensorflow does not find a DLL.

The Dave2 executor uses TensorFlow 2.4.1. which does not strictly require you to install the CUDA libraries to run. TensorFlow uses the CPU when it cannot find any suitable GPU. However, on computers that have NVidia GPUs, it may try to load a few DLLs and sometimes it fails to do so, raising the following error message:

```
ImportError: DLL load failed: The specified module could not be found.
```

The solution we tried and that worked for us is documented [here](https://github.com/tensorflow/tensorflow/issues/35749). In summary, you need to

1. Go to [https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads](https://support.microsoft.com/en-us/help/2977003/the-latest-supported-visual-c-downloads)
2. Download vc_redist.x64.exe (if you are using a 64-bit machine);
3. Install it;
4. Reboot your PC.

You can use the following code (after activating the virtual environment) to test whether this solved your issue.

Start the python interpreter:

```
$py.exe
Python 3.7.9 (tags/v3.7.9:13c94747c7, Aug 17 2020, 18:58:18) [MSC v.1900 64 bit (AMD64)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>>
```

Type in:

```
import tensorflow as tf
```

If this code does not crash the interpreter you should be ready to go.

Note: do not worry if you see a message like this:

```
W tensorflow/stream_executor/platform/default/dso_loader.cc:60] Could not load dynamic library 'cudart64_110.dll'; dlerror: cudart64_110.dll not found
I tensorflow/stream_executor/cuda/cudart_stub.cc:29] Ignore above cudart dlerror if you do not have a GPU set up on your machine.
```
### 4. BeamNG starts but the pipeline cannot load the level/map

We noticed that setting the `beamng-user` and `beamng-home` options to point to the same folder the simulators starts but the pipeline fails. Despite this setting worked in the past, we suggest you use different folders to host the simulator (`beamng-home`) and the user data (`beamng-user`).
