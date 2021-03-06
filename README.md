# Audio Converter

This program enables the conversion of a specific codec from a music folder to another. (i.e "I want to convert all my flac audio files to mp3 because my lazy mp3 player can't handle flac files")

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and standard usage.


### Fetching the project and resolving the dependencies

Fetch the project using :

```
$ git clone https://github.com/inlakin/AudioConverter.git
```

Move into the project

```
$ cd AudioConverter/
```

and resolve the dependencies using the following command

```
$ pip install -r requirements.txt
```


for practical usage, I recommend adding the folder to the path. 


### Usage examples

Help command :

```
$ AudioConverter -h 
```

Will output :

```
AudioConverter 

Programm that permits to convert a music folder into another codec (i.e flac to mp3)
 
Usage:
    AudioConverter.py <original_codec> [options]
    AudioConverter.py -h | --help
    AudioConverter.py -v | --version
 
Options:
  -h, --help      
  -v, --version      
  --check               Check the number of file to convert before conversion       [default: False]
  --to=<codec>          Output codec                                                [default: mp3]
  --path=<path>         Path to the music folder (default is the current folder)
  --bitrate=<b>         Bitrate (64k, 128k, 192k...)                                [default: 128k]
  --output_file=<file>  Output file name                                            [default: AudioConverter_log_err.txt]
```

THe only **mandatory argument** is the type of codec we want to convert in our based music folder (i.e "flac")

### Basic usage 

```
$ AudioConverter flac --check --path=path/to/music/folder --output_file=logerr.txt
```

This command will first check all the *flac* files in the *path/to/music/folder* folder and then proceed to the conversion. If any error is encountered, they will be output in the *logerr.txt* file.

If the user wants to proceed with the conversion, a new folder will be created for storing each of the converted folder (i.e If we are converting the *"Apparat"* folder that contains only flac files, a new folder *"Apparat - mp3"* will be created containing all the mp3 files.)

## GIF

![Output](http://github.com/inlakin/AudioConverter/blob/master/output.gif)
![Output 2](http://github.com/inlakin/AudioConverter/blob/master/output2.gif)

## License

This project is licensed under the MIT License - see the [LICENSE.md](https://github.com/inlakin/AudioConverter/LICENSE.md) file for details



