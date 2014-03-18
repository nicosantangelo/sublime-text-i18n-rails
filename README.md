# Sublime Text: I18n Rails

This package is aimed to help you create Internationalization keys.

## Available commands

### 1. Checking keys
If you want to check which keys in the file are present in the `*.yml` files, you can open up a Rails view and [run][1] "I18n Rails: Toggle key highlighting", resulting in something like this:

![](https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/demo.png)

Each translation is looked up in the relative or absolute path (the same logic applied for adding the values). So, in the example:
  
  * `.missing_key` wasn't found on any `*.yml` file. Uses the "invalid" scope for the color.
  * `.partial` was found in some locales but no all (for example, only defined in en.yml but missing in es.yml). Uses the "string" scope for the color.
  * `.full` is correctly added. Uses the "comment" scope for the color.

### 2. Adding keys ([readme][5])
To add a key, go to a Rails view, [select][4] the key you want to add a value to and [run][1] the command "I18n Rails: Add key".

The package will display a prompt asking for the value in every language available, If the key value is found, the prompt will show it (so it can be edited easily). If you don't want to edit a locale, just skip it by pressing Esc.


The package supports relative and absolute routes, for example


````erb
<%# views/users/index.html.erb %>

<%= t('.hello') %>  <%# It will search in config/locales/views/users/*.yml (see note below) %>

<%# (...) %>

<%= t('some.other.key.bye') %> <%# It will search in config/locales/*.yml %>
````

**Notes** 
 * If the package doesn't find the path (for example with `.hello`) it will default to `config/locales/*.yml`.
 * The package requires the root key (`es:`, `en:`, etc.) to be present to work.

##### Known "issue"
Because of the way [PyYAML][6], the python yaml parser, dumps the loaded yaml files I can't ensure the file format after a value it's added using this command. I couldn't find a work around this, so I made an [issue][7] wich also contains an (unanswered) stackoverflow question.

I'm thinking of some way to improve this, but in the meantime if you want to help, any ideas are welcome or just fork away!


### 3. Go to YAML file
If you [run][1] "I18n Rails: Go to YAML file" [selecting][4] a key, you will be prompted with the files where the key might be defined, so you can access them quickly (as a tip, you can go back to the file you were editing with the sublime command *jump_back*, *["alt+-""]* by default).

If the translation is found, the quick panel will show it after the locale:

````yaml
    en.yml: With translation
    es.yml
````

## Selecting keys
To select a key you can:

1. Select the text (with or without quotes), for example, select `this.key` from `<%= t 'this.key' %>`.
2. Place the cursor inside the quotes and [run][1] "I18n Rails: Add key".

## Settings

````json
{
    "rejected_files": [],
    
    "valid_color_scope"  : "comment",
    "partial_color_scope": "string",
    "invalid_color_scope": "invalid",
    
    "reload_highlighted_keys_on_save": true
}
````
### Rejected files
You can add to the array any file you want to skip in when you're running the adding or check commands. So for example, if you want to skip devise files:

````json
{ "rejected_files": ["devise.es.yml", "devise.en.yml"] }
````

The settings are accesible from Menu -> Preferences -> Package settings -> I18nRails

### Color scopes
If you'd like to customize the color used to hightlight each key, you can add an existing scope name to the settings, or define a new one in your colorscheme file (`.tmTheme`), for example:

````json
  { "invalid_color_scope": "i18ninvalid" }
````

````xml
<!-- Color scheme -->
<dict>
  <key>name</key>
  <string>I18n invalid</string>
  <key>scope</key>
  <string>i18ninvalid</string>
  <key>settings</key>
  <dict>
    <key>background</key>
    <string>#FF0DFF</string>
    <key>fontStyle</key>
    <string></string>
    <key>foreground</key>
    <string>#E80C7A</string>
  </dict>
</dict>
````

You may have to restart sublime to see the changes.

### Reload on save

If this setting is true, the highlighted keys will be updated on each save, so if anything changed it will be picked up changing the colors appropriately.

Right now to reload, you need to save the file with the highlighted keys, meaning that the keys wont change if the save is only made in (for example) the .yml file alone.

## Shortcut Keys

**Windows and Linux:**

 * Add:   `ctrl+alt+i` 
 * Toggle: `ctrl+alt+u`
 * Go to file: `ctrl+alt+y`

**OSX**

 * Add:   `super+alt+i` 
 * Toggle: `super+alt+u` 
 * Go to file: `super+alt+y` 

## Installation

This package is available in [Package Control][2] or you can clone the repo into your `/Packages` folder.

The package name is `I18n Rails`.

## Roadmap

 * ~~Command to "Go to yml file".~~
 * ~~Support custom color scopes.~~
 * ~~Allow path filtering.~~

## Copyright

Copyright &copy; 2013+ Nicolás Santángelo. 

See LICENSE for details.

  [1]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#shortcut-keys
  [2]: https://sublime.wbond.net/
  [3]: https://raw.github.com/NicoSantangelo/sublime-text-i18n-rails/master/LICENSE
  [4]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#selecting-keys
  [5]: https://github.com/NicoSantangelo/sublime-text-i18n-rails#known-issue
  [6]: http://pyyaml.org/
  [7]: https://github.com/NicoSantangelo/sublime-text-i18n-rails/issues/6
