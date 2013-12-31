# Sublime Text: Rails I18n

This package is aimed to help you create Internationalization keys.

## Available commands

### Checking keys
If you want to check which keys in the file are present in the `*.yml` files, you can open up a Rails view and [run][1] "I18n Rails: Toggle key highlighting", resulting in something like this:

![](https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/demo.png)

Each translation is looked up in the relative or absolute path (the same logic applied for adding the values). So, in the example:
  
  * `.missing_key` wasn't found on any `*.yml` file. Uses the "invalid" scope for the color.
  * `.partial` was found in some locales but no all (for example, only defined in en.yml but missing in es.yml). Uses the "string" scope for the color.
  * `.full` is correctly added. Uses the "comment" scope for the color.

### Adding keys ([readme][5])
To add a key, go to a Rails view, [select][4] the key you want to add a value to and [run][1] the command "I18n Rails: Add key".

The package will display a prompt asking for the value in every language available, If the key value is found, the prompt will show it (so it can be edited easily). If you don't want to edit a locale, just skip it by pressing Esc.


The package supports relative and absolute routes, for example


````erb
<%# views/users/index.html.erb %>

<%= t('.hello') %>  <%# It will search in config/locales/views/users/*.yml (see note below) %>

<%# (...) %>

<%= t('some.other.key.bye') %> <%# It will search in config/locales/*.yml %>
````

**Note:** If the package doesn't find the path (for example with `.hello`) it will default to `config/locales/*.yml`.
**Note2:** The package requires the root key (`es:`, `en:`, etc.) to be present to work.

##### Readme
Because of the way [PyYAML][6], the python yaml parser, dumps the loaded yaml files I can't ensure the file format after a value it's added using this command. I couldn't find a work around this, so I made an [issue][7] wich also contains an (unanswered) stackoverflow question.

I'm thinking of some way to improve this, but right now I'll leave the issue open and add a *"(experimental)"* "tag" to the command name.
If you want to help, any ideas are welcome or just fork away! 


### Go to YAML file
If you [run][1] "I18n Rails: Go to YAML file" [selecting][4] a key, you will be prompted with the files where the key might be defined, so you can access them quickly (as a tip, you can go back to the file you were editing with the sublime command _jump_back_, "alt+-" by default).
The implementation is kind of rough right now, I will try to improve it overtime.

### Select keys
To select a key you can:

1. Select the text (with or without quotes), for example, select `this.key` from `<%= t 'this.key' %>`.
2. Place the cursor inside the quotes and [run][1] "I18n Rails: Add key".

## Shortcut Keys

**Windows and Linux:**

 * Add:   `ctrl+alt+i` 
 * Toggle: `ctrl+alt+u`
 * Go to file: `ctrl+alt+f`

**OSX**

 * Add:   `super+alt+i` 
 * Toggle: `super+alt+u` 
 * Go to file: `super+alt+f` 

## Settings

Right now, there's only one available setting

````json
{
    "rejected_files": []
}
````

You can add to the array any file you want to skip in when you're running the adding or check commands. So for example, if you want to skip devise files:

` { "rejected_files": ["devise.es.yml", "devise.en.yml"] }`

The settings are accesible from Menu -> Preferences -> Package settings -> I18nRails

## Installation

This package is available in [Package Control][2] or you can clone the repo into your package folder (use Package Control, is awesome).

## Roadmap

 * ~~Command to "Go to yml file".~~
 * Support custom color scopes.
 * ~~Allow path filtering.~~

## License
[MIT][3]

  [1]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#shortcut-keys
  [2]: https://sublime.wbond.net/
  [3]: https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/LICENSE
  [4]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#select-keys
  [5]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#readme
  [6]: http://pyyaml.org/
  [7]: https://github.com/NicoSantangelo/sublime-text-i18n-rails/issues/6
