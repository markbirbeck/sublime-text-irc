# sublime-text-irc

IRC client for Sublime Text 3

## Introduction

This is a very alpha IRC plugin for Sublime Text 3, inspired by Emacs IRC clients such as ERC. Although there are obviously much better clients in the form of Adium, Limechat, et. al., there are many advantages to having IRC built into your text editor. The goal here is to be automatically connected to a particular channel when working on a specific project.

## Installation

In the `Packages` directory:

```shell
git clone https://github.com/markbirbeck/sublime-text-irc.git IRC
```

## Using the IRC Command

To create an IRC buffer run the IRC command with a list of connection settings:

```python
view.run_command("irc", {"server": "irc.freenode.net", "target": "#sublimetext"})
```

To wire a command into the Command Palette edit your *Preferences > Package Settings > IRC > Commands - User* file. You can find some examples in the *Commands - Default* file.

## Using the IRC client

Any time `[ENTER]` is pressed commands are submitted to the selected IRC server. If no text is selected and the cursor is simply on the last line of the buffer then the whole line is sent, without the prompt. If any text is selected then in keeping with the spirit of Sublime, each selection is submitted as its own command.

## Improving the IRC Client

There's lots of scope for improvement!

New feature requests, bugs and of course pull requests will all be managed via the issue-tracker.

Code is formatted with PEP8 with E501 turned off (i.e., the default settings for `SublimeLinter`).

GitFlow is used for branching and preparing releases.

### Architecture

The client tries to fit in with Sublime Text's architecture as much as possible. So for example, an IRC window is simply a document with the IRC syntax type, which is how things like user names and status messages get their appearance.

### Limitations

The main limitation is that [the prompt is not protected](issues/7)! If you type over it then the plugin won't be able to find the end of the buffer and therefore won't know where to insert text. It should be straightforward to fix, but for now just watch those backspaces.

## Changelog

2013-07-02 Initial release. (v0.1)
