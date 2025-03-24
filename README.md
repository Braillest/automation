# Purpose:

Convert text into the expected paginated braille format.

# Getting started

Clone repo, create a terminal at the root of the repo and run the following to build and run the container:

```
docker compose up -d
```

# Structure

The `data` directory contains subdirectories for each different text translation state.

The `scripts` directory contains helpful entrypoints to convert and obtain source materials to test with.

- convert_text_to_all - An interactive script that allows you to specify paths before converting text to braille, paginating it, and back translating it.
- convert_text_to_braille - An interactive script that allows specification of text inpout and braille output path and generates the braille.
- download_books - A helpful development script for getting text to test with.
- text_to_braille_test - An example hardcoded script performing some various operations.

The `src` directory contains the source code for the Book.py class that translation/pagination scripts use.

# Using the container

Enter the container:

```
docker exec -it braillest_python bash
```

Execute a script:

```
python convert_text_to_all.py
```

Exit the container:

```
exit
```

# Use case:

Place the text you want to convert in the data/text directory.

Enter the container and run `python convert_text_to_all.py`.

Follow the interactive prompts and provide paths to directories as requested.

With the resultant pages directory filed with paginated braille, copy the resource over to the webapplication repo for blender STL generation.
