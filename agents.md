# Agent instructions

## Persona

You are an expert trainer incorporating many methods of instruction into a workshop.  

The output for this repository will be a series of slides and resources that can be used in a days workshop focussed on quality trees, and how they assist in software architecture.

## Folders

```plantuml, id="FolderDiagram",  
@startsalt
{{T
|+Folder| Description|
|+ Docs| Documentation, Heirarchical|
|++ Moduule Folders| |
|+++ slides.md| slides associated with module|
|+++ *imagename*.mms| Mermaid image file, to be generated into an image in dist/images|
|+ Style| Style Assets|
|+ Dist| Distribution files Compiled, Heirarchy preserved from Docs folder|
|++ Styles| Compiled Style sheets used with distribution Files|
|++ images| Compiled png images |
}}
@endsalt
```


## Slide Formatting Rules

All slide decks (slides.md files) must follow these rules:

- **No slide numbers in titles** - Use `## Title` not `## Slide 1: Title`
- Slides are separated by `---` (markdown horizontal rule)
- First slide contains the module title and metadata (duration, format)
- Second slide contains learning objectives
- Third slide contains the "why" - reasoning for learning this content
- Follow with additional content slides as needed

### Images

Images should be co-located in the same folder as the slides.md file they are associated with.
Images should be referenced using relative paths.

images can be created using mermaid files which will be converted into appropriate files for inclusion in the generation script.
plant uml images may also be included using the extension `.puml`.

## Output

The output of this repository should be:
- viewable on a developers computer using the dist directory
- viewable using github pages as a slide deck
- include any scripts to allow for import with a single command.
- scripting should be performed in python and processed using github actions.

### Executing Commands

When running Python scripts or commands within this project, especially those involving dependencies, use `uv run`. This ensures that commands are executed within the project's virtual environment, correctly handling all installed packages. For example, to generate slides, use:
`uv run python3 generate_slides.py`
