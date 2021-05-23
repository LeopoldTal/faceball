# faceball

Turn a person's face into a ball representing their ideology.

## Motivation

Consider the humble ancapball. Thanks to it, we can express the sentiment "The current topic of conversation is representative of anarcho-capitalist ideological principles". How convenient and delightful!

![ancapball](doc/ancap.jpg)

This cries out for generalisation. A discussion on free software principles needs a Stallmanball; a debate over foreign aid requires the ability to describe a position as "based and Moyopilled".

![Richard Stallman ball](examples/ball/stallman.png) ![Dambisya Moyo ball](examples/ball/moyo.jpg)

Blame for this idea rests on anthropicprincipal.

## Usage

````
python faceball.py [--debug] [-b BACKGROUND] input_image_path [output_image_path]
````

Supported formats: PNG and JPG.

`output_image_path` defaults to the input path, with the name prefixed by `ball_`.

The background fill colour can be "white", "black", "discord" (Discord dark theme), a hex code (e.g. `ff8800`), or comma-separated decimal RGB (e.g. `255,128,0`). Default is transparent for PNG and Discord for JPG.

A log is written to `log/` with intermediate images. The `--debug` flag adds marks on the image.
