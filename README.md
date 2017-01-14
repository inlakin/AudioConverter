# Audio Converter

This program enables the conversion of a specific codec from a music folder to another. (i.e "I want to convert all my flac audio files to mp3 because my lazy mp3 player can't handle flac files")

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.


### Resolving the dependencies

```
pip install -r requirements.txt
```

### Installing


After resolving the dependencies, you should run the [settings.py] file
```
./settings.py 
```

### Usage examples

Help command :
```
AudioConverter -h 
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

THe only mandatory argument is the type of codec we want to convert in all of our music folder (i.e "flac")

### Basic usage 

```
AudioConverter flac --check --path=path/to/music/folder --output_file=logerr.txt
```

This command will first check all the 'flac' files in the path/to/music/folder folder and then proceed to the conversion. If any error is encountered, they will be output in the 'logerr.txt' file.


```

## Running the tests

No tests implemented yet .. :(

## Deployment

Add additional notes about how to deploy this on a live system


## Authors

* **Robin Desir** - *Initial work* - [RobinDesir](https://github.com/RobinDesir)


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Yet to come


